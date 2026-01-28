import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)
MODEL = "openai/gpt-oss-120b"


def call_llm(prompt: str) -> str:
    """
    Call Groq API with a prompt and return the response.
    
    Args:
        prompt: The user prompt to send to the model
    
    Returns:
        The model's response text
    """
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model=MODEL,
    )
    return chat_completion.choices[0].message.content