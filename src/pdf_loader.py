from pypdf import PdfReader

def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Docstring for extract_text_from_pdf
    
    Extracts text from a PDF file.
    Returns all text as a single string.
    """
    reader = PdfReader(pdf_path)
    text = ""

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    
    return text