from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from .client import Client
from .tools import Tools

app = FastAPI()
tools = Tools()
client = Client(tools)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
def start_chat(chat_request: ChatRequest):
    return client.send_user_query(chat_request.message)