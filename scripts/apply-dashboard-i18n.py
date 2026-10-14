#!/usr/bin/env python

"""Make ``dashboard/index.save.html`` bilingual (French by default / English).

The i18n engine + FR→EN dictionary live in ``dashboard/i18n.partial.html``,
which is the single source of truth. This script injects (or refreshes) that
block inside the dashboard template between the ``I18N:BEGIN`` / ``I18N:END``
markers, so updating a translation is a one-liner in the partial followed by::

    python scripts/apply-dashboard-i18n.py
    bash scripts/generate-dashboard.sh      # regenerate dashboard/index.html

The script is idempotent and safe to run repeatedly.

What it does
------------
1. Injects/refreshes the i18n engine just before ``</head>``.
2. Adds the ``.lang-switcher`` CSS and makes ``.header`` positioned.
3. Inserts the FR / EN toggle at the top of the ``.header`` block.
4. Swaps the hard-coded ``'fr-FR'`` locale for the dynamic ``I18N.locale``.
5. Wraps imperative strings (alert / confirm / prompt / canvas) with ``t()``.
6. Re-renders the canvas charts when the language changes.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

BEGIN = "<!-- I18N:BEGIN -->"
END = "<!-- I18N:END -->"

SWITCHER_CSS = """
        /* ─── i18n language switcher ─────────────────────────────── */
        .lang-switcher {
            position: absolute; top: 0; right: 0;
            display: inline-flex;
            border: 1px solid var(--gray-600); border-radius: 999px;
            overflow: hidden; background: rgba(31,41,55,0.85);
            z-index: 50;
        }
        .lang-switcher button {
            background: none; border: none; cursor: pointer;
            color: var(--gray-400); font-size: 0.75rem; font-weight: 700;
            padding: 5px 13px; letter-spacing: 0.04em;
            transition: background 0.15s, color 0.15s;
        }
        .lang-switcher button:hover { color: var(--green-200); }
        .lang-switcher button.active { background: var(--green-700); color: #fff; }
        @media (max-width: 900px) {
            .lang-switcher { position: static; margin: 0 auto 10px; }
        }
"""

SWITCHER_HTML = """        <div class="lang-switcher" role="group" aria-label="Language / Langue">
            <button type="button" data-lang="fr" class="active" lang="fr" title="Français">FR</button>
            <button type="button" data-lang="en" lang="en" title="English">EN</button>
        </div>
"""

CHART_HOOK = """
// ─── i18n: canvas charts are not reachable by the DOM translator,
//     so re-render them (and the computed Creedengo panel) on switch ───
document.addEventListener('i18n:changed', () => {
    if (history.length > 0) { renderHistory(); renderEnergyHistory(); renderCO2History(); }
    if (typeof creedengoReport !== 'undefined' && creedengoReport) {
        renderCreedengoEnvImpact(creedengoReport);
    }
});
"""

# (old, new) imperative-string replacements — applied only when still present
IMPERATIVE_PATCHES: list[tuple[str, str]] = [
    ("alert('Erreur de parsing JSON Creedengo: ' + err.message);",
     "alert(t('Erreur de parsing JSON Creedengo: ') + err.message);"),
    ("alert('Erreur de parsing JSON: ' + err.message);",
     "alert(t('Erreur de parsing JSON: ') + err.message);"),
    ("alert('Erreur: ' + err.message)",
     "alert(t('Erreur: ') + err.message)"),
    ("prompt('URL du rapport JSON:', 'reports/latest-report.json')",
     "prompt(t('URL du rapport JSON:'), 'reports/latest-report.json')"),
    ("confirm('Supprimer tout l\\'historique (toutes les apps) ?')",
     "confirm(t('Supprimer tout l\\'historique (toutes les apps) ?'))"),
    ("alert('Export PNG indisponible. Vérifiez votre connexion réseau.');",
     "alert(t('Export PNG indisponible. Vérifiez votre connexion réseau.'));"),
    ("confirm(`Supprimer tout l'historique de l'app \"${currentAppname}\" ?`)",
     "confirm(t(\"Supprimer tout l'historique de l'app\") + ` \"${currentAppname}\" ?`)"),
    ("ctx.fillText('Énergie (Wh)', 0, 0);",
     "ctx.fillText(t('Énergie (Wh)'), 0, 0);"),
]

HEADER_CSS_OLD = (
    "        .header {\n"
    "            text-align: center;\n"
    "            margin-bottom: 24px;\n"
    "        }"
)
HEADER_CSS_NEW = (
    "        .header {\n"
    "            text-align: center;\n"
    "            margin-bottom: 24px;\n"
    "            position: relative;\n"
    "        }"
)


def patch(template: Path, partial: Path) -> int:
    html = template.read_text(encoding="utf-8")
    block = partial.read_text(encoding="utf-8").strip("\n")
    if BEGIN not in block:
        block = f"{BEGIN}\n{block}\n{END}"

    changed = False

    # 1. i18n engine — inject or refresh between the markers
    if BEGIN in html and END in html:
        head, rest = html.split(BEGIN, 1)
        _old, tail = rest.split(END, 1)
        new_html = head + block + tail
        if new_html != html:
            html, changed = new_html, True
            print("↻ i18n block refreshed from the partial")
    else:
        html = html.replace("</head>", block + "\n</head>", 1)
        changed = True
        print("+ i18n block injected before </head>")

    # 2. CSS — switcher + positioned header
    if ".lang-switcher {" not in html.split(BEGIN)[0]:
        html = html.replace(HEADER_CSS_OLD, HEADER_CSS_NEW, 1)
        html = html.replace("    </style>", SWITCHER_CSS + "    </style>", 1)
        changed = True
        print("+ language switcher styles added")

    # 3. Language toggle at the top of the header
    if 'class="lang-switcher"' not in html.split("<body>")[-1]:
        html = html.replace(
            '<body>\n    <div class="header">\n',
            '<body>\n    <div class="header">\n' + SWITCHER_HTML,
            1,
        )
        changed = True
        print("+ FR/EN toggle added to the header")

    # 4. Dynamic locale for number formatting
    if ".toLocaleString('fr-FR')" in html:
        html = html.replace(".toLocaleString('fr-FR')", ".toLocaleString(I18N.locale)")
        changed = True
        print("+ 'fr-FR' locale made dynamic")

    # 5. Imperative strings
    for old, new in IMPERATIVE_PATCHES:
        if old in html:
            html = html.replace(old, new)
            changed = True
            print(f"+ wrapped with t(): {old[:52]}…")

    # 6. Re-render canvas charts on language change
    if "i18n:changed" not in html.split(END)[-1]:
        html = html.replace("</script>\n</body>", CHART_HOOK + "</script>\n</body>", 1)
        changed = True
        print("+ chart re-render hook added")

    if not changed:
        print(f"✓ {template.name} already up to date — nothing to do")
        return 0

    template.write_text(html, encoding="utf-8")
    print(f"✓ {template} is bilingual (FR default / EN)")
    return 0


def main() -> int:
    template = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "dashboard" / "index.save.html"
    partial = Path(sys.argv[2]) if len(sys.argv) > 2 else ROOT / "dashboard" / "i18n.partial.html"
    if not template.is_file():
        print(f"Template not found: {template}", file=sys.stderr)
        return 1
    if not partial.is_file():
        print(f"i18n partial not found: {partial}", file=sys.stderr)
        return 1
    return patch(template, partial)


if __name__ == "__main__":
    raise SystemExit(main())

