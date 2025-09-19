import os
from pathlib import Path
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from app.services.intent_service import classify_intent

# =========================
# Load environment variables (once)
# =========================
ENV = os.getenv("ENV", "development")

if ENV == "development":
    from dotenv import load_dotenv
    env_path = Path(__file__).resolve().parents[2] / ".env"
    load_dotenv(dotenv_path=env_path)

# Fetch GROQ API key
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError(
        "GROQ_API_KEY is missing! "
        "Set it in .env for local dev or in Render environment variables."
    )

# =========================
# Initialize LLM
# =========================
llm = ChatGroq(
    api_key=GROQ_API_KEY,
    model="llama-3.3-70b-versatile",
    temperature=0.3,
)

# =========================
# Chat Prompt Template
# =========================
chat_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are MindMitra, a mental health support AI platform assistant. "
        "Provide empathetic, informative responses. Tone and style should match the user's role."
    ),
    (
        "human",
        "Role: {role}\nIntent: {intent}\nMessage: {message}\nConversation History:\n{history}\n\n"
        "Reply in the same conversational style and maintain continuity."
    )
])

# =========================
# Analyze Message Function
# =========================
def analyze_message(message: str, role: str = "patient", history: list[dict] = None) -> dict:
    """
    Classify the intent of the message, and generate a reply using ChatGroq LLM.
    """
    # 1️⃣ Classify intent using your intent service
    intent_result = classify_intent(message, role)

    # 2️⃣ Prepare conversation history (last 10 messages)
    history_str = "".join([
        f"{'User' if msg['role']=='user' else 'Bot'}: {msg['message']}\n"
        for msg in (history or [])[-10:]
    ])

    # 3️⃣ Generate response from LLM
    try:
        chain = chat_prompt | llm
        response = chain.invoke({
            "message": message,
            "role": role,
            "intent": intent_result["intent"],
            "history": history_str
        })
        intent_result["reply"] = response.content.strip()
    except Exception as e:
        print("LLM Error:", e)
        intent_result["reply"] = "⚠️ Sorry, I couldn't process your request right now."

    return intent_result
