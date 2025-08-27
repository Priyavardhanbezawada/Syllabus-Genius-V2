# image_parser.py
import easyocr
import io

# Initialize the OCR reader for English.
# This will download the necessary model the first time it runs.
reader = easyocr.Reader(['en'])

def extract_text_from_image(image_bytes):
    """
    Uses EasyOCR to extract text from an image provided as bytes.
    """
    try
        # The readtext method returns a list of results.
        results = reader.readtext(image_bytes)

        # We join the text from all the results into a single string.
        full_text = " ".join([item[1] for item in results])

        return full_text
    except Exception as e:
        print(f"Error during EasyOCR processing: {e}")
        return ""
