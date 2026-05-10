from PyPDF2 import PdfReader
import io

def extract_text_from_pdf(file_bytes: bytes) -> str:
    """Converts PDF bytes into a clean string for the Agent."""
    reader = PdfReader(io.BytesIO(file_bytes))
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text
