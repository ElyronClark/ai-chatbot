from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from jose import JWTError, jwt
from pydantic import BaseModel
from openai import OpenAI
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY not set in environment")
ALGORITHM = "HS256"

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)

class Conversation(Base):
    __tablename__ = "conversations"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    message = Column(String)
    role = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class Message(BaseModel):
    message: str

@app.post("/chat")
async def chat(body: Message, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    history = db.query(Conversation)\
        .filter(Conversation.user_id == current_user.id)\
        .order_by(Conversation.created_at)\
        .all()

    recent = history[-10:] if len(history) > 10 else history
    conversation = [{"role": m.role, "content": m.message} for m in recent]

    messages = [
        {"role": "system", "content": "Your name is Maggie. You are a friendly but professional assistant for TechFlow, a project management SaaS. Respond in plain text only, no markdown formatting. Be concise and direct — no unnecessary filler. If you don't know the answer, say so honestly and suggest the user contact TechFlow support directly."}
    ] + conversation + [
        {"role": "user", "content": body.message}
    ]

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0.3
        )
    except Exception:
        raise HTTPException(status_code=500, detail="AI service failed")

    reply = response.choices[0].message.content
    tokens_used = response.usage.total_tokens
    print(f"Tokens used: {tokens_used}")

    db.add(Conversation(user_id=current_user.id, message=body.message, role="user"))
    db.add(Conversation(user_id=current_user.id, message=reply, role="assistant"))
    db.commit()

    return {"reply": reply, "tokens_used": tokens_used}

@app.get("/history")
async def get_history(current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    messages = db.query(Conversation)\
        .filter(Conversation.user_id == current_user.id)\
        .order_by(Conversation.created_at)\
        .all()
    return [{"role": m.role, "content": m.message, "created_at": str(m.created_at)} for m in messages]

@app.get("/")
async def root():
    return {"message": "AI Chatbot API is running"}