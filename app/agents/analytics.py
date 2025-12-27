from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from app.agents.utils import get_llm
from app.agents.state import AgentState
from app.db.mongodb import mongodb
from datetime import datetime, timedelta
from pydantic import BaseModel, Field
from typing import Optional

llm = get_llm()

class QueryParams(BaseModel):
    category: Optional[str] = Field(description="The health category to filter by (e.g., water, sleep). If null, fetch all.")
    days: int = Field(description="Number of days to look back. Default to 7 if not specified.")

parser = JsonOutputParser(pydantic_object=QueryParams)

system_prompt = """
You are an Analytics Agent. Extract query parameters from the user's request.
Return a JSON with:
- category: The health category (water, sleep, mood, workout, bp, sugar, medication) or null if not specific.
- days: Number of days to look back (e.g., "last week" = 7, "yesterday" = 1). Default to 7.
"""

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("user", "{input}")
])

chain = prompt | llm | parser

async def analytics_node(state: AgentState):
    user_input = state["user_input"]
    try:
        params = await chain.ainvoke({"input": user_input})
        days = params.get("days", 7)
        category = params.get("category")
        
        start_date = datetime.utcnow() - timedelta(days=days)
        
        query = {"timestamp": {"$gte": start_date}}
        if category:
            query["category"] = category
            
        logs = []
        if mongodb.db is not None:
            cursor = mongodb.db.logs.find(query)
            async for doc in cursor:
                doc["_id"] = str(doc["_id"]) # Serialize ObjectId
                logs.append(doc)
        
        return {"analytics_data": logs}
    except Exception as e:
        return {"analytics_data": [], "final_response": f"Error fetching data: {str(e)}"}
