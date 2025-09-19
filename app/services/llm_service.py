from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from app.services.intent_service import classify_intent
from app.services.memory import get_history
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment
env_path = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(dotenv_path=env_path)
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Initialize LLM
llm = ChatGroq(
    api_key=GROQ_API_KEY,
    model="llama-3.3-70b-versatile",
    temperature=0.3,  # slightly warmer for friendly conversation
)

# Prompt template for role-aware, context-aware responses
chat_prompt = ChatPromptTemplate.from_messages([
    ("system",
     "You are MindMitra, a mental health support AI platform assistant.\n"
     "You help users (patients), doctors, and admins manage appointments and doctor profiles.\n"
     "Tone and style based on role:\n"
     "- Patients → empathetic, friendly, concise, acknowledge past messages, ask only for missing info.\n"
     "- Doctors/Admins → professional, concise, focus on actionable info.\n"
     "Always provide actionable guidance, follow the detected intent and extracted details strictly."
    ),
    ("human",
     "Role: {role}\nIntent: {intent}\nMessage: {message}\nConversation History:\n{history}\n\n"
     "Reply in the same conversational style and maintain continuity.")
])

def analyze_message(message: str, role: str = "patient", history: list[dict] = None) -> dict:
    """
    Combines intent classification and actionable LLM reply.
    Maintains conversation continuity by including past messages.
    Returns a dict with 'intent', extracted details, and 'reply'.
    """
    # 1️⃣ Detect intent & extract details
    intent_result = classify_intent(message, role)

    # 2️⃣ Format conversation history for LLM
    history_str = ""
    if history:
        for msg in history[-10:]:  # last 10 messages for context
            speaker = "User" if msg["role"] == "user" else "Bot"
            # Add slight formatting for readability
            history_str += f"{speaker}: {msg['message']}\n"

    # 3️⃣ Generate actionable, role-aware reply
    chain = chat_prompt | llm
    response = chain.invoke({
        "message": message,
        "role": role,
        "intent": intent_result["intent"],
        "history": history_str
    })

    # 4️⃣ Clean up reply
    reply_text = response.content.strip()

    # 5️⃣ Add reply to intent result
    intent_result["reply"] = reply_text
    return intent_result
