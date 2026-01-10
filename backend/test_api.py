import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

print(f"API Key found: {'Yes' if api_key else 'No'}")
print(f"API Key length: {len(api_key) if api_key else 0}")
print(f"API Key starts with: {api_key[:10] if api_key else 'N/A'}...")

print("\nTesting OpenAI API connection...")

try:
    client = OpenAI(api_key=api_key, timeout=10.0)
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": "Say 'API works!'"}
        ],
        max_tokens=10
    )
    
    print(f"SUCCESS: {response.choices[0].message.content}")
    
except Exception as e:
    print(f"ERROR: {str(e)}")
