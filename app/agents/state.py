from typing import TypedDict, Optional, Any, List
from langchain_core.messages import BaseMessage

class AgentState(TypedDict):
    user_input: str
    intent: Optional[str]  # "TRACK" or "QUERY"
    
    # For Tracking
    extracted_data: Optional[dict]
    
    # For Querying
    query_type: Optional[str] # "GENERAL", "ANALYTICS", "INSIGHT"
    analytics_data: Optional[Any]
    
    final_response: Optional[str]
    messages: List[BaseMessage]
