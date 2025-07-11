from fastapi import FastAPI, Form
from fastapi.responses import StreamingResponse
from weasyprint import HTML
import tempfile
import os
import io
from datetime import datetime

app = FastAPI()


def replace_emojis_with_local_images(html: str) -> str:
    base_path = os.path.abspath("emoji")
    emoji_map = {
        "✅": f'<img src="file://{base_path}/check.png" class="emoji emoji-check">',
        "❌": f'<img src="file://{base_path}/cross.png" class="emoji emoji-cross">',
        "📋": f'<img src="file://{base_path}/report.png" class="emoji emoji-report">',
        "ℹ️": f'<img src="file://{base_path}/info.png" class="emoji emoji-info">',
    }
    for emoji, img_tag in emoji_map.items():
        html = html.replace(emoji, img_tag)
    return html
    
'''
def inject_css(html: str) -> str:
    css = """
    <style>
      img.emoji {
        vertical-align: middle;
        display: inline-block;
      }
      .emoji-check,
      .emoji-cross,
      .emoji-info {
        width: 16px;
        height: 16px;
      }
      .emoji-report {
        width: 24px;
        height: 24px;
      }
    </style>
    """
    return html.replace("</head>", f"{css}\n</head>")'''


@app.post("/convert-html-to-pdf/")
async def convert_html_to_pdf(html_content: str = Form(...)):
    # Replace emojis with image tags
    html_content = replace_emojis_with_local_images(html_content)

    # Optional: replace timestamp tag with current time
    html_content = html_content.replace("[Current Timestamp]", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    # Render HTML to PDF
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_pdf:
        HTML(string=html_content).write_pdf(tmp_pdf.name)
        tmp_pdf.seek(0)
        file_data = tmp_pdf.read()

    pdf_stream = io.BytesIO(file_data)
    filename = f"EMAIL_VALIDATE_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    return StreamingResponse(pdf_stream, media_type="application/pdf", headers={
        "Content-Disposition": f"attachment; filename={filename}"
    })
