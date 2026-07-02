#!/usr/bin/env python3
"""
ADR verification module for the Green Score Analyzer.
=====================================================

Parses Architecture Decision Records (MADR-style Markdown with YAML
front-matter) under an ``--adr-dir`` and runs cross-validation checkers
against the OpenAPI spec, runtime measurements and (optionally) the
source-dir IaC/build files already scanned by ``architecture_rules.py``.

Design rules — strict:
  • stdlib-only (no PyYAML) — front-matter is parsed with a minimal, safe
    YAML subset (strings, ints, booleans, lists, mappings).
  • every checker returns a ``{ok, evidence, reason}`` triple so the
    dashboard can render *why* an ADR passed or failed.
  • ADRs with ``status: deprecated | superseded | proposed`` are skipped
    (only ``accepted`` gates the build).
  • Cross-referenced with ``architecture_rules`` helpers when possible to
    avoid re-implementing the same logic (SSE detection, CDN headers,
    IaC scan, dependency scan…).

CLI usage (standalone self-test)::

    python3 adr_rules.py --adr-dir docs/adr --spec openapi.json

Integration usage (called by green-api-auto-discover.py)::

    from adr_rules import evaluate_adrs
    report = evaluate_adrs(
        adr_dir="docs/adr",
        spec=merged_spec,
        endpoints=endpoints,
        measurements=measurements,
        base_urls=base_urls,
        source_dir=source_dir,
        scanned_files=phase2_scanned,   # optional pre-scan
    )
"""
from __future__ import annotations

import fnmatch
import json
import os
import re
import sys
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any, Callable

# ---------------------------------------------------------------------------
# Minimal safe YAML subset parser (front-matter only)
# ---------------------------------------------------------------------------

_SCALAR_RE = re.compile(r"^(-?\d+(?:\.\d+)?|true|false|null|~)$", re.IGNORECASE)


def _coerce_scalar(v: str) -> Any:
    """Coerce a bare string to int/float/bool/None when it matches."""
    s = v.strip()
    if not s:
        return ""
    if (s.startswith('"') and s.endswith('"')) or (s.startswith("'") and s.endswith("'")):
        return s[1:-1]
    if s.lower() in ("true", "yes"):
        return True
    if s.lower() in ("false", "no"):
        return False
    if s.lower() in ("null", "~"):
        return None
    if _SCALAR_RE.match(s):
        try:
            if "." in s:
                return float(s)
            return int(s)
        except ValueError:
            return s
    return s


def _parse_flow_list(s: str) -> list:
    """Parse ``[a, b, "c"]`` flow-style YAML list."""
    inner = s.strip()[1:-1].strip()
    if not inner:
        return []
    parts, depth, buf = [], 0, ""
    for ch in inner:
        if ch in "[{":
            depth += 1
        elif ch in "]}":
            depth -= 1
        if ch == "," and depth == 0:
            parts.append(buf)
            buf = ""
            continue
        buf += ch
    if buf.strip():
        parts.append(buf)
    return [_coerce_scalar(p.strip()) for p in parts]


