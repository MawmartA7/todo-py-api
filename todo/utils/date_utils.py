from datetime import datetime

def format_datetime_to_response_date(date: datetime) -> str:
    return date.isoformat(timespec='microseconds').replace('+00:00', 'Z')