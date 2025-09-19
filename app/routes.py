from fastapi import APIRouter
from app.models import ChatRequest, ChatResponse, Message
from app.services import memory, llm_service, spring_api

router = APIRouter()

quick_actions = [
    {"action": "View Appointments", "role": "patient"},
    {"action": "Book Appointment", "role": "patient"},
    {"action": "Mood Tracker", "role": "patient"},
]

@router.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    username, role, message, intent_override = req.username, req.role, req.message, req.intent

    # 1️⃣ Add user message to memory
    memory.add_message(username, "user", message)

    # 2️⃣ Get conversation history from memory
    history = memory.get_history(username)

    # 3️⃣ Analyze message with history (continuity enabled)
    ai_result = (
        llm_service.analyze_message(message, role, history)
        if not intent_override
        else {"intent": intent_override, "reply": ""}
    )
    intent = intent_override or ai_result["intent"]
    bot_reply = ai_result.get("reply", "")

    # 4️⃣ Role-based actionable logic
    role_lower = role.lower()

    # Patient
    if role_lower == "patient":
        if intent == "retrieve_appointments":
            data = spring_api.get_appointments(username)
            bot_reply = f"📅 Your appointments:\n{data}"

        elif intent == "view_doctors":
            data = spring_api.get_doctors()
            bot_reply = f"🧑‍⚕️ Available doctors:\n{data}"

        elif intent == "view_journal":
            data = spring_api.get_journal(username)
            bot_reply = f"📖 Your journal entries:\n{data}"

    # Doctor
    elif role_lower == "doctor":
        if intent == "retrieve_appointments":
            data = spring_api.get_doctor_appointments(username)
            bot_reply += f"\n\n👨‍⚕️ Scheduled appointments: {data}"

        elif intent == "view_totals":
            totals = spring_api.get_doctor_totals(username)
            bot_reply = f"📊 Stats: {totals}"

        elif intent == "update_status":
            appt_id = ai_result.get("appointment_id")
            new_status = ai_result.get("status")
            if appt_id and new_status:
                result = spring_api.update_appointment_status(appt_id, new_status)
                bot_reply = (
                    f"🔄 Appointment {appt_id} updated to {new_status}.\n📄 {result}"
                )
            else:
                bot_reply = "⚠️ Missing appointment ID or status."

    # Admin
    elif role_lower == "admin":
        if intent == "retrieve_appointments":
            data = spring_api.get_all_appointments()
            bot_reply += f"\n\n📅 All appointments: {data}"

        elif intent == "update_status":
            appt_id = ai_result.get("appointment_id")
            new_status = ai_result.get("status")
            if appt_id and new_status:
                result = spring_api.update_appointment_status(appt_id, new_status)
                bot_reply = (
                    f"🔄 Appointment {appt_id} updated to {new_status}.\n📄 {result}"
                )
            else:
                bot_reply = "⚠️ Missing appointment ID or status."

        elif intent == "view_totals":
            totals = spring_api.get_admin_totals()
            bot_reply = f"📊 Overall system stats: {totals}"

        elif intent == "create_doctor":
            doctor_name = ai_result.get("doctor_name")
            specialization = ai_result.get("specialization")
            if doctor_name and specialization:
                result = spring_api.create_doctor_profile(
                    {"name": doctor_name, "specialization": specialization}
                )
                bot_reply = (
                    f"✅ Doctor profile created: {doctor_name} ({specialization}).\n📄 {result}"
                )
            else:
                bot_reply = "⚠️ Missing doctor name or specialization."

    # 5️⃣ Add bot reply to memory
    memory.add_message(username, "bot", bot_reply)

    # 6️⃣ Return response with full updated history (validated by Pydantic)
    updated_history = memory.get_history(username)

    return ChatResponse(
        reply=bot_reply,
        history=[Message(**msg) for msg in updated_history]  # ensure schema compliance
    )
