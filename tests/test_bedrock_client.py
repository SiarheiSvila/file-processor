import pytest
from unittest.mock import MagicMock, patch
from bedrock_client import BedrockClient
import json
import io

@patch('boto3.client')
def test_bedrock_client_init(mock_boto):
    client = BedrockClient()
    mock_boto.assert_called_once()
    assert client.model_id == 'us.anthropic.claude-sonnet-4-20250514-v1:0'

@patch('boto3.client')
def test_call_llm(mock_boto):
    # Setup mock response
    mock_runtime = MagicMock()
    mock_boto.return_value = mock_runtime

    mock_response = {
        'body': io.BytesIO(json.dumps({
            'content': [{'text': '[{"id": 1, "value": "A"}]'}]
        }).encode('utf-8'))
    }
    mock_runtime.invoke_model.return_value = mock_response

    client = BedrockClient()
    response = client.call_llm(b"file content", "prompt", 0.5)

    assert response == '[{"id": 1, "value": "A"}]'
    mock_runtime.invoke_model.assert_called_once()

    # Check if arguments to invoke_model are correct
    args, kwargs = mock_runtime.invoke_model.call_args
    assert kwargs['modelId'] == client.model_id
    body = json.loads(kwargs['body'])
    assert body['temperature'] == 0.5
    assert body['messages'][0]['content'][1]['text'] == 'prompt'
