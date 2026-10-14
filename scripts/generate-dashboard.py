#!/usr/bin/env python

"""Generate dashboard/index.html by embedding the latest report JSON.
Also generates dashboard/index.md (Markdown equivalent for GitHub rendering).
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from datetime import datetime

PLACEHOLDER = "__REPORT_JSON__"
CREEDENGO_PLACEHOLDER = "__CREEDENGO_JSON__"
ADR_PLACEHOLDER = "__ADR_JSON__"

# ── Labels & max scores for the breakdown table ──
LABELS = {
    "DE11_pagination": "DE11 Pagination",
    "DE08_fields": "DE08 Filtrage champs",
    "DE01_compression": "DE01 Compression",
    "DE02_DE03_cache": "DE02/03 Cache ETag",
    "DE06_delta": "DE06 Delta",
    "range_206": "206 Range",
    "LO01_observability": "LO01 Observabilité",
    "US07_rate_limit": "US07 Rate Limit",
    "AR02_format_cbor": "AR02 CBOR",
}
MAX_SCORES = {
    "DE11_pagination": 15,
    "DE08_fields": 15,
    "DE01_compression": 15,
    "DE02_DE03_cache": 15,
    "DE06_delta": 10,
    "range_206": 10,
    "LO01_observability": 5,
    "US07_rate_limit": 5,
    "AR02_format_cbor": 10,
}


def _fmt_bytes(n: int) -> str:
    if n >= 1_000_000:
        return f"{n/1_000_000:.1f} MB"
    if n >= 1_000:
        return f"{n/1_000:.1f} KB"
    return f"{n} B"


def generate_creedengo_markdown(creedengo: dict) -> str:
    """Return a Markdown section for the Creedengo eco-design analysis.

    The recap (severity breakdown) is focalized on Creedengo/ecodesign rules ONLY,
    not all SonarQube rules. General SonarQube issues are shown in a separate section.
    """
    lines: list[str] = []
    a = lines.append

    score = creedengo.get("creedengo_score", {})
    total = score.get("total", 0)
    grade = score.get("grade", "?")
    issues = score.get("issues_count", 0)
    bd = score.get("severity_breakdown", {})
    emoji = "🟢" if total >= 85 else "🟡" if total >= 70 else "🔴"

    sev_icons = {"BLOCKER": "🔴", "CRITICAL": "🟠", "MAJOR": "🟡", "MINOR": "⚪", "INFO": "🔵"}
    sev_labels_fr = {"BLOCKER": "Bloquant", "CRITICAL": "Critique", "MAJOR": "Majeur", "MINOR": "Mineur", "INFO": "Info"}

    a("")
    a("---")
    a("")
    a(f"## 🌱 Creedengo Éco-Design : **{total}/100** — Grade **{grade}** {emoji}")
    a("")
    a(f"> Analyse statique de l'éco-conception du code source via "
      f"[Creedengo](https://github.com/green-code-initiative) / SonarQube")
    a("")
    a("> ⚠️ **Seules les règles Creedengo/écodesign sont comptabilisées** "
      f"dans le score et le récapitulatif ci-dessous. "
      f"Les règles SonarQube générales sont listées séparément.")
    a("")

    # Detection metadata
    detection = creedengo.get("detection", {})
    if detection:
        langs = ", ".join(detection.get("languages", []))
        primary = detection.get("primary_language", "?")
        fw = detection.get("primary_framework", "")
        plugins = ", ".join(detection.get("plugins_used", []))
        a(f"- **Langages détectés** : {langs}")
        a(f"- **Principal** : {primary}" + (f" ({fw})" if fw else ""))
        a(f"- **Plugins Creedengo** : {plugins}")
        a("")

    # ── Severity breakdown — CREEDENGO RULES ONLY ──
    a("### 📊 Récapitulatif — Règles Creedengo écodesign uniquement")
    a("")
    a("| Sévérité | Nombre |")
    a("|:--------:|-------:|")
    total_issues_recap = 0
    for sev in ["BLOCKER", "CRITICAL", "MAJOR", "MINOR", "INFO"]:
        count = bd.get(sev, 0)
        total_issues_recap += count
        icon = sev_icons.get(sev, "⚪")
        label = sev_labels_fr.get(sev, sev)
        a(f"| {icon} **{label}** | {count} |")
    a(f"| **Total** | **{total_issues_recap}** |")
    a("")

    if total_issues_recap == 0:
        a("> ✅ **Aucune violation de règle Creedengo/écodesign détectée !** Bravo 🎉")
        a("")

    a(f"- **Issues écodesign** : {issues}")
    rules_violated = creedengo.get('rules_violated', 0)
    all_rules = creedengo.get('all_creedengo_rules', 0)
    a(f"- **Règles écodesign violées** : {rules_violated} / "
      f"{all_rules} analysées")
    a(f"- **Formule du score** : (1 − {rules_violated}/{all_rules}) × 100 = **{total}/100**")
    if score.get("total_effort"):
        a(f"- **Effort de remédiation** : {score['total_effort']}")
    a("")

    # Measures
    measures = creedengo.get("measures", {})
    ncloc = measures.get("ncloc", 0)
    if ncloc:
        a(f"- **Lignes de code** : {ncloc:,}")
        a("")

    # Categories (Creedengo only)
    categories = creedengo.get("categories", [])
    if categories:
        a("### 🏷️ Catégories éco-design")
        a("")
        a("| Catégorie | Issues | Règles |")
        a("|-----------|-------:|-------:|")
        for cat in categories:
            a(f"| {cat.get('label', cat.get('key', '?'))} | {cat['issues_count']} | {cat['rules_count']} |")
        a("")

    # Rules summary — Creedengo only (top 20)
    rules = creedengo.get("rules_summary", [])
    if rules:
        a("### 📋 Règles Creedengo violées")
        a("")
        a("| Sévérité | Règle | Issues | Catégorie |")
        a("|:--------:|-------|-------:|-----------|")
        for rule in rules[:20]:
            sev = rule.get("severity", "INFO")
            icon = sev_icons.get(sev, "⚪")
            short_key = rule["key"].split(":")[-1] if ":" in rule["key"] else rule["key"]
            a(f"| {icon} {sev} | **{short_key}** — {rule['name']} | {rule['count']} | {rule.get('category', '')} |")
        if len(rules) > 20:
            a(f"| | *… et {len(rules) - 20} autres* | | |")
        a("")

    # Top files (Creedengo only)
    top_files = creedengo.get("top_files", [])
    if top_files:
        a("### 📁 Fichiers les plus impactés (écodesign)")
        a("")
        a("| Fichier | Issues |")
        a("|---------|-------:|")
        for f in top_files[:10]:
            short = "/".join(f["file"].split("/")[-2:])
            a(f"| `{short}` | {f['count']} |")
        if len(top_files) > 10:
            a(f"| *… et {len(top_files) - 10} autres* | |")
        a("")

    # ═══════════════════════════════════════════════════════════════
    # ── General SonarQube issues (separate section, for context) ──
    # ═══════════════════════════════════════════════════════════════
    sonar = creedengo.get("sonar_issues", {})
    sq_count = sonar.get("issues_count", 0)
    if sq_count > 0:
        sq_bd = sonar.get("severity_breakdown", {})
        a("---")
        a("")
        a(f"### 🔧 Issues SonarQube générales (hors écodesign) — {sq_count} issues")
        a("")
        a("> Ces issues proviennent des règles SonarQube standard (qualité de code, "
          f"bugs, sécurité). Elles ne sont **pas** comptabilisées dans le score Creedengo.")
        a("")
        a("| Sévérité | Nombre |")
        a("|:--------:|-------:|")
        for sev in ["BLOCKER", "CRITICAL", "MAJOR", "MINOR", "INFO"]:
            count = sq_bd.get(sev, 0)
            if count > 0:
                icon = sev_icons.get(sev, "⚪")
                label = sev_labels_fr.get(sev, sev)
                a(f"| {icon} {label} | {count} |")
        a(f"| **Total** | **{sq_count}** |")
        a("")

        sq_rules = sonar.get("rules_summary", [])
        if sq_rules:
            a("| Sévérité | Règle | Issues |")
            a("|:--------:|-------|-------:|")
            for rule in sq_rules[:15]:
                sev = rule.get("severity", "INFO")
                icon = sev_icons.get(sev, "⚪")
                short_key = rule["key"].split(":")[-1] if ":" in rule["key"] else rule["key"]
                a(f"| {icon} {sev} | **{short_key}** — {rule['name']} | {rule['count']} |")
            if len(sq_rules) > 15:
                a(f"| | *… et {len(sq_rules) - 15} autres* | |")
            a("")

        if sonar.get("total_effort"):
            a(f"- **Effort de remédiation SonarQube** : {sonar['total_effort']}")
            a("")

    a(f"📅 *{creedengo.get('timestamp', '')}*")
    a("")

    return "\n".join(lines)


def _radar_svg(arch_scores: list[tuple[str, int, int]], size: int = 260) -> str:
    """Return an inline SVG radar chart for architecture rules.

    ``arch_scores`` is a list of (rule_id, score, max_pts). Any GitHub /
    GitLab Markdown renderer displays the SVG since it's embedded inline.
    """
    import math
    n = len(arch_scores)
    if n < 3:
        return ""
    cx = cy = size / 2
    r_max = size / 2 - 30
    # Axis points (max) and score points
    def _pt(i: int, ratio: float) -> tuple[float, float]:
        angle = -math.pi / 2 + 2 * math.pi * i / n
        return (cx + r_max * ratio * math.cos(angle),
                cy + r_max * ratio * math.sin(angle))
    axis_pts   = [_pt(i, 1.0) for i in range(n)]
    score_pts  = [_pt(i, (s / m) if m else 0) for i, (_id, s, m) in enumerate(arch_scores)]
    axis_poly  = " ".join(f"{x:.1f},{y:.1f}" for (x, y) in axis_pts)
    score_poly = " ".join(f"{x:.1f},{y:.1f}" for (x, y) in score_pts)
    # Concentric grid at 25/50/75/100 %
    grid = []
    for ratio in (0.25, 0.5, 0.75, 1.0):
        pts = " ".join(f"{cx + r_max*ratio*math.cos(-math.pi/2 + 2*math.pi*i/n):.1f},"
                       f"{cy + r_max*ratio*math.sin(-math.pi/2 + 2*math.pi*i/n):.1f}"
                       for i in range(n))
        grid.append(f'<polygon points="{pts}" fill="none" stroke="#e5e7eb" stroke-width="1"/>')
    # Axis lines + labels
    lines_svg = []
    labels_svg = []
    for i, (rid, s, m) in enumerate(arch_scores):
        x_end, y_end = axis_pts[i]
        lines_svg.append(f'<line x1="{cx:.1f}" y1="{cy:.1f}" x2="{x_end:.1f}" y2="{y_end:.1f}" '
                         f'stroke="#d1d5db" stroke-width="1"/>')
        # Label positioned slightly beyond the axis end
        ratio_lbl = 1.15
        lx = cx + r_max * ratio_lbl * math.cos(-math.pi/2 + 2*math.pi*i/n)
        ly = cy + r_max * ratio_lbl * math.sin(-math.pi/2 + 2*math.pi*i/n)
        anchor = "middle"
        if lx < cx - 5:
            anchor = "end"
        elif lx > cx + 5:
            anchor = "start"
        labels_svg.append(
            f'<text x="{lx:.1f}" y="{ly:.1f}" text-anchor="{anchor}" '
            f'font-size="11" font-family="sans-serif" fill="#374151">'
            f'{rid} ({s}/{m})</text>'
        )
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" '
        f'viewBox="0 0 {size} {size}">'
        f'{"".join(grid)}'
        f'{"".join(lines_svg)}'
        f'<polygon points="{score_poly}" fill="rgba(34,197,94,0.35)" '
        f'stroke="#16a34a" stroke-width="2"/>'
        f'{"".join(labels_svg)}'
        f'</svg>'
    )


def _architecture_markdown_section(report: dict) -> list[str]:
    """Render the Architecture 23/23 section with a radar SVG + a rule table."""
    arch_keys = ["AR01_event_driven", "AR02_runtime_close", "AR03_unique_api",
                 "AR04_scalable_infra", "AR05_cloud_footprint"]
    rrm = (report.get("green_score", {}) or {}).get("rule_resource_mapping", {}) or {}
    breakdown = (report.get("green_score", {}) or {}).get("breakdown", {}) or {}
    arch_meta = {
        "AR01_event_driven":   ("AR01", "Event-Driven Architecture", 6),
        "AR02_runtime_close":  ("AR02", "Runtime proche du consommateur", 7),
        "AR03_unique_api":     ("AR03", "Une seule API par besoin", 3),
        "AR04_scalable_infra": ("AR04", "Infrastructure scalable", 5),
        "AR05_cloud_footprint":("AR05", "Cloud footprint dashboard", 2),
    }
    scored: list[tuple[str, int, int]] = []
    for k in arch_keys:
        rid, _label, max_pts = arch_meta[k]
        s = int(breakdown.get(k, 0) or rrm.get(k, {}).get("score", 0) or 0)
        scored.append((rid, s, max_pts))
    total = sum(s for _r, s, _m in scored)
    max_total = sum(m for _r, _s, m in scored)
    if max_total == 0:
        return []
    emoji = "🟢" if total == max_total else "🟡" if total >= max_total * 0.5 else "🔴"

    out: list[str] = []
    out.append("")
    out.append("---")
    out.append("")
    out.append(f"## 🏛️ Architecture : **{total}/{max_total}** {emoji}")
    out.append("")
    out.append("> **Ces règles pèsent 23 points** — au même titre que les règles code — "
               "mais sont souvent oubliées. Elles portent sur la topologie de l'API "
               "(événements, edge/CDN, dédup, autoscaling, empreinte cloud).")
    out.append("")
    svg = _radar_svg(scored)
    if svg:
        out.append(svg)
        out.append("")
    out.append("| Statut | Règle | Score | Max | Signaux détectés |")
    out.append("|:------:|-------|------:|----:|------------------|")
    for k in arch_keys:
        rid, label, max_pts = arch_meta[k]
        s = int(breakdown.get(k, 0) or rrm.get(k, {}).get("score", 0) or 0)
        icon = "✅" if s >= max_pts else ("⚠️" if s > 0 else "❌")
        # Try to surface signal_kinds from the rule mapping if present
        signals = []
        entry = rrm.get(k, {}) or {}
        for ev in (entry.get("evidence") or [])[:3]:
            if isinstance(ev, dict):
                signals.append(ev.get("kind", ""))
        sig_str = ", ".join(sorted(set(s for s in signals if s))) or "—"
        out.append(f"| {icon} | **{rid}** {label} | {s} | {max_pts} | {sig_str} |")
    out.append("")
    return out


def _adr_markdown_section(adr_report: dict | None) -> list[str]:
    """Render the ADR compliance section."""
    if not adr_report or not isinstance(adr_report, dict):
        return []
    summ = adr_report.get("summary", {}) or {}
    results = adr_report.get("results", []) or []
    if not results:
        return []
    total = int(summ.get("total", 0))
    accepted = int(summ.get("accepted", 0))
    passed = int(summ.get("passed", 0))
    failed = int(summ.get("failed", 0))
    pct = float(summ.get("score_pct", 0.0))
    icon = "🟢" if failed == 0 else ("🟡" if pct >= 60 else "🔴")

    out: list[str] = []
    out.append("")
    out.append("---")
    out.append("")
    out.append(f"## 📜 ADR compliance : **{passed}/{accepted}** ({pct}%) {icon}")
    out.append("")
    out.append(f"> Total ADR : **{total}** — Acceptés : **{accepted}** — "
               f"Passés : **{passed}** — Échecs : **{failed}** — "
               f"Ignorés (deprecated/proposed) : **{total - accepted}**")
    out.append("")
    out.append("| Statut | ADR | Titre | Règles | Checks passés |")
    out.append("|:------:|:---:|-------|--------|:--------------|")
    for r in results:
        if r.get("skipped"):
            mark = "⏭️"
            checks_str = f"skipped ({r.get('status','')})"
        else:
            mark = "✅" if r.get("ok") else "❌"
            checks = r.get("checks") or []
            ok_n = sum(1 for c in checks if c.get("ok"))
            checks_str = f"{ok_n}/{len(checks)}"
        rules_str = ", ".join(r.get("green_rules") or []) or "—"
        out.append(f"| {mark} | `{r.get('adr','?')}` | {r.get('title','')[:80]} | {rules_str} | {checks_str} |")
    # Detailed failures
    fail_details = [r for r in results
                    if not r.get("skipped") and not r.get("ok")]
    if fail_details:
        out.append("")
        out.append("### ❌ ADR en échec — détail")
        out.append("")
        for r in fail_details:
            out.append(f"#### `{r.get('adr','?')}` — {r.get('title','')}")
            out.append("")
            for c in (r.get("checks") or []):
                if c.get("ok"):
                    continue
                out.append(f"- ❌ **{c.get('kind','?')}** — {c.get('reason','')}")
            out.append("")
    out.append("")
    return out


def generate_markdown(report: dict, *, appname: str = "",
                      creedengo: dict | None = None,
                      adr_report: dict | None = None) -> str:
    """Return a Markdown string representing the Green Score report."""
    gs = report.get("green_score", {})
    total = gs.get("total", 0)
    grade = gs.get("grade", "?")
    breakdown = gs.get("breakdown", {})
    details = gs.get("details", {})
    ts = report.get("timestamp", "")
    measurements = report.get("measurements", {})
    baseline = measurements.get("baseline", {})
    optimized = measurements.get("optimized", {})
    discovery = report.get("auto_discovery", {})
    spectral = report.get("spectral", {})

    emoji = "🟢" if total >= 80 else "🟡" if total >= 50 else "🔴"
    grade_emoji = {"A+": "🏆", "A": "🥇", "B": "🥈", "C": "🥉"}.get(grade, "📉")

    lines: list[str] = []
    a = lines.append

    a("# 🌿 Green API Score Dashboard")
    a("")
    if appname:
        a(f"> 📦 **Application : {appname}**")
        a(">")
    a("> **Summit AXA 2026 — Green Architecture : moins de gras, plus d'impact !**")*")
    a("")
    a(f"📅 *Dernière analyse : {ts}*")
    a("")

    # ── Score hero ──
    a("---")
    a("")
    a(f"## {emoji} Green Score : **{total}/100** — Grade **{grade}** {grade_emoji}")
    a("")

    # ── Breakdown table ──
    a("### 📋 Détail par règle")
    a("")
    a("| Statut | Règle | Score | Max | Endpoints | Détail |")
    a("|:------:|-------|------:|----:|:---------:|--------|")
    rrm_top = gs.get("rule_resource_mapping", {})
    for key, label in LABELS.items():
        score = breakdown.get(key, 0)
        mx = MAX_SCORES.get(key, 0)
        rrmEntry = rrm_top.get(key, {})
        matched = rrmEntry.get("matched_count")
        candidates = rrmEntry.get("candidate_count")
        ep_str = f"{matched}/{candidates}" if matched is not None and candidates is not None else "—"
        icon = "✅" if mx > 0 and score >= mx else "⚠️" if mx > 0 and score > 0 else "❌"
        detail_dict = details.get(key, {})
        note = detail_dict.get("note", "")
        pct = detail_dict.get("reduction_pct")
        detail_str = f"-{pct}%" if pct is not None else note
        a(f"| {icon} | {label} | {score} | {mx} | {ep_str} | {detail_str} |")
    a("")

    # ── Architecture (23 pts) ── rendered at the same visibility level
    # as the "code" breakdown above (radar SVG + table).
    for line in _architecture_markdown_section(report):
        a(line)

    # ── ADR compliance (if adr-report.json provided) ──
    for line in _adr_markdown_section(adr_report):
        a(line)

    # ── Measurements comparison ──
    # ── Measurements table — uses discovered endpoints or legacy fallback ──
    disc_eps_table = discovery.get("discovered_endpoints", [])
    if disc_eps_table:
        a("### 📊 Mesures par endpoint (API découverte)")
        a("")
        a("| Méthode | Endpoint | Taille | Temps | HTTP |")
        a("|:-------:|----------|-------:|------:|-----:|")
        for ep in disc_eps_table[:40]:
            method = ep.get("method", "GET")
            path = ep.get("path", "?")
            sz = ep.get("size_download", 0)
            tt = ep.get("time_total", 0.0)
            code = ep.get("http_code", 0)
            a(f"| {method} | `{path}` | {_fmt_bytes(sz)} | {tt:.3f}s | {code} |")
        if len(disc_eps_table) > 40:
            a(f"| | *… et {len(disc_eps_table) - 40} autres* | | | |")
        a("")
    else:
        # Legacy: show hardcoded measurement keys
        a("### 📊 Mesures (legacy)")
        a("")
        b_full = baseline.get("full_payload", {})
        o_pag = optimized.get("pagination", {})
        o_fields = optimized.get("fields_filter", {})
        o_gzip = optimized.get("gzip_compression", {})
        o_etag = optimized.get("etag_304", {})
        o_delta = optimized.get("delta_changes", {})
        o_range = optimized.get("range_206", {})
        o_cbor = optimized.get("cbor_format", {})
        o_full = optimized.get("full_payload", {})

        a("| Mesure | Taille | Temps | HTTP |")
        a("|--------|-------:|------:|-----:|")
        rows = [
            ("Full payload", b_full if b_full else o_full),
            ("Pagination", o_pag), ("Fields filter", o_fields),
            ("Gzip", o_gzip), ("ETag/304", o_etag),
            ("Delta", o_delta), ("Range 206", o_range),
            ("CBOR", o_cbor),
        ]
        for label, ep in rows:
            if not ep:
                continue
            a(f"| {label} | {_fmt_bytes(ep.get('size_download', 0))} | {ep.get('time_total', 0):.3f}s | {ep.get('http_code', 0)} |")
        a("")

    # ── Key metrics — single API model ──
    a("### 🔑 Métriques clés")
    a("")

    # Energy constants (same as dashboard)
    NET_KWH_PER_GB = 0.06   # The Shift Project
    SERVER_WATTS = 25        # Estimated VM power

    def _energy_network_wh(size_bytes: int) -> float:
        return (size_bytes / (1024**3)) * NET_KWH_PER_GB * 1000

    def _energy_server_wh(time_s: float) -> float:
        return time_s * (SERVER_WATTS / 3600)

    # Compute from discovered endpoints
    disc_eps_energy = discovery.get("discovered_endpoints", [])
    total_bytes = 0
    total_energy_wh = 0.0
    ep_measured = 0
    all_times: list[float] = []

    if disc_eps_energy:
        for ep in disc_eps_energy:
            sz = ep.get("size_download", 0)
            tt = ep.get("time_total", 0.0)
            total_bytes += sz
            total_energy_wh += _energy_network_wh(sz) + _energy_server_wh(tt)
            if tt > 0:
                all_times.append(tt)
            ep_measured += 1
    else:
        # Legacy fallback
        for section in (optimized, baseline):
            for k, v in section.items():
                if isinstance(v, dict) and (v.get("size_download") or v.get("time_total")):
                    sz = v.get("size_download", 0)
                    tt = v.get("time_total", 0.0)
                    total_bytes += sz
                    total_energy_wh += _energy_network_wh(sz) + _energy_server_wh(tt)
                    if tt > 0:
                        all_times.append(tt)
                    ep_measured += 1

    avg_time = sum(all_times) / len(all_times) if all_times else 0
    CO2_G_PER_KWH = 53  # France
    co2_g = (total_energy_wh / 1000) * CO2_G_PER_KWH

    a(f"- **Endpoints mesurés** : {ep_measured}")
    a(f"- **Transfert total** : {_fmt_bytes(total_bytes)}")
    if ep_measured > 0:
        a(f"- **Transfert moyen / endpoint** : {_fmt_bytes(total_bytes // ep_measured)}")
    a(f"- **Temps moyen** : {avg_time:.3f}s")
    a(f"- **⚡ Énergie totale / appel** : {total_energy_wh:.4f} Wh")
    a(f"- **🌍 CO₂ / appel** : {co2_g:.5f} g (France — {CO2_G_PER_KWH} gCO₂/kWh)")
    a("")

    # ── Auto-discovery summary (URL only — endpoint table already shown above) ──
    swagger_url = discovery.get("swagger_url", "")
    if swagger_url:
        a(f"> 🔍 Swagger : `{swagger_url}` — {discovery.get('endpoints_discovered', 0)} endpoints découverts")
        a("")

    # ── Spectral ──
    issues_count = spectral.get("issues_count", 0)
    if issues_count > 0:
        a(f"### 🔬 Spectral Lint ({issues_count} issues)")
        a("")
        sev_map = {0: "❌ error", 1: "⚠️ warn", 2: "ℹ️ info", 3: "💡 hint"}
        issues = spectral.get("issues", [])
        for issue in issues[:25]:
            sev = sev_map.get(issue.get("severity", 3), "?")
            code = issue.get("code", "")
            msg = issue.get("message", "")[:100]
            a(f"- {sev} **[{code}]** {msg}")
        if len(issues) > 25:
            a(f"- *… et {len(issues) - 25} autres*")
        a("")

    # ── Suggestions d'amélioration ──
    rrm = gs.get("rule_resource_mapping", {})
    all_suggestions: list[dict] = []
    rules_with_suggestions: list[dict] = []

    rule_icons = {
        "DE11_pagination": "📄", "DE08_fields": "🔍", "DE01_compression": "🗜️",
        "DE02_DE03_cache": "💾", "DE06_delta": "🔄", "range_206": "✂️",
        "AR02_format_cbor": "📦", "LO01_observability": "👁️", "US07_rate_limit": "🚦",
    }
    rule_display_names = {
        "DE11_pagination": "DE11 — Pagination", "DE08_fields": "DE08 — Filtrage de champs",
        "DE01_compression": "DE01 — Compression Gzip", "DE02_DE03_cache": "DE02/03 — Cache ETag/304",
        "DE06_delta": "DE06 — Delta / Changes", "range_206": "206 — Range / Partial Content",
        "AR02_format_cbor": "AR02 — Format binaire (CBOR)", "LO01_observability": "LO01 — Observabilité",
        "US07_rate_limit": "US07 — Rate Limiting",
    }
    priority_icons = {"high": "🔴 Haute", "medium": "🟡 Moyenne", "low": "⚪ Basse"}

    for rule_key, rule_data in rrm.items():
        suggs = rule_data.get("suggestions", [])
        if not suggs:
            continue
        rules_with_suggestions.append({
            "key": rule_key,
            "icon": rule_icons.get(rule_key, "📌"),
            "name": rule_display_names.get(rule_key, rule_key),
            "description": rule_data.get("description", ""),
            "max_pts": rule_data.get("max_pts", 0),
            "score": rule_data.get("score", 0),
            "validated": rule_data.get("validated", False),
            "matched_count": rule_data.get("matched_count", 0),
            "candidate_count": rule_data.get("candidate_count", 0),
            "suggestions": suggs,
        })
        all_suggestions.extend(suggs)

    if all_suggestions:
        potential_gain = sum(
            max(0, r["max_pts"] - r["score"]) for r in rules_with_suggestions
        )
        potential_score = min(total + potential_gain, gs.get("max", 100))

        a("### 💡 Suggestions d'amélioration")
        a("")
        a(f"> **Score actuel : {total}/{gs.get('max', 100)}** — "
          f"Score potentiel avec toutes les suggestions : **{potential_score}/{gs.get('max', 100)}** "
          f"(+{potential_gain} pts possibles)")
        a("")

        high_count = sum(1 for s in all_suggestions if s.get("priority") == "high")
        medium_count = sum(1 for s in all_suggestions if s.get("priority") == "medium")
        low_count = sum(1 for s in all_suggestions if s.get("priority") == "low")
        a(f"🔴 Haute priorité : {high_count} | "
          f"🟡 Moyenne : {medium_count} | "
          f"⚪ Basse : {low_count} | "
          f"**Total : {len(all_suggestions)} suggestions**")
        a("")

        # Sort: failed first, then partial, then fully passed — by gap descending
        def _sort_key(r):
            rank = 0 if not r["validated"] else (1 if r["matched_count"] < r["candidate_count"] else 2)
            return (rank, -(r["max_pts"] - r["score"]))
        rules_with_suggestions.sort(key=_sort_key)

        for rule in rules_with_suggestions:
            gap = max(0, rule["max_pts"] - rule["score"])
            is_partial = rule["validated"] and rule["matched_count"] < rule["candidate_count"]
            status = "❌ Non validé" if not rule["validated"] else (f"⚠️ Partiel ({rule['matched_count']}/{rule['candidate_count']})" if is_partial else "✅ Validé")
            a(f"#### {rule['icon']} {rule['name']} ({status}"
              f"{f' — +{gap} pts possibles' if gap > 0 else ''})")
            a("")
            a(f"> {rule['description']} "
              f"({rule['matched_count']}/{rule['candidate_count']} endpoints validés)")
            a("")
            a("| Priorité | Cible | Action | Impact |")
            a("|:--------:|-------|--------|--------|")
            for s in rule["suggestions"][:8]:
                prio = priority_icons.get(s.get("priority", "medium"), "🟡 Moyenne")
                target = s.get("target", "").replace("|", "\\|")
                action = s.get("action", "").replace("|", "\\|")
                impact = s.get("impact", "").replace("|", "\\|")
                a(f"| {prio} | `{target}` | {action} | {impact} |")
            if len(rule["suggestions"]) > 8:
                a(f"| | *… et {len(rule['suggestions']) - 8} autres* | | |")
            a("")

            # Show first suggestion's 'how' as a collapsible block
            first_how = next(
                (s.get("how") for s in rule["suggestions"] if s.get("how")), None
            )
            if first_how:
                a("<details><summary>🔧 Comment implémenter</summary>")
                a("")
                a("```")
                a(first_how)
                a("```")
                a("</details>")
                a("")
    else:
        # No suggestions — show congratulations section
        a("### 💡 Suggestions d'amélioration")
        a("")
        max_score = gs.get("max", 100)
        if total >= max_score:
            a("> 🏆 **Score parfait !** Toutes les règles Green API sont validées — bravo !")
        else:
            a(f"> ✅ **Aucune suggestion d'amélioration** — "
              f"Score actuel : **{total}/{max_score}** — "
              f"toutes les règles analysées sont conformes.")
        a("")

    # ── Creedengo eco-design section ──
    if creedengo and creedengo.get("creedengo_score"):
        a(generate_creedengo_markdown(creedengo))

    # ── Footer ──
    a("---")
    a("")
    a("🌿 *API Green Score — [Framework](https://github.com/API-Green-Score/APIGreenScore) | "
      "[Training](https://github.com/API-Green-Score/training-student) | "
      "🌱 [Creedengo](https://github.com/green-code-initiative) | Summit AXA 2026*")
    a("")
    a("> 📊 Pour le dashboard interactif complet, ouvrez [`dashboard/index.html`](index.html)")
    a("")

    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", required=True, help="Path to report JSON")
    parser.add_argument("--template", required=True, help="Path to HTML template")
    parser.add_argument("--output", required=True, help="Path to output HTML")
    parser.add_argument("--creedengo-report", default="", help="Path to Creedengo report JSON (optional)")
    parser.add_argument("--adr-report", default="", help="Path to ADR report JSON (optional)")
    args = parser.parse_args()

    report_path = Path(args.report)
    template_path = Path(args.template)
    output_path = Path(args.output)
    creedengo_path = Path(args.creedengo_report) if args.creedengo_report else None
    adr_path = Path(args.adr_report) if args.adr_report else None

    if not report_path.is_file():
        print(f"Report not found: {report_path}", file=sys.stderr)
        return 1
    report_text = report_path.read_text(encoding="utf-8").strip()
    if not report_text:
        print(f"Report file is empty: {report_path}", file=sys.stderr)
        return 1
    if not template_path.is_file():
        print(f"Template not found: {template_path}", file=sys.stderr)
        return 1

    raw_data = json.loads(report_text)
    template = template_path.read_text(encoding="utf-8")

    if PLACEHOLDER not in template:
        print(f"Placeholder {PLACEHOLDER} not found in template", file=sys.stderr)
        return 1

    # ── Unwrap {appname, report} envelope if present ──
    if "report" in raw_data and "appname" in raw_data:
        appname = raw_data["appname"]
        report = raw_data["report"]
    else:
        appname = ""
        report = raw_data

    # ── Generate HTML — embed the full envelope (or flat report) ──
    embedded = json.dumps(raw_data, ensure_ascii=True)
    output = template.replace(PLACEHOLDER, embedded)

    # ── Embed Creedengo report if available ──
    if creedengo_path and creedengo_path.is_file():
        creedengo_text = creedengo_path.read_text(encoding="utf-8").strip()
        if creedengo_text:
            creedengo_data = json.loads(creedengo_text)
            creedengo_embedded = json.dumps(creedengo_data, ensure_ascii=True)
            output = output.replace(CREEDENGO_PLACEHOLDER, creedengo_embedded)
            print(f"Creedengo report embedded from {creedengo_path}")
        else:
            output = output.replace(CREEDENGO_PLACEHOLDER, "null")
    else:
        output = output.replace(CREEDENGO_PLACEHOLDER, "null")

    # ── Embed ADR report if available (optional; template may not have placeholder) ──
    adr_data = None
    if adr_path and adr_path.is_file():
        adr_text = adr_path.read_text(encoding="utf-8").strip()
        if adr_text:
            try:
                adr_data = json.loads(adr_text)
            except Exception:
                adr_data = None
    if ADR_PLACEHOLDER in output:
        output = output.replace(
            ADR_PLACEHOLDER,
            json.dumps(adr_data, ensure_ascii=True) if adr_data else "null",
        )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(output, encoding="utf-8")
    print(f"Dashboard written to {output_path}")

    # ── Generate Markdown (same directory as HTML, named index.md) ──
    md_path = output_path.parent / "index.md"
    creedengo_data_md = None
    if creedengo_path and creedengo_path.is_file():
        try:
            creedengo_data_md = json.loads(creedengo_path.read_text(encoding="utf-8").strip())
        except Exception:
            pass
    md_content = generate_markdown(report, appname=appname,
                                   creedengo=creedengo_data_md,
                                   adr_report=adr_data)
    md_path.write_text(md_content, encoding="utf-8")
    print(f"Markdown dashboard written to {md_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

