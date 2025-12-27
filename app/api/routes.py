from fastapi import APIRouter, HTTPException
from app.models.schemas import TrackRequest, QueryRequest, AgentResponse
from app.agents.graph import graph
from app.agents.state import AgentState

router = APIRouter()

@router.post("/track", response_model=AgentResponse)
async def track_data(request: TrackRequest):
    """
    Log health data. Forces the intent to TRACK.
    """
    initial_state: AgentState = {
        "user_input": request.text,
        "intent": "TRACK",
        "messages": []
    }
    
    result = await graph.ainvoke(initial_state)
    
    return AgentResponse(
        response=result.get("final_response", "Processed."),
        data=result.get("extracted_data")
    )

@router.post("/query", response_model=AgentResponse)
async def query_agent(request: QueryRequest):
    """
    Handle natural language queries. Intent is detected automatically.
    """
    initial_state: AgentState = {
        "user_input": request.query,
        "intent": None,
        "messages": []
    }
    
    result = await graph.ainvoke(initial_state)
    
    return AgentResponse(
        response=result.get("final_response", "Processed."),
        data=result.get("analytics_data") or result.get("extracted_data")
    )
