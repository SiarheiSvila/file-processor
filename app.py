import streamlit as st
from processor import process_file
from const import PROMPT

SMALL_WIDTH = 600

st.set_page_config(page_title="SBC File Processor", layout="wide")

st.title("SBC file processor")

prompt_text = st.text_area(
    "Enter your prompt text:",
    value=PROMPT,
    height=450,
    help="This prompt will be used to instruct the AI model."
)

temperature = st.slider(
    "Select temperature for the AI model:",
    min_value=0.0,
    max_value=1.0,
    value=0.3,
    step=0.05,
    width=SMALL_WIDTH,
    help="Higher values (e.g., 0.8) make the output more random, while lower values (e.g., 0.2) makes it more focused and deterministic."
)

MODEL_OPTIONS = {
    "Claude Sonnet 4": "us.anthropic.claude-sonnet-4-20250514-v1:0",
    "Claude Sonnet 4.5": "us.anthropic.claude-sonnet-4-5-20250929-v1:0",
}

model_label = st.selectbox(
    "Model",
    options=list(MODEL_OPTIONS.keys()),
    index=0,
    width=SMALL_WIDTH,
    help="Choose the Claude model for extraction.",
)
model_id = MODEL_OPTIONS[model_label]

uploaded_file = st.file_uploader(
    "Upload your file",
    type=None,
    width=SMALL_WIDTH,
    help="Drag and drop or click to upload a file"
)

process_button = st.button("Process")

if uploaded_file is not None:
    st.success(f"File uploaded: {uploaded_file.name}")
    # st.write(f"File size: {uploaded_file.size} bytes")
    if process_button:
        # processing = st.info("Processing...")
        result = process_file(uploaded_file, prompt_text, temperature, model_id=model_id)
        if result:
            # processing.empty()
            st.success("Processing complete!")
