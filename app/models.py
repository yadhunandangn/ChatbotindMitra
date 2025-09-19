from pydantic import BaseModel
from typing import List, Optional

class ChatRequest(BaseModel):
    username: str
    role: str
    message: str
    intent: Optional[str] = None

class Message(BaseModel):
    role: str
    message: str
    timestamp: str

class ChatResponse(BaseModel):
    reply: str
    history: List[Message]
