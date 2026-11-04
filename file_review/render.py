"""Self-contained offline HTML; source contents never enter the report."""

import json
from pathlib import Path
from .briefing import briefing, introduction, priority


def render(report):
    report = dict(report, briefing=briefing(report), guidance=introduction(report),
                  default_rows=sorted(range(len(report["rows"])), key=lambda i: priority(report["rows"][i]))[:12])
    assets = Path(__file__).parent
    template = (assets / "report.html").read_text(encoding="utf-8")
    # JSON stays inert even when a repository filename contains HTML markup.
    payload = json.dumps(report, ensure_ascii=True).replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")
    return template.replace("/* STYLE */", (assets / "report.css").read_text()).replace(
        "/* SCRIPT */", (assets / "report.js").read_text()).replace("REPORT_DATA", payload)
