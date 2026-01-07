from pathlib import Path
from pypdf import PdfReader


def load_pdf_text(pdf_path: str) -> str:
    """
    Extracts text from a PDF file page by page.
    """
    reader = PdfReader(pdf_path)
    pages_text = []

    for page_num, page in enumerate(reader.pages):
        text = page.extract_text()
        if text:
            pages_text.append(text)

    return "\n".join(pages_text)


def load_all_pdfs(folder_path: str) -> dict:
    """
    Loads all PDFs from a folder.
    Returns a dict: {filename: extracted_text}
    """
    pdf_texts = {}
    pdf_files = Path(folder_path).glob("*.pdf")

    for pdf in pdf_files:
        with open(pdf, 'r') as file:
            pdf_texts[pdf.name] = load_pdf_text(pdf)

    return pdf_texts
