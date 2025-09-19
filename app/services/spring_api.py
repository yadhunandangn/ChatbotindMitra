import requests

BASE_URL = "http://localhost:8080/api"  # Spring Boot URL

def get_appointments(username):
    try:
        return requests.get(f"{BASE_URL}/auth/get-appointments/{username}", timeout=5).json()
    except Exception as e:
        return {"error": str(e)}

def book_appointment(data):
    try:
        return requests.post(f"{BASE_URL}/auth/book-appointment", json=data, timeout=5).json()
    except Exception as e:
        return {"error": str(e)}    

def cancel_appointment(username):
    try:
        return requests.delete(f"{BASE_URL}/appointments/{username}", timeout=5).json()
    except Exception as e:
        return {"error": str(e)}

def get_doctor_appointments(username):
    try:
        return requests.get(f"{BASE_URL}/doctor/{username}/appointments", timeout=5).json()
    except Exception as e:
        return {"error": str(e)}

def get_doctor_totals(username):
    try:
        return requests.get(f"{BASE_URL}/doctor/{username}/totals", timeout=5).json()
    except Exception as e:
        return {"error": str(e)}

def update_appointment_status(appt_id, status):
    try:
        return requests.put(f"{BASE_URL}/appointments/{appt_id}/status", json={"status": status}, timeout=5).json()
    except Exception as e:
        return {"error": str(e)}

def get_all_appointments():
    try:
        return requests.get(f"{BASE_URL}/appointments", timeout=5).json()
    except Exception as e:
        return {"error": str(e)}

def get_admin_totals():
    try:
        return requests.get(f"{BASE_URL}/admin/totals", timeout=5).json()
    except Exception as e:
        return {"error": str(e)}

def create_doctor_profile(data):
    try:
        return requests.post(f"{BASE_URL}/doctor", json=data, timeout=5).json()
    except Exception as e:
        return {"error": str(e)}
