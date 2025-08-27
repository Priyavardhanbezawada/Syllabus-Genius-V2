# app.py
import streamlit as st
import os

# We will create these helper files in the next steps
from pdf_parser import extract_text
from topic_extractor import extract_topics
from resource_finder import find_resources

st.set_page_config(page_title="Syllabus Genius", page_icon="🚀", layout="centered")

st.title("Syllabus Genius 🚀")
st.write("Upload your course syllabus (PDF) to automatically find learning resources for each topic.")

uploaded_file = st.file_uploader("Choose your syllabus PDF file", type="pdf")

if uploaded_file is not None:
    if st.button("Generate Study Guide"):
        temp_file_path = os.path.join(".", uploaded_file.name)
        with open(temp_file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        with st.spinner("Reading your syllabus... 📄"):
            raw_text = extract_text(temp_file_path)

        with st.spinner("Identifying topics... 🧠"):
            topics = extract_topics(raw_text)

        os.remove(temp_file_path)

        if not topics:
            st.error("Could not extract any topics from the PDF.")
        else:
            st.success(f"Found {len(topics)} topics! Fetching resources now...")
            st.header("✨ Your Personalized Study Guide ✨", divider="rainbow")

            for topic in topics:
                with st.expander(f"📚 {topic}"):
                    with st.spinner(f"Searching for '{topic}'..."):
                        resources = find_resources(topic)
                        if resources and "Error:" not in resources[0]:
                            for resource in resources:
                                st.markdown(resource)
                        else:
                            st.warning(resources[0] if resources else "No resources found.")
