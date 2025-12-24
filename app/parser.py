import fitz
import tempfile

def extract_pages(upload_file):
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(upload_file.file.read())
        path = tmp.name

    doc = fitz.open(path)
    return [page.get_text() for page in doc]
