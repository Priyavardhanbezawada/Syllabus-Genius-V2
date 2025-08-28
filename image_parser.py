# image_parser.py
import easyocr
import io

# --- LAZY LOADING FIX ---
# We initialize the reader as None. It will only be loaded into memory
# the first time a user uploads an image.
reader = None

def get_ocr_reader():
    """
    This function initializes the EasyOCR reader but only does it once.
    """
    global reader
    if reader is None:
        print("Initializing EasyOCR reader...")
        # This is the memory-intensive step
        reader = easyocr.Reader(['en'])
        print("EasyOCR reader initialized.")
    return reader

def extract_text_from_image(image_bytes):
    """
    Uses EasyOCR to extract text from an image provided as bytes.
    """
    try:
        # Get the reader (it will be initialized only on the first call)
        ocr_reader = get_ocr_reader()

        # The readtext method returns a list of results.
        results = ocr_reader.readtext(image_bytes)

        # We join the text from all the results into a single string.
        full_text = " ".join([item[1] for item in results])

        return full_text
    except Exception as e:
        print(f"Error during EasyOCR processing: {e}")
        return ""