def parse_front_matter(text: str) -> tuple[dict, str]:
    """Return ``(front_matter_dict, body_markdown)``.

    Supports the small YAML subset used in ADR front-matter:
      - top-level ``key: value``
      - flow lists ``key: [a, b]``
      - block lists of mappings under a key, e.g.::

            verifies:
              - kind: sse_endpoint
                path: /**/events
              - kind: absent_query_param
                param: poll
    """
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end == -1:
        return {}, text
    header = text[3:end].strip("\n")
    body = text[end + 4:].lstrip("\n")

    lines = [ln for ln in header.splitlines() if ln.strip() and not ln.lstrip().startswith("#")]
    root: dict = {}
    i = 0
    while i < len(lines):
        raw = lines[i]
        indent = len(raw) - len(raw.lstrip(" "))
        line = raw.strip()
        # top-level entries only
        if indent != 0 or ":" not in line:
            i += 1
            continue
        key, _, val = line.partition(":")
        key = key.strip()
        val = val.strip()
        if val:
            root[key] = _parse_value(val)
            i += 1
            continue
        # key with no inline value → block list of dicts, block scalar, or empty
        # Peek next non-empty line
        j = i + 1
        items: list = []
        while j < len(lines):
            sub_raw = lines[j]
            sub_indent = len(sub_raw) - len(sub_raw.lstrip(" "))
            if sub_indent == 0:
                break
            sub_line = sub_raw.strip()
            if sub_line.startswith("- "):
                # new list item — collect a dict from this "-" line plus
                # subsequent deeper-indented "key: value" lines until we
                # hit either another "-" at the same indent or a shallower line.
                item_dict: dict = {}
                first_kv = sub_line[2:].strip()
                if ":" in first_kv and not first_kv.startswith("["):
                    k2, _, v2 = first_kv.partition(":")
                    item_dict[k2.strip()] = _parse_value(v2.strip())
                elif first_kv:
                    # scalar list item
                    items.append(_parse_value(first_kv))
                    j += 1
                    continue
                item_indent = sub_indent
                j += 1
                while j < len(lines):
                    inner_raw = lines[j]
                    inner_indent = len(inner_raw) - len(inner_raw.lstrip(" "))
                    inner_line = inner_raw.strip()
                    if inner_indent <= item_indent:
                        # another "- " at same indent OR outdented → stop
                        break
                    if ":" in inner_line and not inner_line.startswith("- "):
                        k3, _, v3 = inner_line.partition(":")
                        item_dict[k3.strip()] = _parse_value(v3.strip())
                    j += 1
                if item_dict:
                    items.append(item_dict)
            else:
                # not a list — treat as empty
                break
        root[key] = items if items else []
        i = j
    return root, body


def _parse_value(v: str) -> Any:
    v = v.strip()
    if not v:
        return ""
    if v.startswith("[") and v.endswith("]"):
        return _parse_flow_list(v)
    return _coerce_scalar(v)


# ---------------------------------------------------------------------------
# ADR data model
# ---------------------------------------------------------------------------

@dataclass
class AdrCheckResult:
    kind: str
    ok: bool
    reason: str = ""
    evidence: list[dict] = field(default_factory=list)
    params: dict = field(default_factory=dict)


@dataclass
class AdrResult:
    adr: str                     # ADR number ("0007") or filename stem
    title: str
    status: str
    file: str
    green_rules: list[str] = field(default_factory=list)
    checks: list[AdrCheckResult] = field(default_factory=list)
    skipped: bool = False
    ok: bool = True

    @property
    def failed_checks(self) -> list[AdrCheckResult]:
        return [c for c in self.checks if not c.ok]


# ---------------------------------------------------------------------------
# Path matching helpers
# ---------------------------------------------------------------------------

def _path_matches(pattern: str, path: str) -> bool:
    """Match an OpenAPI path against a glob. `/**` matches any depth."""
    if not pattern:
        return True
    p = pattern.replace("/**", "/*")
    # Normalise trailing slashes
    return fnmatch.fnmatch(path, pattern) or fnmatch.fnmatch(path, p) or (
        pattern.endswith("/**") and path.startswith(pattern[:-3])
    )


def _iter_operations(spec: dict):
    for path, ops in ((spec or {}).get("paths") or {}).items():
        if not isinstance(ops, dict):
            continue
        for method, op in ops.items():
            if method not in ("get", "post", "put", "patch", "delete", "head", "options"):
                continue
            if isinstance(op, dict):
                yield path, method, op


def _op_query_params(op: dict) -> set[str]:
    params = op.get("parameters") or []
    return {
        (p or {}).get("name", "").lower()
        for p in params
        if isinstance(p, dict) and (p.get("in") == "query")
    }


# ---------------------------------------------------------------------------
# Checkers
# ---------------------------------------------------------------------------

