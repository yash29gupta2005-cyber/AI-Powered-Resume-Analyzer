
import sys
from pathlib import Path

# Allow importing modules from the backend folder.
backend_path = Path(__file__).resolve().parents[1] / "backend"
sys.path.insert(0, str(backend_path))

from resume_parser import extract_resume_text


def test_resume_parser():
    resume_path = input("Enter the full path of your resume PDF: ").strip()
    resume_path = resume_path.strip('"')

    try:
        text = extract_resume_text(resume_path)

        if text:
            print("\nResume text extracted successfully!\n")
            print("-" * 50)
            print(text)
            print("-" * 50)
        else:
            print("No readable text found in the PDF.")

    except Exception as error:
        print(f"Error extracting resume: {error}")


if __name__ == "__main__":
    test_resume_parser()
