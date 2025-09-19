from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import router
from dotenv import load_dotenv
import os

# Load environment variables from .env (for local dev)
load_dotenv()

# Initialize FastAPI app
app = FastAPI(title="MindMitra Chatbot")

# ✅ Dynamic CORS setup
# Allow localhost during dev and frontend origin in production (set via env var)
FRONTEND_URL = os.environ.get("FRONTEND_URL", "http://localhost:5173")
origins = [
    FRONTEND_URL,
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(router, prefix="/api")

# Optional root endpoint
@app.get("/")
def root():
    return {"message": "MindMitra Chatbot API is running 🚀"}

# Entry point for Render (uvicorn will use this)
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))  # Render sets PORT env var automatically
    uvicorn.run(app, host="0.0.0.0", port=port)
