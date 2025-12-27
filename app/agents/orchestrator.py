from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from app.agents.utils import get_llm
from app.agents.state import AgentState

llm = get_llm()

system_prompt = """
You are the Orchestrator of a Health AI system.
Classify the user's input into one of the following intents:

1. TRACK: The user wants to log or record health data (e.g., "I drank water", "slept 8 hours", "took meds").
2. KNOWLEDGE: The user is asking a general health question that does not require their personal data (e.g., "What is normal BP?", "How to sleep better?").
3. ANALYTICS: The user is asking about their personal health data, stats, history, or patterns (e.g., "How much water did I drink?", "Show my sleep trends", "Am I improving?").

Return ONLY the intent: TRACK, KNOWLEDGE, or ANALYTICS.
"""

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("user", "{input}")
])

chain = prompt | llm | StrOutputParser()

async def orchestrator_node(state: AgentState):
    if state.get("intent"):
        return {"intent": state["intent"]}

    user_input = state["user_input"]
    intent = await chain.ainvoke({"input": user_input})
    intent = intent.strip().upper()
    
    # Fallback or cleaning
    if intent not in ["TRACK", "KNOWLEDGE", "ANALYTICS"]:
        intent = "KNOWLEDGE" # Default to general knowledge if unsure
        
    return {"intent": intent}
