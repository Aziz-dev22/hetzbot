import os

ADMIN_ID = int(os.getenv("ADMIN_ID", 0))

def is_admin(user_id: int) -> bool:
    return user_id == ADMIN_ID

def gb_to_tb(gb: float) -> str:
    if gb >= 1024:
        return f"{gb/1024:.2f} TB"
    return f"{gb:.2f} GB"

def format_expiry(date):
    return date.strftime("%Y/%m/%d")
