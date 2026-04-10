import json
import subprocess
import sys
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI(title="Document Gate UI")

BASE_DIR = Path(__file__).resolve().parents[1]
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
DEFAULT_REPORT_PATH = BASE_DIR / "reports" / "doa_document_gate_run_001.json"
GATE_SCRIPT_PATH = BASE_DIR / "scripts" / "doa_document_gate.py"


@app.get("/", response_class=HTMLResponse)
def index(request: Request) -> HTMLResponse:
    context = {
        "request": request,
        "status": "No run yet",
        "gate_status": None,
        "counts": None,
        "findings": [],
        "report_path": str(DEFAULT_REPORT_PATH),
        "error": None,
    }
    return templates.TemplateResponse("document_gate/index.html", context)


@app.post("/run", response_class=HTMLResponse)
def run_gate(request: Request) -> HTMLResponse:
    # Thin shell only: call existing gate script and read generated report.
    context = {
        "request": request,
        "status": "Run failed",
        "gate_status": None,
        "counts": None,
        "findings": [],
        "report_path": str(DEFAULT_REPORT_PATH),
        "error": None,
    }

    cmd = [
        sys.executable,
        str(GATE_SCRIPT_PATH),
        "--root",
        str(BASE_DIR),
        "--out",
        str(DEFAULT_REPORT_PATH),
        "--dry-run",
    ]

    try:
        proc = subprocess.run(
            cmd,
            cwd=str(BASE_DIR),
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=False,
        )
    except OSError as exc:
        context["error"] = f"Failed to start gate subprocess: {exc}"
        return templates.TemplateResponse("document_gate/index.html", context)

    if proc.returncode != 0:
        stderr = proc.stderr.strip() or "(no stderr)"
        context["error"] = f"Gate subprocess exited with code {proc.returncode}: {stderr}"
        return templates.TemplateResponse("document_gate/index.html", context)

    if not DEFAULT_REPORT_PATH.is_file():
        context["error"] = f"Gate report not found: {DEFAULT_REPORT_PATH}"
        return templates.TemplateResponse("document_gate/index.html", context)

    try:
        report = json.loads(DEFAULT_REPORT_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        context["error"] = f"Invalid gate report JSON: {exc}"
        return templates.TemplateResponse("document_gate/index.html", context)
    except OSError as exc:
        context["error"] = f"Failed to read gate report: {exc}"
        return templates.TemplateResponse("document_gate/index.html", context)

    context["status"] = "Run completed"
    context["gate_status"] = report.get("gate_status")
    context["counts"] = report.get("counts") or {}
    context["findings"] = report.get("findings") or []
    return templates.TemplateResponse("document_gate/index.html", context)