def _check_has_pagination_params(spec, ctx, **params) -> AdrCheckResult:
    path_glob = params.get("path", "/**")
    wanted = [str(x).lower() for x in (params.get("params") or ["page", "size"])]
    any_of = bool(params.get("any_of"))
    hits, misses = [], []
    for path, method, op in _iter_operations(spec):
        if method != "get" or not _path_matches(path_glob, path):
            continue
        # Heuristic: only care about "collection-like" endpoints
        # (no path parameter at the end)
        if path.rstrip("/").endswith("}"):
            continue
        qp = _op_query_params(op)
        if any_of:
            has_it = any(w in qp for w in wanted)
        else:
            has_it = all(w in qp for w in wanted)
        if has_it:
            hits.append(f"{method.upper()} {path}")
        else:
            misses.append(f"{method.upper()} {path} (has: {sorted(qp) or '∅'})")
    ok = not misses
    return AdrCheckResult(
        kind="has_pagination_params",
        ok=ok,
        reason=(
            f"{len(hits)} endpoint(s) OK"
            if ok
            else f"{len(misses)} endpoint(s) sans {'|'.join(wanted) if any_of else '+'.join(wanted)}"
        ),
        evidence=[{"kind": "hit", "value": h} for h in hits[:5]]
                 + [{"kind": "miss", "value": m} for m in misses[:5]],
        params=params,
    )


def _check_sse_endpoint(spec, ctx, **params) -> AdrCheckResult:
    path_glob = params.get("path", "/**")
    ct_expected = str(params.get("content_type", "text/event-stream")).lower()
    declared, confirmed = [], []
    for path, method, op in _iter_operations(spec):
        if not _path_matches(path_glob, path):
            continue
        for resp in (op.get("responses") or {}).values():
            if not isinstance(resp, dict):
                continue
            for mt in (resp.get("content") or {}).keys():
                if ct_expected in mt.lower():
                    declared.append(f"{method.upper()} {path} ({mt})")
                    key = f"{method}:{path}"
                    m = (ctx.get("measurements") or {}).get(key) or {}
                    hdrs = m.get("response_headers") or {}
                    if ct_expected in (hdrs.get("content-type", "").lower()):
                        confirmed.append(f"{method.upper()} {path}")
                    break
    if not declared:
        return AdrCheckResult(
            kind="sse_endpoint", ok=False, params=params,
            reason=f"Aucun endpoint SSE déclaré sur {path_glob}")
    return AdrCheckResult(
        kind="sse_endpoint",
        ok=bool(confirmed) or True,  # spec declaration alone counts
        reason=(f"{len(confirmed)} SSE confirmé(s) runtime"
                if confirmed else f"{len(declared)} SSE déclaré(s) (runtime non testé)"),
        evidence=[{"kind": "spec", "value": d} for d in declared[:5]]
                 + [{"kind": "runtime", "value": c} for c in confirmed[:5]],
        params=params,
    )


def _check_absent_query_param(spec, ctx, **params) -> AdrCheckResult:
    path_glob = params.get("path", "/**")
    forbidden = str(params.get("param", "")).lower()
    hits = []
    for path, method, op in _iter_operations(spec):
        if not _path_matches(path_glob, path):
            continue
        if forbidden in _op_query_params(op):
            hits.append(f"{method.upper()} {path}")
    return AdrCheckResult(
        kind="absent_query_param",
        ok=not hits,
        reason=(f"Param interdit `{forbidden}` présent sur {len(hits)} endpoint(s)"
                if hits else f"Param `{forbidden}` absent (OK)"),
        evidence=[{"kind": "hit", "value": h} for h in hits[:10]],
        params=params,
    )


def _check_cdn_header_present(spec, ctx, **params) -> AdrCheckResult:
    wanted = [h.lower() for h in (params.get("headers") or [])]
    hits = []
    for key, m in (ctx.get("measurements") or {}).items():
        hdrs = (m or {}).get("response_headers") or {}
        for h in wanted:
            if h in hdrs:
                hits.append(f"{key}: {h}={hdrs[h]}")
                break
    return AdrCheckResult(
        kind="cdn_header_present",
        ok=bool(hits),
        reason=(f"{len(hits)} hit(s) CDN" if hits
                else f"Aucun des en-têtes CDN {wanted} observé"),
        evidence=[{"kind": "runtime", "value": h} for h in hits[:5]],
        params=params,
    )


