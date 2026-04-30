# AI Chatbot

A conversational AI chatbot built with OpenAI and Anthropic Claude APIs, featuring streaming responses and function calling.

## Features
 - Streaming chat responses
 - Conversation memory across messages
 - Function calling - AI can fetch real-time weather data
 - Built with both OpenAI and Claude APIs

## Setup
1. Clone the repo
2. Create a Virtual envrionment: `python3 -m venv venve`
3. Activate it: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Create a `.env` file with your API keys:
OPEN_API_KEY=your_openai_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here
6. Run the chatbot: `python3 main.py`
7. Run function calling demo: `python3 function_calling.py`

## Stack
 - Python 3
 - OpenAI API (GPT-4o-mini)
 - Anthropic Claude API
 - FastAPI
 - dotenv