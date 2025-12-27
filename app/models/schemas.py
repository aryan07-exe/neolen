from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime

class HealthLog(BaseModel):
    category: Literal["water", "sleep", "mood", "workout", "bp", "sugar", "medication"]
    value: str | float | int
    unit: Optional[str] = None
    note: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class QueryRequest(BaseModel):
    query: str

class TrackRequest(BaseModel):
    text: str

class AgentResponse(BaseModel):
    response: str
    data: Optional[dict | list] = None
