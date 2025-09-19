from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import router
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

app = FastAPI(title="MindMitra Chatbot")

# ✅ CORS setup to allow requests from your frontend
origins = [
    "http://localhost:5173",  # Vite React dev server
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],   # GET, POST, PUT, DELETE, etc.
    allow_headers=["*"],   # Authorization, Content-Type, etc.
)

# Register routes
app.include_router(router, prefix="/api")

# Optional root endpoint
@app.get("/")
def root():
    return {"message": "MindMitra Chatbot API is running 🚀"}
