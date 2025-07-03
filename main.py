from fastapi import FastAPI, Form
from fastapi.responses import StreamingResponse, JSONResponse
from weasyprint import HTML
import io

app = FastAPI()

@app.post("/convert-html-to-pdf/")
async def convert_html_to_pdf(html: str = Form(...)):
    try:
        pdf_io = io.BytesIO()
        HTML(string=html).write_pdf(pdf_io)
        pdf_io.seek(0)

        return StreamingResponse(
            pdf_io,
            media_type="application/pdf",
            headers={"Content-Disposition": "attachment; filename=validation_report.pdf"}
        )
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
