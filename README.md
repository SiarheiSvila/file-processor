# SBC File Processor

A Streamlit UI that uploads a plan document (PDF), sends it to **AWS Bedrock (Anthropic Claude)** with an extraction prompt, and displays the extracted attributes as a table.

## What it does

- **Input**: a PDF document (uploaded in the UI)
- **Prompt**: editable in the UI (defaults to `PROMPT` in `const.py`)
- **Model call**: `bedrock-runtime:InvokeModel` using a Claude model (default: `us.anthropic.claude-sonnet-4-20250514-v1:0`)
- **Output expected from the model**: a JSON array like:

```json
[
  { "id": 1630, "value": "..." },
  { "id": 1631, "value": "..." }
]
```

- **Rendering**: the app merges extracted `{id, value}` rows with metadata from `SOURCE_DATAFRAME` in `const.py` and shows a table with columns:
  `id`, `attr_type`, `category_name`, `name`, `tier_desc`, `value`.

## Prerequisites

- Python 3.8 or higher
- AWS credentials with permission to call **Bedrock Runtime**

## Installation

1. Create a virtual environment (optional but recommended):

```bash
python -m venv venv
```

2. Activate the virtual environment:

**Windows:**
```bash
venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## AWS configuration

The app uses `boto3` to call Bedrock and relies on the standard AWS credential resolution chain (env vars, shared config, IAM role, etc.).

- **Region**: uses `AWS_REGION` if set, otherwise defaults to `us-east-1`.

Example (PowerShell):

```powershell
$env:AWS_REGION="us-east-1"
# plus any standard AWS auth method, e.g.:
# $env:AWS_ACCESS_KEY_ID="..."
# $env:AWS_SECRET_ACCESS_KEY="..."
# $env:AWS_SESSION_TOKEN="..."   # if applicable
```

## Running the App

Start the Streamlit app with:

```bash
streamlit run app.py
```

The app will open in your default browser at `http://localhost:8501`.

## Using the UI

1. **Enter your prompt text** (or keep the default).
2. **Select temperature** (default: `0.3`).
3. **Upload your file** (PDF).
4. Click **Process** to run extraction and display the results.

## Notes / limitations

- **PDF-only**: the Bedrock request always sends `media_type: application/pdf`. Uploading non-PDF files will likely fail or produce bad results.
- **JSON parsing**: the app extracts the *first* JSON array matching `[...]` from the model response. Keep the prompt strict so the model outputs a clean JSON array.
