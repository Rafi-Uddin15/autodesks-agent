import requests
import json
from termcolor import colored

url = "http://localhost:8000/chat"
payload = {"message": "I need a refund for invoice INV-1234"}
headers = {"Content-Type": "application/json"}

print(f"Testing API at {url}...")
try:
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        print(colored("Success!", "green"))
        print(json.dumps(response.json(), indent=2))
    else:
        print(colored(f"Failed with status {response.status_code}", "red"))
        print(response.text)
except Exception as e:
    print(colored(f"Error: {e}", "red"))
