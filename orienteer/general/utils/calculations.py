from datetime import timedelta


def calculate_fine(time: timedelta) -> int:
    return int(round(((((time.total_seconds() / 60) ** 0.5) * 1.9641855033) / 1.5) + 25, 0))
