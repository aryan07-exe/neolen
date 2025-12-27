
## Note: I have pushed the .env folder to make the setup simple and easy to use.
## I have added my gemini api and mongo url for the testing part.
# AI Health Tracking Backend

## Project Overview

This is a smart backend system designed to be your personal AI health companion. Think of it as a team of intelligent assistants working together to help you track your health and answer your questions.

Here's what it does:
- It Listens: You can tell it things like "I just drank a glass of water" or "I ran 5km today," and it automatically understands and saves that information.
- It Remembers: All your health data (sleep, mood, workouts, etc.) is securely stored so you don't have to worry about forgetting.
- It Analyzes: You can ask questions like "How has my sleep been this week?" and it will look at your history and give you a summary.
- It Educates: If you have general health questions like "Why is hydration important?", it can answer those too, using general medical knowledge.

It uses advanced AI (Gemini) to understand natural language, so you don't need to fill out boring forms—just talk to it!

## Setup

1. Install dependencies:
   
   pip install -r requirements.txt
   

2. Set up environment variables:
   
   Start Your MONGODB COmpass

3. Run the server:

   uvicorn app.main:app --reload


Endpoints

- `POST /track`: Log health data.
  - Body: `{"text": "I drank 500ml water"}`
  Through this api we can give the input of the daily activites which are stored in the db and then later llm can answer based on the data
- `POST /query`: Ask questions or get analytics.
  - Body: `{"query": "How is my sleep trend?"}`
  This uses db as context and based on the info it have it answers the queries asked

## Architecture

- **FastAPI**: Web framework.
- **LangGraph**: Multi-agent orchestration.
- **MongoDB**: Database.
- **Gemini**: LLM for intent detection, extraction, and insights.