def _check_iac_signal(spec, ctx, **params) -> AdrCheckResult:
    wanted = str(params.get("signal", "")).lower()
    any_of = [str(x).lower() for x in (params.get("any_of") or [wanted])]
    signals = set(ctx.get("iac_signals") or [])
    hit = signals & set(any_of)
    return AdrCheckResult(
        kind="iac_signal",
        ok=bool(hit),
        reason=(f"Signal(s) détecté(s): {sorted(hit)}"
                if hit else f"Aucun signal parmi {any_of} (scanné: {sorted(signals) or '∅'})"),
        evidence=[{"kind": "iac", "value": s} for s in sorted(hit)],
        params=params,
    )


def _check_dependency_present(spec, ctx, **params) -> AdrCheckResult:
    pattern = params.get("pattern", "")
    if not pattern:
        return AdrCheckResult(kind="dependency_present", ok=False,
                              reason="`pattern` manquant", params=params)
    try:
        rx = re.compile(pattern, re.IGNORECASE)
    except re.error as e:
        return AdrCheckResult(kind="dependency_present", ok=False,
                              reason=f"regex invalide: {e}", params=params)
    scanned = ctx.get("scanned_files") or []
    build_files = ("pom.xml", "build.gradle", "build.gradle.kts",
                   "package.json", "requirements.txt", "pyproject.toml", "Pipfile")
    hits = []
    for rel, text in scanned:
        fn = os.path.basename(rel)
        if not (fn in build_files or fn.endswith((".csproj", ".fsproj", ".vbproj"))):
            continue
        m = rx.search(text)
        if m:
            hits.append(f"{rel} → {m.group(0)[:60]}")
    return AdrCheckResult(
        kind="dependency_present",
        ok=bool(hits),
        reason=(f"{len(hits)} dépendance(s) trouvée(s)"
                if hits else f"Pattern `{pattern}` introuvable"),
        evidence=[{"kind": "deps", "value": h} for h in hits[:5]],
        params=params,
    )


def _check_openapi_field(spec, ctx, **params) -> AdrCheckResult:
    """Very simple field checker: dotted-path lookup + regex OR min_count for lists."""
    path = str(params.get("path", ""))
    expected = params.get("expected", "")
    min_count = params.get("expected_min_count")
    obj: Any = spec
    for key in path.split("."):
        if isinstance(obj, dict):
            obj = obj.get(key)
        else:
            obj = None
            break
    if min_count is not None:
        n = len(obj) if isinstance(obj, list) else 0
        ok = n >= int(min_count)
        return AdrCheckResult(
            kind="openapi_field", ok=ok, params=params,
            reason=f"{path} count={n} (attendu >= {min_count})",
            evidence=[{"kind": "spec", "value": f"{path}: {obj}"}])
    if expected:
        try:
            ok = bool(re.search(str(expected), str(obj or "")))
        except re.error:
            ok = False
        return AdrCheckResult(
            kind="openapi_field", ok=ok, params=params,
            reason=f"{path}={obj} vs /{expected}/",
            evidence=[{"kind": "spec", "value": f"{path}: {obj}"}])
    return AdrCheckResult(
        kind="openapi_field", ok=obj is not None, params=params,
        reason=f"{path} présent" if obj is not None else f"{path} absent",
        evidence=[{"kind": "spec", "value": f"{path}: {obj}"}])


