# AI Chatbot

A conversational AI chatbot built with OpenAI and Anthropic Claude APIs, featuring streaming responses, function calling, and a FastAPI backend.

## Features
- Streaming chat responses
- Conversation memory across messages
- Function calling — AI can fetch real-time weather data
- FastAPI REST API backend
- Auto-generated API docs at `/docs`
- Built with both OpenAI and Claude APIs

## Setup

1. Clone the repo
2. Create a virtual environment: `python3 -m venv venv`
3. Activate it: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Create a `.env` file with your API keys:
    - `OPENAI_API_KEY=your_openai_key_here`
    - `ANTHROPIC_API_KEY=your_anthropic_key_here`
6. Run the terminal chatbot: `python3 main.py`
7. Run the API: `uvicorn api:app --reload`
8. API docs: `http://127.0.0.1:8000/docs`

## Stack
- Python 3
- OpenAI API (GPT-4o-mini)
- Anthropic Claude API
- FastAPI
- Uvicorn
- dotenv