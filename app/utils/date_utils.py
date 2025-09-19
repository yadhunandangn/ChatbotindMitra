from datetime import datetime

def normalize_datetime(date_str, time_str=None):
    try:
        if time_str:
            return str(datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %I:%M %p"))
        else:
            return str(datetime.strptime(date_str, "%Y-%m-%d"))
    except Exception:
        return None
