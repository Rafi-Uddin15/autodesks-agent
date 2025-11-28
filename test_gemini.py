import os
import dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from termcolor import colored

dotenv.load_dotenv()

key = os.getenv("GOOGLE_API_KEY")
print(f"Key loaded: {key[:5]}...{key[-5:] if key else 'None'}")

if not key:
    print("No key found!")
    exit(1)

print("Testing Gemini Pro...")
try:
    llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0)
    response = llm.invoke("Hello, are you working?")
    print(colored(f"Success! Response: {response.content}", "green"))
except Exception as e:
    print(colored(f"Error with gemini-pro: {e}", "red"))

print("\nTesting Gemini 1.5 Pro...")
try:
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0)
    response = llm.invoke("Hello, are you working?")
    print(colored(f"Success! Response: {response.content}", "green"))
except Exception as e:
    print(colored(f"Error with gemini-1.5-pro: {e}", "red"))
