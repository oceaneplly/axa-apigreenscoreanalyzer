#!/usr/bin/env python3
"""
sobriit_sender.py
─────────────────
Standalone module that sends Green API Score and Creedengo analysis results
to the SobriIT platform via its REST API.

Configuration (environment variables):
  SOBRIIT_BASE_URL   Base URL of the SobriIT API (e.g. https://sobriit.example.com)
  SOBRIIT_API_KEY    API key for authentication (sent as X-API-Key header)

  Application metadata (optional, used when creating a new application):
    SOBRIIT_APP_CODE        Application code (defaults to appname)
    SOBRIIT_APP_DSI         DSI name
    SOBRIIT_APP_TRIBE       Tribe name
    SOBRIIT_APP_TRIBE_ID    Tribe UUID

These can also be passed as function parameters (override env vars).

Usage from Python:
    from sobriit_sender import send_to_sobriit
    result = send_to_sobriit(appname, green_report_dict, creedengo_report_dict)

Usage from CLI (for shell script integration):
    python3 scripts/sobriit_sender.py \\
        --appname myapp \\
        --green-report reports/latest-report.json \\
        --creedengo-report reports/creedengo-report.json \\
        [--base-url https://sobriit.example.com] \\
        [--api-key xxx] \\
        [--app-code CODE] \\
        [--app-dsi DSI] \\
        [--app-tribe TRIBE] \\
        [--app-tribe-id UUID]
    Exit code 0 = success, 1 = failure (non-blocking by design).
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path


# ─── HTTP helpers (stdlib only) ──────────────────────────────────────────────

def _api_call(method: str, url: str, api_key: str,
              body: dict | None = None, timeout: int = 15) -> tuple[int, dict | str]:
    """Perform an HTTP request to SobriIT. Returns (status_code, parsed_json_or_text)."""
    headers = {
        "X-API-Key": api_key,
        "Accept": "application/json",
    }
    data = None
    if body is not None:
        headers["Content-Type"] = "application/json; charset=utf-8"
        data = json.dumps(body, ensure_ascii=False).encode("utf-8")

    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read()
            try:
                return resp.status, json.loads(raw)
            except Exception:
                return resp.status, raw.decode("utf-8", errors="replace")
    except urllib.error.HTTPError as e:
        raw = e.read() if e.fp else b""
        try:
            return e.code, json.loads(raw)
        except Exception:
            return e.code, raw.decode("utf-8", errors="replace")
    except Exception as exc:
        # Connection-level failures (DNS, refused, socket permission denied…)
        # surface as status 0. WinError 10013 ("socket access forbidden") on
        # Windows usually means nothing is listening on the target host/port,
        # the port is in a Windows-reserved/excluded range, or a firewall/proxy
        # blocks it. Make that actionable instead of a raw stack string.
        hint = ""
        text = str(exc)
        if "10013" in text or "forbidden by its access permissions" in text:
            hint = (
                f" — impossible de joindre '{url}'. Vérifiez SOBRIIT_BASE_URL "
                "(--sobriit-base-url) : l'hôte/port n'écoute pas, est réservé "
                "par Windows, ou est bloqué par un firewall/proxy."
            )
        return 0, f"{text}{hint}"


def _log(msg: str) -> None:
    """Emit a progress/trace line to stderr so the caller can verify that the
    build and report were actually sent to SobriIT."""
    print(msg, file=sys.stderr, flush=True)


def _extract_id(resp) -> str | int | None:
    """Extract an entity id from a SobriIT response.

    SobriIT may return the created entity either flat ({"id": ...}) or wrapped
    in a {"data": {"id": ...}} / {"data": [{"id": ...}]} envelope. We check all
    of these so a successful build/report is never treated as a silent failure
    just because of the response shape."""
    if isinstance(resp, dict):
        if resp.get("id"):
            return resp["id"]
        data = resp.get("data")
        if isinstance(data, dict) and data.get("id"):
            return data["id"]
        if isinstance(data, list) and data and isinstance(data[0], dict) and data[0].get("id"):
            return data[0]["id"]
    return None


def _json_str(obj) -> str | None:
    """Serialize obj to a JSON string, or None if obj is None/empty."""
    if obj is None:
        return None
    if isinstance(obj, str):
        return obj if obj.strip() else None
    try:
        return json.dumps(obj, ensure_ascii=False)
    except Exception:
        return str(obj)


# ─── Main send function ─────────────────────────────────────────────────────

def send_to_sobriit(
    appname: str,
    green_report: dict | None = None,
    creedengo_report: dict | None = None,
    base_url: str | None = None,
    api_key: str | None = None,
    app_code: str | None = None,
    app_dsi: str | None = None,
    app_tribe: str | None = None,
    app_tribe_id: str | None = None,
) -> dict:
    """
    Send analysis results to SobriIT.

    Flow:
      1. GET /api/v1/applications/by-name/{appname} → lookup existing app
         If 404 → POST /api/v1/applications to create it
      2. POST /api/v1/builds → create a build linked to the application
      3. POST /api/v1/reports/greenapibackend → create the detailed report

    Returns a status dict:
      {"ok": True/False, "applicationId": ..., "buildId": ..., "reportId": ..., "error": ...}
    """
    base_url = (base_url or os.environ.get("SOBRIIT_BASE_URL", "")).rstrip("/") or "http://localhost:8080"
    api_key = api_key or os.environ.get("SOBRIIT_API_KEY", "") or "U2kgdm91cyBuZSBwb3V2ZXogcGFzIGxlIG1lc3VyZXIsIHZvdXMgbmUgcG91dmV6IHBhcyBsJ2Ftw6lsaW9yZXIu"
    app_code = app_code or os.environ.get("SOBRIIT_APP_CODE", "") or appname
    app_dsi = app_dsi or os.environ.get("SOBRIIT_APP_DSI", "") or "DSI IARD ET PARTENARIATS"
    app_tribe = app_tribe or os.environ.get("SOBRIIT_APP_TRIBE", "") or "TRIBU IARD PARTICULIERS"
    app_tribe_id = app_tribe_id or os.environ.get("SOBRIIT_APP_TRIBE_ID", "") or "C954FAC2-AEAC-41D4-A4FF-D958DC3FD3B3"

    if not base_url:
        return {"ok": False, "error": "SOBRIIT_BASE_URL not configured"}
    if not api_key:
        return {"ok": False, "error": "SOBRIIT_API_KEY not configured"}
    if not appname:
        return {"ok": False, "error": "appname is required"}
    if not green_report and not creedengo_report:
        return {"ok": False, "error": "no report data to send"}

    # ── Extract green score data ──
    gs = {}
    report_section = {}
    if green_report:
        report_section = green_report.get("report") or {}
        gs = report_section.get("green_score") or {}

    green_total = gs.get("total")
    green_max = gs.get("max")
    green_grade = gs.get("grade")
    score_normalised = round(green_total / green_max * 100, 2) if green_total and green_max else None
    report_timestamp = report_section.get("timestamp")

    # ── Extract creedengo data ──
    cs = {}
    if creedengo_report:
        cs = creedengo_report.get("creedengo_score") or {}

    # ── Step 1: Lookup or create application ──
    app_id = None
    quoted = urllib.request.quote(appname, safe='')
    _log(f"→ [SobriIT] Base URL: {base_url}")
    _log(f"→ [SobriIT] Step 1/3: resolving application '{appname}' …")

    # Try lookup by name first, then by code via the search endpoint
    for search_field in ("name", "code"):
        status, resp = _api_call(
            "GET",
            f"{base_url}/api/v1/applications/search?{search_field}={quoted}",
            api_key,
        )
        if status == 200 and isinstance(resp, dict):
            items = resp.get("data") or []
            # Exact match (search may return partial matches)
            for item in items:
                if isinstance(item, dict) and item.get("id"):
                    val = (item.get(search_field) or "").strip()
                    if val.lower() == appname.lower():
                        app_id = item["id"]
                        break
            if app_id:
                break

    # Also try the direct by-name endpoint as fallback
    if not app_id:
        status, resp = _api_call(
            "GET",
            f"{base_url}/api/v1/applications/by-name/{quoted}",
            api_key,
        )
        if status == 200:
            app_id = _extract_id(resp)

    # If still not found, create the application with all available fields
    if app_id:
        _log(f"✓ [SobriIT] Application found: {app_id}")
    else:
        app_payload = {
            "name": appname,
            "code": app_code,
            "dsi": app_dsi,
            "tribe": app_tribe,
            "tribeId": app_tribe_id,
            "globalScore": score_normalised or 0.0,
            "performance": 0.0,
            "accessibility": 0.0,
            "bestPractices": 0.0,
            "ecoindex": 0.0,
            "bestPracticesCnumr": round(cs.get("total", 0) / cs.get("max", 100) * 100, 2) if cs.get("max") else 0.0,
            "accessibilityAxeCore": 0.0,
            "greenApiScore": score_normalised or 0.0,
            "greenBackendScore": 0.0,
        }
        # Remove None values
        app_payload = {k: v for k, v in app_payload.items() if v is not None}

        status, resp = _api_call("POST", f"{base_url}/api/v1/applications", api_key, body=app_payload)
        app_id = _extract_id(resp) if status in (200, 201) else None
        if app_id:
            _log(f"✓ [SobriIT] Application created: {app_id}")
        else:
            _log(f"✗ [SobriIT] Failed to create application (HTTP {status})")
            return {"ok": False, "error": f"failed to create application (HTTP {status}): {resp}"}

    # ── Step 2: Create build ──
    _log("→ [SobriIT] Step 2/3: creating build …")
    build_payload = {
        "applicationId": app_id,
        "tag": report_timestamp or "",
        "globalScore": score_normalised or 0.0,
        "performance": 0.0,
        "accessibility": 0.0,
        "bestPractices": 0.0,
        "ecoindex": 0.0,
        "bestPracticesCnumr": round(cs.get("total", 0) / cs.get("max", 100) * 100, 2) if cs.get("max") else 0.0,
        "accessibilityAxeCore": 0.0,
        "greenApiScore": score_normalised or 0.0,
        "greenBackendScore": 0.0,
    }
    status, resp = _api_call("POST", f"{base_url}/api/v1/builds", api_key, body=build_payload)
    build_id = _extract_id(resp) if status in (200, 201) else None
    if not build_id:
        _log(f"✗ [SobriIT] Failed to create build (HTTP {status}): {resp}")
        return {
            "ok": False,
            "applicationId": app_id,
            "error": f"failed to create build (HTTP {status}): {resp}",
        }
    _log(f"✓ [SobriIT] Build created: {build_id}")

    # ── Step 3: Create GreenApiBackendReport ──
    _log("→ [SobriIT] Step 3/3: creating GreenApiBackend report …")
    report_payload = {
        "buildId": build_id,
        "appName": appname,
        "reportTimestamp": report_timestamp,
        # Green Score fields
        "greenApiScoreTotal": green_total,
        "greenApiScoreMax": green_max,
        "greenApiGrade": green_grade,
        "scoreNormalised100": score_normalised,
        "greenScoreBreakdownJson": _json_str(gs.get("breakdown")),
        "ruleResourceMappingJson": _json_str(gs.get("rule_resource_mapping")),
        "greenScoreDetailsJson": _json_str(gs.get("details")),
        "endpointRulesJson": _json_str(report_section.get("endpoint_rules")),
        "totalsJson": _json_str(report_section.get("totals")),
        "endpointsJson": _json_str(report_section.get("endpoints")),
        "measurementsJson": _json_str(report_section.get("measurements")),
        "autoDiscoveryJson": _json_str(report_section.get("auto_discovery")),
        # Creedengo fields
        "creedengoScoreTotal": cs.get("total"),
        "creedengoScoreMax": cs.get("max"),
        "creedengoGrade": cs.get("grade"),
        "creedengoIssuesCount": cs.get("issues_count"),
        "creedengoTotalEffortMinutes": cs.get("total_effort_minutes"),
        "creedengoLanguage": creedengo_report.get("language") if creedengo_report else None,
        "creedengoProject": creedengo_report.get("project") if creedengo_report else None,
        "creedengoSeverityJson": _json_str(cs.get("severity_breakdown")),
        "creedengoMeasuresJson": _json_str(creedengo_report.get("measures")) if creedengo_report else None,
        "creedengoRulesSummaryJson": _json_str(creedengo_report.get("rules_summary")) if creedengo_report else None,
        "creedengoCategoriesJson": _json_str(creedengo_report.get("categories")) if creedengo_report else None,
        "creedengoTopFilesJson": _json_str(creedengo_report.get("top_files")) if creedengo_report else None,
        "creedengoIssuesJson": _json_str(creedengo_report.get("issues")) if creedengo_report else None,
        "sonarIssuesJson": _json_str(creedengo_report.get("sonar_issues")) if creedengo_report else None,
        "creedengoDetectionJson": _json_str(creedengo_report.get("detection")) if creedengo_report else None,
    }

    # Remove None values (SobriIT accepts nullable but cleaner without)
    report_payload = {k: v for k, v in report_payload.items() if v is not None}

    status, resp = _api_call(
        "POST", f"{base_url}/api/v1/reports/greenapibackend", api_key, body=report_payload
    )
    if status not in (200, 201):
        _log(f"✗ [SobriIT] Failed to create report (HTTP {status}): {resp}")
        return {
            "ok": False,
            "applicationId": app_id,
            "buildId": build_id,
            "error": f"failed to create report (HTTP {status}): {resp}",
        }

    report_id = _extract_id(resp)
    _log(f"✓ [SobriIT] Report created: {report_id or '(id non renvoyé)'}")
    _log(f"✓ [SobriIT] Done — application={app_id}, build={build_id}, report={report_id}")
    return {
        "ok": True,
        "applicationId": app_id,
        "buildId": build_id,
        "reportId": report_id,
    }


# ─── CLI entry point (for shell script integration) ─────────────────────────

def main():
    p = argparse.ArgumentParser(description="Send analysis results to SobriIT")
    p.add_argument("--appname", required=True, help="Application name")
    p.add_argument("--green-report", help="Path to latest-report.json")
    p.add_argument("--creedengo-report", help="Path to creedengo-report.json")
    p.add_argument("--base-url", default=None, help="SobriIT base URL (or SOBRIIT_BASE_URL env)")
    p.add_argument("--api-key", default=None, help="SobriIT API key (or SOBRIIT_API_KEY env)")
    p.add_argument("--app-code", default=None, help="Application code (or SOBRIIT_APP_CODE env, defaults to appname)")
    p.add_argument("--app-dsi", default=None, help="DSI name (or SOBRIIT_APP_DSI env)")
    p.add_argument("--app-tribe", default=None, help="Tribe name (or SOBRIIT_APP_TRIBE env)")
    p.add_argument("--app-tribe-id", default=None, help="Tribe UUID (or SOBRIIT_APP_TRIBE_ID env)")
    args = p.parse_args()

    green_report = None
    if args.green_report:
        fp = Path(args.green_report)
        if fp.is_file():
            with fp.open("r", encoding="utf-8") as f:
                green_report = json.load(f)
        else:
            print(f"⚠ Green report not found: {args.green_report}", file=sys.stderr)

    creedengo_report = None
    if args.creedengo_report:
        fp = Path(args.creedengo_report)
        if fp.is_file():
            with fp.open("r", encoding="utf-8") as f:
                creedengo_report = json.load(f)
        else:
            print(f"⚠ Creedengo report not found: {args.creedengo_report}", file=sys.stderr)

    if not green_report and not creedengo_report:
        print("❌ No report files found — nothing to send.", file=sys.stderr)
        sys.exit(1)

    result = send_to_sobriit(
        appname=args.appname,
        green_report=green_report,
        creedengo_report=creedengo_report,
        base_url=args.base_url,
        api_key=args.api_key,
        app_code=args.app_code,
        app_dsi=args.app_dsi,
        app_tribe=args.app_tribe,
        app_tribe_id=args.app_tribe_id,
    )

    print(json.dumps(result, indent=2, ensure_ascii=False))
    sys.exit(0 if result.get("ok") else 1)


if __name__ == "__main__":
    main()

