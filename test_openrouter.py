import os
import dotenv
from langchain_openai import ChatOpenAI
from termcolor import colored

dotenv.load_dotenv()

key = os.getenv("OPENROUTER_API_KEY")
print(f"Key loaded: {key[:10]}...{key[-5:] if key else 'None'}")

if not key:
    print("No key found!")
    exit(1)

print("Testing OpenRouter with x-ai/grok-4.1-fast:free...")
try:
    llm = ChatOpenAI(
        model="x-ai/grok-4.1-fast:free",
        temperature=0,
        base_url="https://openrouter.ai/api/v1",
        api_key=key,
        default_headers={
            "HTTP-Referer": "https://localhost:3000", # Required by OpenRouter
            "X-Title": "AutoDesk Agent"
        }
    )
    response = llm.invoke("Hello, are you working?")
    print(colored(f"Success! Response: {response.content}", "green"))
except Exception as e:
    print(colored(f"Error: {e}", "red"))
