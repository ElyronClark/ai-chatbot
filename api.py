from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class Message(BaseModel):
    message: str
    conversation: list = []

@app.post("/chat")
async def chat(body: Message):
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