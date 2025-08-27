# topic_extractor.py
import spacy
import re

# Load the small English NLP model from spaCy.
# The build script will handle downloading this model on the server.
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("Spacy model 'en_core_web_sm' not found. This should be installed by the build.sh script.")
    nlp = None

def extract_topics(text: str) -> list[str]:
    """
    Extracts key topics from any text using spaCy's NLP model by identifying noun chunks.
    """
    if not nlp:
        return ["Error: spaCy model not loaded. Check the build script and deployment logs."]

    # Process the text with the spaCy pipeline
    doc = nlp(text)

    topics = []
    # A noun chunk is a phrase that has a noun as its head, e.g., "climate change"
    for chunk in doc.noun_chunks:
        topic = chunk.text.strip().replace("\n", " ")

        # Filter out very short phrases or irrelevant terms
        if len(topic) > 3 and "page" not in topic.lower():
            topics.append(topic)

    # Return unique topics while preserving the order
    unique_topics = list(dict.fromkeys(topics))

    return unique_topics[:50] # Limit to a reasonable number of topics
