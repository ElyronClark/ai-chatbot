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
    messages = [
        {"role": "system", "content": "You are a helpful assistant for TechFlow, a project management SaaS."}
    ] + body.conversation + [
        {"role": "user", "content": body.message}
    ]
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )
    
    reply = response.choices[0].message.content
    return {"reply": reply}

@app.get("/")
async def root():
    return {"message": "AI Chatbot API is running"}