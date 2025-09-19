import json
import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate

# Load environment variables
env_path = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(dotenv_path=env_path)
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Initialize LLM
llm = ChatGroq(
    api_key=GROQ_API_KEY,
    model="llama-3.3-70b-versatile",
    temperature=0.0,
)

# Prompt for intent classification
intent_prompt = ChatPromptTemplate.from_messages([
    ("system",
     "You are an intent classification assistant for a mental health chatbot.\n"
     "Classify the user's message into a valid intent for their role and extract details.\n\n"
     "Valid intents by role:\n"
     "Patient → retrieve_appointments, book_appointment, cancel_appointment, general_chat\n"
     "Doctor → retrieve_appointments, view_totals, update_status, general_chat\n"
     "Admin → retrieve_appointments, update_status, view_totals, create_doctor, general_chat\n\n"
     "If intent is one of:\n"
     "- book_appointment → extract: doctor, date, time\n"
     "- update_status → extract: appointment_id, status\n"
     "- create_doctor → extract: doctor_name, specialization\n"
     "⚠️ Always return strictly JSON. Null if not applicable."),
    ("human", "Role: {role}\nMessage: {message}")
])

def classify_intent(message: str, role: str) -> dict:
    chain = intent_prompt | llm
    response = chain.invoke({"message": message, "role": role})
    try:
        result = json.loads(response.content)
        print("Classified Intent:", result)
    except Exception:
        result = {
            "intent": "general_chat",
            "doctor": None,
            "date": None,
            "time": None,
            "appointment_id": None,
            "status": None,
            "doctor_name": None,
            "specialization": None
        }
    return result
