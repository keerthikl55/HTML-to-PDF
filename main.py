from fastapi import FastAPI, Form
from fastapi.responses import StreamingResponse, JSONResponse
from weasyprint import HTML
import io
import os

app = FastAPI()

def replace_emojis_with_local_images(html: str) -> str:
    base_path = os.path.abspath("emoji")
    emoji_map = {
        "✅": f'<img src="file://{base_path}/check.png" width="18" style="vertical-align: middle;">',
        "❌": f'<img src="file://{base_path}/cross.png" width="18" style="vertical-align: middle;">',
        "📋": f'<img src="file://{base_path}/report.png" width="20" style="vertical-align: middle;">',
        "ℹ️": f'<img src="file://{base_path}/info.png" width="18" style="vertical-align: middle;">',
    }
    for emoji, img_tag in emoji_map.items():
        html = html.replace(emoji, img_tag)
    return html

@app.post("/convert-html-to-pdf/")
async def convert_html_to_pdf(html: str = Form(...)):
    try:
        modified_html = replace_emojis_with_local_images(html)

        pdf_io = io.BytesIO()
        HTML(string=modified_html).write_pdf(pdf_io)
        pdf_io.seek(0)

        return StreamingResponse(
            pdf_io,
            media_type="application/pdf",
            headers={"Content-Disposition": "attachment; filename=validation_report.pdf"}
        )
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
