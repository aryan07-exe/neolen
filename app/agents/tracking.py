from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from app.agents.utils import get_llm
from app.agents.state import AgentState
from app.models.schemas import HealthLog
from app.db.mongodb import mongodb
from datetime import datetime

llm = get_llm()

parser = JsonOutputParser(pydantic_object=HealthLog)

system_prompt = """
You are a Health Tracking Agent. Extract health data from the user's input.
Map it to the following schema:
- category: One of ["water", "sleep", "mood", "workout", "bp", "sugar", "medication"]
- value: The numerical value or string value (e.g., "120/80" for bp).
- unit: The unit of measurement (e.g., "ml", "hours", "mg").
- note: Any additional context.

If multiple logs are present, just extract the first one or the most prominent one.
Return a valid JSON object.
"""

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("user", "{input}")
])

chain = prompt | llm | parser

async def tracking_node(state: AgentState):
    user_input = state["user_input"]
    try:
        data = await chain.ainvoke({"input": user_input})
        
        # Save to DB
        log_entry = HealthLog(**data)
        log_dict = log_entry.model_dump()
        
        if mongodb.db is not None:
            await mongodb.db.logs.insert_one(log_dict)
            log_dict["_id"] = str(log_dict["_id"])
            response = f"Successfully logged: {log_entry.category} - {log_entry.value} {log_entry.unit or ''}"
        else:
            response = "Database not connected. Data extracted but not saved."
            
        return {"extracted_data": log_dict, "final_response": response}
    except Exception as e:
        return {"final_response": f"Failed to track data: {str(e)}"}
