# pdf_parser.py
import fitz  # PyMuPDF
import sys

def extract_text(pdf_path: str) -> str:
    """
    Extracts raw text content from a PDF file.
    """
    try:
        # Open the PDF file
        doc = fitz.open(pdf_path)

        # Initialize an empty string to hold all the text
        full_text = ""

        # Loop through each page in the PDF
        for page in doc:
            # Get the text from the page and add it to our string
            full_text += page.get_text()

        # Close the document to free up resources
        doc.close()

        return full_text
    except Exception as e:
        # If something goes wrong, print an error and return an empty string
        print(f"Error reading PDF file: {e}", file=sys.stderr)
        return ""
