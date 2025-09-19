from datetime import datetime, timezone
from typing import Dict, List, Any

# Stores conversation history and temporary slots for users
memory_store: Dict[str, List[Dict[str, Any]]] = {}
slot_store: Dict[str, Dict[str, Any]] = {}

def add_message(username: str, sender: str, text: str) -> None:
    """
    Store a message in memory with timestamp.
    sender: "user" or "bot"
    """
    if username not in memory_store:
        memory_store[username] = []
    memory_store[username].append({
        "role": sender,  # "user" or "bot"
        "message": text,
        "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds")
    })

def get_history(username: str) -> List[Dict[str, Any]]:
    """
    Get conversation history for a user.
    """
    return memory_store.get(username, [])

def clear_history(username: str) -> None:
    """
    Reset chat history for a user.
    """
    memory_store.pop(username, None)

def set_slots(username: str, slots: Dict[str, Any]) -> None:
    """
    Save temporary slot data (e.g., appointment booking flow).
    """
    slot_store[username] = slots

def get_slots(username: str) -> Dict[str, Any] | None:
    """
    Retrieve temporary slot data.
    """
    return slot_store.get(username)

def clear_slots(username: str) -> None:
    """
    Clear temporary slot data for a user.
    """
    slot_store.pop(username, None)
