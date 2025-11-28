from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_core.utils.function_calling import convert_to_openai_function
from pydantic import BaseModel, Field
from typing import Literal
import os

from state import AgentState
from tools import lookup_invoice, process_refund, check_server_status, search_knowledge_base

# --- LLM Setup ---
# Using OpenRouter with the requested model
llm = ChatOpenAI(
    model="x-ai/grok-4.1-fast:free",
    temperature=0,
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    default_headers={
        "HTTP-Referer": "https://localhost:3000",
        "X-Title": "AutoDesk Agent"
    }
)

# --- Supervisor ---
class Route(BaseModel):
    next_step: Literal["billing", "technical", "general"] = Field(
        description="The department to route the ticket to."
    )

supervisor_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are the Support Supervisor. Your job is to route incoming tickets to the correct department.\n"
               "Options:\n"
               "- 'billing': For invoices, payments, refunds.\n"
               "- 'technical': For server issues, bugs, technical questions.\n"
               "- 'general': For greetings or out-of-scope queries that you can answer directly."),
    MessagesPlaceholder(variable_name="messages"),
])

def supervisor_node(state: AgentState):
    chain = supervisor_prompt | llm.with_structured_output(Route)
    result = chain.invoke({"messages": state["messages"]})
    return {"next_step": result.next_step, "current_agent": result.next_step}

# --- Billing Agent ---
billing_tools = [lookup_invoice, process_refund]
billing_llm = llm.bind_tools(billing_tools)

def billing_node(state: AgentState):
    messages = state["messages"]
    system_msg = SystemMessage(content="You are a Billing Support Agent. Use your tools to help the user. "
                                       "If you have performed an action, summarize it for the user.")
    
    current_messages = [system_msg] + messages
    response = billing_llm.invoke(current_messages)
    
    while response.tool_calls:
        tool_outputs = []
        for tool_call in response.tool_calls:
            tool_name = tool_call["name"]
            tool_args = tool_call["args"]
            
            if tool_name == "lookup_invoice":
                res = lookup_invoice.invoke(tool_args)
            elif tool_name == "process_refund":
                res = process_refund.invoke(tool_args)
            else:
                res = "Unknown tool"
            
            tool_outputs.append(
                {"tool_call_id": tool_call["id"], "role": "tool", "name": tool_name, "content": res}
            )
        
        from langchain_core.messages import ToolMessage
        tool_msgs = [ToolMessage(content=t["content"], tool_call_id=t["tool_call_id"], name=t["name"]) for t in tool_outputs]
        
        current_messages.append(response)
        current_messages.extend(tool_msgs)
        
        response = billing_llm.invoke(current_messages)
        
    return {"draft_response": response.content}

# --- Technical Agent ---
tech_tools = [check_server_status, search_knowledge_base]
tech_llm = llm.bind_tools(tech_tools)

def tech_node(state: AgentState):
    messages = state["messages"]
    system_msg = SystemMessage(content="You are a Technical Support Agent. Use your tools to diagnose and solve issues.")
    
    current_messages = [system_msg] + messages
    response = tech_llm.invoke(current_messages)
    
    while response.tool_calls:
        tool_outputs = []
        for tool_call in response.tool_calls:
            tool_name = tool_call["name"]
            tool_args = tool_call["args"]
            
            if tool_name == "check_server_status":
                res = check_server_status.invoke(tool_args)
            elif tool_name == "search_knowledge_base":
                res = search_knowledge_base.invoke(tool_args)
            else:
                res = "Unknown tool"
                
            tool_outputs.append(
                {"tool_call_id": tool_call["id"], "role": "tool", "name": tool_name, "content": res}
            )
            
        from langchain_core.messages import ToolMessage
        tool_msgs = [ToolMessage(content=t["content"], tool_call_id=t["tool_call_id"], name=t["name"]) for t in tool_outputs]
        
        current_messages.append(response)
        current_messages.extend(tool_msgs)
        
        response = tech_llm.invoke(current_messages)
        
    return {"draft_response": response.content}

# --- General Agent ---
def general_node(state: AgentState):
    messages = state["messages"]
    response = llm.invoke(messages)
    return {"draft_response": response.content}

# --- QA / Reflection Node ---
class QAResult(BaseModel):
    status: Literal["Accepted", "Rejected"] = Field(description="Accept or Reject the response.")
    feedback: str = Field(description="Feedback if rejected, or empty if accepted.")

qa_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a Quality Assurance Specialist. Review the draft response.\n"
               "Check for:\n"
               "1. Politeness and professionalism.\n"
               "2. Accuracy (based on the tools used, if visible, or general sense).\n"
               "3. Completeness.\n"
               "If the response is good, accept it. If not, reject it with feedback."),
    ("human", "User Query: {last_user_message}\n"
              "Draft Response: {draft_response}")
])

def qa_node(state: AgentState):
    last_user_message = state["messages"][-1].content
    draft = state["draft_response"]
    
    chain = qa_prompt | llm.with_structured_output(QAResult)
    result = chain.invoke({"last_user_message": last_user_message, "draft_response": draft})
    
    if result.status == "Rejected":
        from langchain_core.messages import SystemMessage
        feedback_msg = SystemMessage(content=f"QA Rejected your draft. Feedback: {result.feedback}. Please try again.")
        return {
            "qa_feedback": result.feedback, 
            "next_step": state["current_agent"], 
            "messages": [feedback_msg]
        }
    else:
        final_msg = AIMessage(content=draft)
        return {
            "qa_feedback": "", 
            "next_step": "END", 
            "messages": [final_msg]
        }
