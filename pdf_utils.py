import pdfplumber
from weasyprint import HTML
from jinja2 import Environment, FileSystemLoader, select_autoescape
from pathlib import Path

# Jinja2 environment – looks in the 'templates' folder next to this file
env = Environment(
    loader=FileSystemLoader(Path(__file__).parent / "templates"),
    autoescape=select_autoescape(['html', 'xml'])
)


def extract_text_from_pdf(filepath: str) -> str:
    """Extract plain text from PDF using pdfplumber"""
    text = ""
    try:
        with pdfplumber.open(filepath) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n\n"
    except Exception as e:
        print(f"Extraction error: {e}")
    return text.strip()


def render_resume_to_pdf(structured_data: dict, output_path: str):
    print("Rendering PDF with data keys:", list(structured_data.keys()))  # debug

    if "error" in structured_data:
        print("Error in data:", structured_data["error"])
        # Optional: generate a fallback PDF with error message
        error_html = f"<h1>Error</h1><p>{structured_data['error']}</p>"
        HTML(string=error_html).write_pdf(output_path)
        return

    template = env.get_template("resume.html")
    data = { ... }  # your existing defaults

    print("Template data has education items:", len(data["education"]))
    print("Experience items:", len(data["experience"]))

    html_content = template.render(**data)
    print("Generated HTML length:", len(html_content))  # if 0 or very small → template broken

    HTML(string=html_content).write_pdf(output_path)
    print(f"PDF written to: {output_path}")

def generate_cover_letter_pdf(cover_text: str, output_path: str, full_name: str = "Ken Kaibe"):
    """Simple cover letter PDF"""
    html = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 2.5cm 2cm; line-height: 1.6; font-size: 11pt; }}
            h1 {{ text-align: center; margin-bottom: 1.5cm; color: #004080; }}
        </style>
    </head>
    <body>
        <h1>{full_name.upper()}</h1>
        <div style="white-space: pre-wrap;">{cover_text}</div>
    </body>
    </html>
    """
    HTML(string=html).write_pdf(output_path)