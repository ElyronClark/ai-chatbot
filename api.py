from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import BaseModel
from openai import OpenAI
from typing import List, Dict, Any
import os
import httpx
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY not set in environment")
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="http://localhost:8001/token")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return email
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # your React port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class Message(BaseModel):
    message: str
    conversation: List[Dict[str, Any]] = []

@app.post("/chat")
async def chat(body: Message, current_user: str = Depends(get_current_user)):
    # Keep only last 10 messages to manage token costs
    recent_conversation = body.conversation[-10:] if len(body.conversation) > 10 else body.conversation

    messages = [
        {"role": "system", "content": "Your name is Maggie. You are a friendly but professional assistant for TechFlow, a project management SaaS. Respond in plain text only, no markdown formatting. Be concise and direct — no unnecessary filler. If you don't know the answer, say so honestly and suggest the user contact TechFlow support directly."}
    ] + recent_conversation + [
        {"role": "user", "content": body.message}
    ]
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.3
    )

    reply = response.choices[0].message.content
    tokens_used = response.usage.total_tokens
    print(f"Tokens used: {tokens_used}")
    return {"reply": reply, "tokens_used": tokens_used}

@app.get("/")
async def root():
    return {"message": "AI Chatbot API is running"}