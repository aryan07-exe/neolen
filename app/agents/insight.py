from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from app.agents.utils import get_llm
from app.agents.state import AgentState

llm = get_llm()

system_prompt = """
You are an Insight Agent. Analyze the provided health data and answer the user's question.
Look for patterns, trends, or simply summarize the data.
If the data is empty, inform the user.

Data:
{data}
"""

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("user", "{input}")
])

chain = prompt | llm | StrOutputParser()

async def insight_node(state: AgentState):
    data = state.get("analytics_data", [])
    user_input = state["user_input"]
    
    if not data:
        return {"final_response": "I couldn't find any data matching your query."}
        
    # Limit data size to avoid context overflow if too large
    data_str = str(data[:50]) # Just take last 50 records for now
    
    response = await chain.ainvoke({"input": user_input, "data": data_str})
    return {"final_response": response}
