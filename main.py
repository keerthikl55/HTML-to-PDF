from fastapi import FastAPI, Form
from fastapi.responses import StreamingResponse, JSONResponse
from weasyprint import HTML, CSS
import io
import os

app = FastAPI()

@app.post("/convert-html-to-pdf/")
async def convert_html_to_pdf(html: str = Form(...)):
    try:
        pdf_io = io.BytesIO()

        # Load the emoji-compatible font CSS
        css = CSS(string=f"""
            @font-face {{
                font-family: 'Noto Color Emoji';
                src: url('file://{os.path.abspath("NotoColorEmoji.ttf")}');
            }}
            body {{
                font-family: 'Arial', 'Noto Color Emoji', sans-serif;
            }}
        """)

        HTML(string=html).write_pdf(pdf_io, stylesheets=[css])
        pdf_io.seek(0)

        return StreamingResponse(
            pdf_io,
            media_type="application/pdf",
            headers={"Content-Disposition": "attachment; filename=validation_report.pdf"}
        )
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
