from datetime import datetime


def calculate_fine(time: datetime.timestamp) -> int:
    return int(round(((((time.total_seconds() / 60) ** 0.5) * 1.9641855033) / 1.5) + 25, 0))
