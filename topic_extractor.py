# topic_extractor.py
import re

def extract_topics(text: str) -> list[str]:
    """
    This function uses a text pattern (regular expression) to find lines
    in the text that are likely to be topics. It looks for common syllabus
    formats like "Unit 1: Topic Name" or numbered lists.
    """
    # This complex-looking string is a "regular expression".
    # It defines a pattern to search for in the text.
    pattern = re.compile(
        # This part looks for lines starting with "Unit", "Module", "Chapter", etc.
        r"^\s*(?:unit|module|section|part|chapter)\s*\d+[:.\s-]*\s*(.+)"
        # This part looks for lines starting with a number like "1." or "2.1"
        r"|^\s*\d+\.\d*\s+([A-Za-z0-9\s,'-]{5,})"
        # This part looks for lines starting with a bullet point "*" or "-"
        r"|^\s*[*-]\s+([A-Za-z0-9\s,'-]{5,})",
        re.IGNORECASE | re.MULTILINE
    )
    
    # Find all strings in the text that match the pattern
    matches = pattern.findall(text)
    
    # The result is a bit messy, so we clean it up.
    # We take all the matched groups and remove any extra whitespace.
    topics = [item.strip() for group in matches for item in group if item]
    
    # We remove any trailing numbers or punctuation from the topics.
    cleaned_topics = [re.sub(r'[\d\.:-]+$', '', topic).strip() for topic in topics]
    
    # Finally, we remove any duplicate topics while keeping the original order.
    unique_topics = list(dict.fromkeys(cleaned_topics))
    
    return unique_topics
