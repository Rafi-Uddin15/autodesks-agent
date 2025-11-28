import os
import dotenv
from termcolor import colored
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

# Load environment variables
dotenv.load_dotenv()

if not os.getenv("OPENROUTER_API_KEY"):
    print(colored("Error: OPENROUTER_API_KEY not found in environment variables.", "red"))
    print("Please set it in a .env file or your environment.")
    print("Get a key from: https://openrouter.ai/keys")
    exit(1)

from graph import app

def print_stream(stream):
    for s in stream:
        message = s.get("messages")[-1] if "messages" in s else None
        if isinstance(message, tuple):
            print(message)
        else:
            message.pretty_print()

def main():
    print(colored("AutoDesk: Intelligent Support Orchestrator", "cyan", attrs=["bold"]))
    print("Type 'quit' to exit.\n")
    
    # Initialize chat history
    # We can keep a running list of messages, or let the graph handle it per turn?
    # The graph state has 'messages'.
    # If we want a continuous conversation, we should pass the previous history in.
    # But 'app.invoke' creates a new run.
    # To have memory across turns, we need to pass the updated 'messages' back in.
    
    chat_history = []
    
    while True:
        user_input = input(colored("User: ", "green"))
        if user_input.lower() in ["quit", "exit"]:
            break
            
        chat_history.append(HumanMessage(content=user_input))
        
        print(colored("\n--- Processing ---", "yellow"))
        
        # Run the graph
        # We pass the full history.
        # Note: The graph returns the FINAL state.
        final_state = app.invoke({"messages": chat_history})
        
        # The final state has the updated messages (including the AIMessage added by QA)
        chat_history = final_state["messages"]
        
        # The last message should be the response
        last_msg = chat_history[-1]
        if isinstance(last_msg, AIMessage):
            print(colored(f"AutoDesk: {last_msg.content}", "cyan"))
        else:
            print(colored(f"System: {last_msg}", "red"))
            
        print(colored("------------------\n", "yellow"))

if __name__ == "__main__":
    main()
