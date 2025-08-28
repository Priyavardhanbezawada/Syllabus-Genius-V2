# pdf_parser.py
import fitz  # This is the PyMuPDF library
import sys

def extract_text(pdf_path: str) -> str:
    """
    This function opens a PDF file from the given path,
    reads the text from every page, and returns it as a single string.
    """
    try:
        # Open the PDF document
        doc = fitz.open(pdf_path)
        
        # Initialize an empty string to store the text
        full_text = ""
        
        # Loop through each page of the PDF
        for page in doc:
            # Add the text from the current page to our string
            full_text += page.get_text()
        
        # Close the document to free up system resources
        doc.close()
        
        return full_text
    except Exception as e:
        # If anything goes wrong (e.g., the file is corrupt),
        # print an error message and return an empty string.
        print(f"Error reading PDF file: {e}", file=sys.stderr)
        return ""
