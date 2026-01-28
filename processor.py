import time
import streamlit as st
from streamlit.runtime.uploaded_file_manager import UploadedFile
from bedrock_client import BedrockClient
import re
import json
from display import display
from result_logger import save_result_files

bedrock_client = BedrockClient()

def extract_json(response: str) -> json:
    # Use regex to find a JSON array that starts with [ { and ends with } ]
    match = re.search(r'\[\s*\{[\s\S]*?\}\s*\]', response)
    if not match:
        return None
    try:
        return json.loads(match.group(0))
    except Exception:
        return None

def read_file(uploaded_file: UploadedFile) -> bytes:
    """Read content from a Streamlit UploadedFile object."""
    return uploaded_file.getvalue()

def process_file(
    uploaded_file: UploadedFile,
    prompt_text: str,
    temperature: float
):
    read_file_banner = st.info(f"Reading file: {uploaded_file.name}")
    file_content = read_file(uploaded_file)
    read_file_banner.empty()
    read_file_banner = st.success("File read complete!")

    process_file_banner = st.info("Extracting attributes...")
    llm_response = bedrock_client.call_llm(file_content, prompt_text, temperature)
    json_response = extract_json(llm_response)
    process_file_banner.empty()
    process_file_banner = st.success("Extracted attributes!")
    display(json_response)

    log_path = save_result_files(
        uploaded_filename=uploaded_file.name,
        prompt_text=prompt_text,
        temperature=temperature,
        extracted_attributes=json_response,
    )
    st.caption(f"Saved results to: {log_path}")

    return True