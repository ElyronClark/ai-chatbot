# AI Chatbot — TechFlow Support Bot

A full-stack AI customer support chatbot built with FastAPI, OpenAI, and JWT authentication.
Features a React frontend, microservices architecture, and persistent conversation history in PostgreSQL.

## Features
- JWT authentication — register, login, protected routes
- Google OAuth login
- Streaming chat responses
- Conversation memory with 10 message limit for token efficiency
- Persistent conversation history in PostgreSQL
- Microservices architecture — auth service and chat service on separate ports
- Token usage tracking
- Tuned system prompt — Maggie, TechFlow support persona
- Auto-generated API docs at `/docs`

## Architecture

React Frontend (5173) → Auth Service on 8001 → PostgreSQL
                      → Chat Service on 8000 → OpenAI API

Both services share a SECRET_KEY to sign and verify JWTs.

## Setup

### 1. Clone and install
    git clone https://github.com/yourusername/ai-chatbot
    cd ai-chatbot
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt

### 2. Environment variables

Auth service .env:
    DATABASE_URL=postgresql://user:password@localhost/dbname
    SECRET_KEY=your_secret_key
    GOOGLE_CLIENT_ID=your_google_client_id
    GOOGLE_CLIENT_SECRET=your_google_client_secret

Chat service .env:
    OPENAI_API_KEY=your_openai_key
    SECRET_KEY=your_exact_same_secret_key

### 3. Run both services

Terminal 1 — auth service:
    uvicorn auth:app --reload --port 8001

Terminal 2 — chat service:
    uvicorn api:app --reload --port 8000

### 4. API docs
- Auth: http://localhost:8001/docs
- Chat: http://localhost:8000/docs

## Stack
- Python 3 / FastAPI / Uvicorn
- OpenAI API (GPT-4o-mini)
- PostgreSQL + SQLAlchemy
- JWT (python-jose) + bcrypt (passlib)
- Google OAuth (authlib)
- React 18 (frontend)