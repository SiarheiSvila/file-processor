import streamlit as st
from processor import process_file
from const import PROMPT

st.set_page_config(page_title="SBC File Processor", layout="wide")

st.title("SBC file processor")

prompt_text = st.text_area(
    "Enter your prompt text:",
    value=PROMPT,
    height=1000,
    help="This prompt will be used to instruct the AI model."
)

temperature = st.slider(
    "Select temperature for the AI model:",
    min_value=0.0,
    max_value=1.0,
    value=0.3,
    step=0.05,
    width=500,
    help="Higher values (e.g., 0.8) make the output more random, while lower values (e.g., 0.2) makes it more focused and deterministic."
)

uploaded_file = st.file_uploader(
    "Upload your file",
    type=None,
    help="Drag and drop or click to upload a file"
)

process_button = st.button("Process")

if uploaded_file is not None:
    st.success(f"File uploaded: {uploaded_file.name}")
    # st.write(f"File size: {uploaded_file.size} bytes")
    if process_button:
        # processing = st.info("Processing...")
        result = process_file(uploaded_file, prompt_text, temperature)
        if result:
            # processing.empty()
            st.success("Processing complete!")
