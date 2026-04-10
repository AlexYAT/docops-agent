from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI(title="Document Gate UI")

BASE_DIR = Path(__file__).resolve().parents[1]
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


@app.get("/", response_class=HTMLResponse)
def index(request: Request) -> HTMLResponse:
    # Subprocess integration with doa_document_gate.py will be added next.
    context = {
        "request": request,
        "status": "No run yet",
    }
    return templates.TemplateResponse("document_gate/index.html", context)

