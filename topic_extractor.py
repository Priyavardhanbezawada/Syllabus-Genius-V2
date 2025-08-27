# topic_extractor.py
import re

def extract_topics(text: str) -> list[str]:
    """
    Extracts potential course topics from raw text using regular expressions.
    This pattern looks for lines that are likely section headers or list items.
    """
    # This regex looks for lines starting with keywords like 'Unit', 'Module',
    # or lines that start with a number (e.g., "1. Introduction"), or a bullet point.
    pattern = re.compile(
        r"^\s*(?:unit|module|section|part|chapter)\s*\d+[:.\s-]*\s*(.+)" 
        r"|^\s*\d+\.\d*\s+([A-Za-z0-9\s,'-]{5,})"
        r"|^\s*[*-]\s+([A-Za-z0-9\s,'-]{5,})"
        , re.IGNORECASE | re.MULTILINE
    )

    matches = pattern.findall(text)

    # Clean up the matched strings
    topics = [item.strip() for group in matches for item in group if item]
    cleaned_topics = [re.sub(r'[\d\.:-]+$', '', topic).strip() for topic in topics]

    # Return unique topics while preserving the order they were found in
    unique_topics = list(dict.fromkeys(cleaned_topics))

    return unique_topics
