import pytest
from processor import extract_json

def test_extract_json_valid():
    response = 'Here is the JSON: [ {"id": 1, "value": "A"} ]'
    expected = [{"id": 1, "value": "A"}]
    assert extract_json(response) == expected

def test_extract_json_with_whitespace():
    response = '[\n  {\n    "id": 1,\n    "value": "A"\n  }\n]'
    expected = [{"id": 1, "value": "A"}]
    assert extract_json(response) == expected

def test_extract_json_no_match():
    response = 'No JSON here'
    assert extract_json(response) is None

def test_extract_json_invalid_json():
    response = '[ {"id": 1, "value": "A" }' # Missing closing bracket
    assert extract_json(response) is None

def test_extract_json_multiple_blocks():
    response = 'First block: [ {"id": 1} ] second block: [ {"id": 2} ]'
    # The current regex matches the first one greedily or non-greedily?
    # re.search(r'\[\s*\{[\s\S]*?\}\s*\]', response) -> non-greedy
    expected = [{"id": 1}]
    assert extract_json(response) == expected

from unittest.mock import patch, MagicMock
from processor import run_extraction

@patch('processor.bedrock_client')
def test_run_extraction(mock_bedrock):
    mock_bedrock.call_llm.return_value = '[{"id": 1, "value": "A"}]'

    result = run_extraction(b"content", "prompt", 0.3)

    assert result == [{"id": 1, "value": "A"}]
    mock_bedrock.call_llm.assert_called_once_with(b"content", "prompt", 0.3)
