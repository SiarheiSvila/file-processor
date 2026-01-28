import boto3
import json
import os
import base64
from dotenv import load_dotenv
from const import PROMPT

load_dotenv()

class BedrockClient:
    def __init__(self, model: str = 'us.anthropic.claude-sonnet-4-20250514-v1:0'):
        self.model_id = model
        self.client = boto3.client(
            aws_access_key_id=os.environ.get("ACCESS_KEY"),
            aws_secret_access_key=os.environ.get("SECRET_ACCESS_KEY"),
            service_name='bedrock-runtime',
            region_name=os.environ.get("AWS_REGION", "us-east-1")
        )

    def call_llm(self, uploaded_file: bytes, prompt_text: str, temperature: float = 0.5) -> str:
        encoded_file = base64.b64encode(uploaded_file).decode('utf-8')
        body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 4096,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "document",
                            "source": {
                                "type": "base64",
                                "media_type": "application/pdf",
                                "data": encoded_file
                            },
                            "title": "medical_report",
                            "citations": {"enabled": True},
                            "cache_control": {"type": "ephemeral"}
                        },
                        {
                            "type": "text",
                            "text": prompt_text,
                        },
                    ],
                }
            ],
            "temperature": temperature,
        }
        
        response = self.client.invoke_model(
            body=json.dumps(body), 
            modelId=self.model_id, 
            accept='application/json', 
            contentType='application/json'
        )
        
        response_body = json.loads(response.get('body').read())
        return response_body['content'][0]['text']
