from datetime import datetime


def get_timestamp() -> str:
    now = datetime.now()
    return now.strftime("%d/%m/%Y, %H:%M:%S")
