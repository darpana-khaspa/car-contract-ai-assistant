import pdfplumber
import io

def extract_text_pipeline(uploaded_file):
    text = ""

    with pdfplumber.open(io.BytesIO(uploaded_file.getvalue())) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

    return text