import operator
from typing import Annotated, List, TypedDict, Union, Dict, Any
from langchain_core.messages import BaseMessage

class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], operator.add]
    next_step: str
    current_agent: str # Track which agent is handling the ticket
    ticket_details: Dict[str, Any]
    draft_response: str
    qa_feedback: str
    retry_count: int
