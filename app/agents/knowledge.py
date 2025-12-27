from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from app.agents.utils import get_llm
from app.agents.state import AgentState

llm = get_llm()

system_prompt = """
You are a Health Knowledge Agent. Answer the user's general health question.
ALWAYS include a disclaimer that you are an AI and this is not medical advice.
Keep the answer concise and helpful.
"""

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("user", "{input}")
])

chain = prompt | llm | StrOutputParser()

async def knowledge_node(state: AgentState):
    user_input = state["user_input"]
    response = await chain.ainvoke({"input": user_input})
    return {"final_response": response}
