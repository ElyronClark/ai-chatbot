# AI Chatbot — TechFlow Support Bot

A full-stack AI customer support chatbot built with FastAPI, OpenAI, and JWT authentication.
Features a React frontend, microservices architecture, and persistent conversation history in PostgreSQL.

## Features
- JWT authentication — register, login, protected routes
- Google OAuth login
- Conversation memory — last 10 messages loaded from PostgreSQL per user
- Persistent conversation history in PostgreSQL — survives refresh and logout
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
    DATABASE_URL=postgresql://user:password@localhost/dbname

Note: Both services connect to the same database. SECRET_KEY must be identical in both.

### 3. Start PostgreSQL

    sudo service postgresql start

### 4. Run both services

Terminal 1 — auth service:

    uvicorn main:app --reload --port 8001

Terminal 2 — chat service:

    uvicorn api:app --reload --port 8000

### 5. API docs
- Auth: http://localhost:8001/docs
- Chat: http://localhost:8000/docs

## Endpoints

- POST /chat — send a message, returns AI reply and saves to DB
- GET /history — load full conversation history for current user

## Stack
- Python 3 / FastAPI / Uvicorn
- OpenAI API (GPT-4o-mini)
- PostgreSQL + SQLAlchemy + psycopg2
- JWT (python-jose) + bcrypt (passlib)
- Google OAuth (authlib)
- React 18 (frontend)