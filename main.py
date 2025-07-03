from fastapi import FastAPI, Form
from fastapi.responses import StreamingResponse, JSONResponse
from weasyprint import HTML
import io
import re

app = FastAPI()

def replace_emojis_with_images(html: str) -> str:
    emoji_map = {
        "✅": '<img src="https://twemoji.maxcdn.com/v/latest/72x72/2705.png" width="18" style="vertical-align: middle;"/>',
        "❌": '<img src="https://twemoji.maxcdn.com/v/latest/72x72/274c.png" width="18" style="vertical-align: middle;"/>',
        "📋": '<img src="https://twemoji.maxcdn.com/v/latest/72x72/1f4cb.png" width="20" style="vertical-align: middle;"/>',
        "ℹ️": '<img src="https://twemoji.maxcdn.com/v/latest/72x72/2139.png" width="18" style="vertical-align: middle;"/>',
    }
    for emoji, img_tag in emoji_map.items():
        html = html.replace(emoji, img_tag)
    return html

@app.post("/convert-html-to-pdf/")
async def convert_html_to_pdf(html: str = Form(...)):
    try:
        modified_html = replace_emojis_with_images(html)

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
