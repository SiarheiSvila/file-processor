from bedrock_client import BedrockClient

bedrock_client = BedrockClient()

def call_llm(prompt: str) -> str:
    return bedrock_client.call_llm(prompt)