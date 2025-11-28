import dotenv
import os

dotenv.load_dotenv()
print(f"DEBUG: OPENAI_API_KEY={os.getenv('OPENAI_API_KEY')}")
print(f"DEBUG: OPENROUTER_API_KEY={os.getenv('OPENROUTER_API_KEY')}")

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_core.messages import HumanMessage, AIMessage
from graph import app

app_api = FastAPI(title="AutoDesk Agent API")

class ChatRequest(BaseModel):
    message: str
    thread_id: str = "default"

class ChatResponse(BaseModel):
    response: str
    thread_id: str

@app_api.get("/health")
async def health():
    return {"status": "active", "agents": ["Billing", "Technical", "General", "QA"]}

@app_api.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        # LangGraph state expects a list of messages
        # We invoke the graph with the user's input
        # Note: For a real app, you'd want to load history based on thread_id
        # Here we just pass the new message, assuming the graph or client handles history
        # But our graph is stateless per invocation unless we use a checkpointer.
        # For this simple integration, we'll just return the immediate response.
        
        inputs = {"messages": [HumanMessage(content=request.message)]}
        
        # Run the graph
        final_state = app.invoke(inputs)
        
        # Get the last message
        last_msg = final_state["messages"][-1]
        response_text = last_msg.content if isinstance(last_msg, AIMessage) else str(last_msg)
        
        return ChatResponse(response=response_text, thread_id=request.thread_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app_api, host="0.0.0.0", port=8000)