def _check_endpoint_returns_status(spec, ctx, **params) -> AdrCheckResult:
    path_glob = params.get("path", "/**")
    status = str(params.get("status", ""))
    hits, misses = [], []
    for path, method, op in _iter_operations(spec):
        if not _path_matches(path_glob, path):
            continue
        responses = (op.get("responses") or {})
        if status in responses:
            hits.append(f"{method.upper()} {path}")
        else:
            misses.append(f"{method.upper()} {path}")
    ok = bool(hits)
    return AdrCheckResult(
        kind="endpoint_returns_status", ok=ok, params=params,
        reason=(f"{len(hits)} endpoint(s) déclarent {status}"
                if ok else f"Aucun endpoint sur {path_glob} ne déclare {status}"),
        evidence=[{"kind": "spec", "value": h} for h in hits[:5]])


def _check_response_header_present(spec, ctx, **params) -> AdrCheckResult:
    header = str(params.get("header", "")).lower()
    if not header:
        return AdrCheckResult(kind="response_header_present", ok=False,
                              reason="`header` manquant", params=params)
    req_ae = str(params.get("request_accept_encoding", "")).lower()
    hits = []
    for key, m in (ctx.get("measurements") or {}).items():
        hdrs = (m or {}).get("response_headers") or {}
        req  = (m or {}).get("request_headers") or {}
        if req_ae:
            if req_ae not in str(req.get("accept-encoding", "")).lower():
                continue
        if header in hdrs:
            hits.append(f"{key}: {header}={hdrs[header]}")
    return AdrCheckResult(
        kind="response_header_present", ok=bool(hits), params=params,
        reason=(f"{len(hits)} hit(s) sur `{header}`"
                if hits else f"En-tête `{header}` jamais observé"),
        evidence=[{"kind": "runtime", "value": h} for h in hits[:5]])


def _check_has_health_endpoint(spec, ctx, **params) -> AdrCheckResult:
    wanted = [p.rstrip("/") for p in (params.get("paths")
              or ["/health", "/actuator/health", "/metrics",
                  "/actuator/prometheus", "/q/metrics"])]
    declared_paths = set(((spec or {}).get("paths") or {}).keys())
    declared_hits = [p for p in wanted if p in declared_paths]
    runtime_hits = [k for k in (ctx.get("measurements") or {}).keys()
                    if any(w in k for w in wanted)]
    ok = bool(declared_hits or runtime_hits)
    return AdrCheckResult(
        kind="has_health_endpoint", ok=ok, params=params,
        reason=(f"Endpoints détectés: {declared_hits or runtime_hits}"
                if ok else f"Aucun endpoint santé parmi {wanted}"),
        evidence=[{"kind": "spec", "value": h} for h in declared_hits]
                 + [{"kind": "runtime", "value": h} for h in runtime_hits[:3]])


CHECKERS: dict[str, Callable] = {
    "has_pagination_params":   _check_has_pagination_params,
    "sse_endpoint":            _check_sse_endpoint,
    "absent_query_param":      _check_absent_query_param,
    "cdn_header_present":      _check_cdn_header_present,
    "iac_signal":              _check_iac_signal,
    "dependency_present":      _check_dependency_present,
    "openapi_field":           _check_openapi_field,
    "endpoint_returns_status": _check_endpoint_returns_status,
    "response_header_present": _check_response_header_present,
    "has_health_endpoint":     _check_has_health_endpoint,
}


# ---------------------------------------------------------------------------
# ADR discovery & evaluation
# ---------------------------------------------------------------------------

def _discover_adrs(adr_dir: str) -> list[Path]:
    p = Path(adr_dir).expanduser().resolve()
    if not p.is_dir():
        return []
    return sorted(f for f in p.glob("*.md") if not f.name.lower().startswith("readme"))


def _load_adr(path: Path) -> tuple[dict, str]:
    text = path.read_text(encoding="utf-8", errors="replace")
    fm, body = parse_front_matter(text)
    return fm or {}, body


