from fastapi import FastAPI, Request, UploadFile, File, Form
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
import shutil
import os
from datetime import datetime

# Your existing imports
from pdf_utils import extract_text_from_pdf, render_resume_to_pdf, generate_cover_letter_pdf
from llm_refiner import refine_resume, generate_cover_letter

app = FastAPI(title="ResumeFlow")

UPLOAD_DIR = "uploads"
OUTPUT_DIR = "output"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Enable Jinja2 templates
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )


# Keep your existing endpoints (just showing them for completeness)
@app.post("/optimize/")
async def optimize_resume(
    resume: UploadFile = File(...),
    job_description: str = Form(None)
):
    # ... your existing code ...
    pass  # keep as is


@app.post("/generate-cover/")
async def generate_cover(
    resume: UploadFile = File(...),
    job_description: str = Form(...),
    full_name: str = Form("Ken Kaibe"),
    contact_info: str = Form("+254 740 413 951 | mukabiken@gmail.com | Mombasa")
):
    # ... your existing code ...
    pass  # keep as is