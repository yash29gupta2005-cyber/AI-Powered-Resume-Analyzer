
from pypdf import PdfReader


def extract_resume_text(file_path):
    """
    Extract readable text from a PDF resume.

    Args:
        file_path: Path to the resume PDF.

    Returns:
        Extracted text as a string.
    """
    reader = PdfReader(file_path)
    extracted_text = []

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            extracted_text.append(page_text)

    return "\n".join(extracted_text).strip()