def evaluate_adrs(
    *,
    adr_dir: str,
    spec: dict,
    endpoints: list | None = None,
    measurements: dict | None = None,
    base_urls: list | None = None,
    source_dir: str | None = None,
    scanned_files: list | None = None,
    iac_signals: list | None = None,
) -> dict:
    """Run every ADR checker and return a dashboard-ready report."""
    adr_files = _discover_adrs(adr_dir)
    ctx = {
        "endpoints": endpoints or [],
        "measurements": measurements or {},
        "base_urls": base_urls or [],
        "source_dir": source_dir,
        "scanned_files": scanned_files or [],
        "iac_signals": iac_signals or [],
    }

    results: list[AdrResult] = []
    for f in adr_files:
        fm, _body = _load_adr(f)
        adr_id = str(fm.get("adr") or f.stem.split("-", 1)[0])
        title = str(fm.get("title") or f.stem)
        status = str(fm.get("status") or "proposed").lower()
        green_rules = [str(x) for x in (fm.get("green_rules") or [])]
        r = AdrResult(adr=adr_id, title=title, status=status,
                      file=str(f), green_rules=green_rules)

        if status != "accepted":
            r.skipped = True
            results.append(r)
            continue

        verifies = fm.get("verifies") or []
        if not isinstance(verifies, list):
            r.ok = False
            r.checks.append(AdrCheckResult(
                kind="_meta", ok=False,
                reason=f"Front-matter `verifies:` doit être une liste (got {type(verifies).__name__})"))
            results.append(r)
            continue

        if not verifies:
            # Narrative ADR (no checks) — accepted as OK.
            results.append(r)
            continue

        for entry in verifies:
            if not isinstance(entry, dict):
                r.checks.append(AdrCheckResult(
                    kind="_meta", ok=False,
                    reason=f"Élément `verifies` invalide: {entry!r}"))
                continue
            kind = entry.get("kind")
            checker = CHECKERS.get(str(kind))
            if not checker:
                r.checks.append(AdrCheckResult(
                    kind=str(kind or "unknown"), ok=False,
                    reason=f"Checker `{kind}` inconnu"))
                continue
            params = {k: v for k, v in entry.items() if k != "kind"}
            try:
                res = checker(spec, ctx, **params)
            except Exception as e:  # noqa: BLE001
                res = AdrCheckResult(kind=str(kind), ok=False,
                                     reason=f"checker crash: {e}", params=params)
            r.checks.append(res)

        r.ok = all(c.ok for c in r.checks)
        results.append(r)

    accepted = [r for r in results if not r.skipped]
    passed   = [r for r in accepted if r.ok]
    failed   = [r for r in accepted if not r.ok]

    report = {
        "summary": {
            "total": len(results),
            "accepted": len(accepted),
            "skipped": len(results) - len(accepted),
            "passed": len(passed),
            "failed": len(failed),
            "score_pct": round(100 * len(passed) / max(1, len(accepted)), 1),
        },
        "adr_dir": adr_dir,
        "results": [
            {
                **asdict(r),
                "checks": [asdict(c) for c in r.checks],
            }
            for r in results
        ],
    }
    return report


# ---------------------------------------------------------------------------
# CLI (self-test)
# ---------------------------------------------------------------------------

def _cli(argv: list[str]) -> int:
    import argparse
    p = argparse.ArgumentParser(description="Evaluate ADRs against an OpenAPI spec.")
    p.add_argument("--adr-dir", required=True)
    p.add_argument("--spec", required=True, help="Path to a merged OpenAPI JSON spec")
    p.add_argument("--fail-on-violation", action="store_true")
    p.add_argument("--out", default="", help="Write JSON report to file")
    args = p.parse_args(argv)

    spec = json.loads(Path(args.spec).read_text(encoding="utf-8"))
    report = evaluate_adrs(adr_dir=args.adr_dir, spec=spec)
    text = json.dumps(report, indent=2, ensure_ascii=False)
    if args.out:
        Path(args.out).write_text(text, encoding="utf-8")
    print(text)
    if args.fail_on_violation and report["summary"]["failed"] > 0:
        print(f"\n❌ {report['summary']['failed']} ADR(s) failed.", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(_cli(sys.argv[1:]))


