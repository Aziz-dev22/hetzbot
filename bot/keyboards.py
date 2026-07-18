from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def main_menu(is_admin: bool):
    buttons = [
        [InlineKeyboardButton("🛒 خرید سرور", callback_data="buy_server")],
        [InlineKeyboardButton("📦 سرورهای من", callback_data="my_servers")],
        [InlineKeyboardButton("💰 موجودی", callback_data="balance")],
        [InlineKeyboardButton("📞 پشتیبانی", callback_data="support")]
    ]
    if is_admin:
        buttons.append([InlineKeyboardButton("⚙️ پنل ادمین", callback_data="admin_panel")])
    buttons.append([InlineKeyboardButton("❌ خروج", callback_data="exit")])
    return InlineKeyboardMarkup(buttons)

def buy_menu():
    buttons = [
        [InlineKeyboardButton("CX22 - 2vCPU 4GB RAM - 2.99€", callback_data="buy_cx22")],
        [InlineKeyboardButton("CX32 - 2vCPU 8GB RAM - 5.83€", callback_data="buy_cx32")],
        [InlineKeyboardButton("CX42 - 4vCPU 16GB RAM - 11.89€", callback_data="buy_cx42")],
        [InlineKeyboardButton("🔙 بازگشت", callback_data="back")]
    ]
    return InlineKeyboardMarkup(buttons)

def servers_menu(servers: list):
    buttons = []
    for s in servers:
        buttons.append([InlineKeyboardButton(f"{s.name} - {s.status}", callback_data=f"server_{s.id}")])
    buttons.append([InlineKeyboardButton("🔙 بازگشت", callback_data="back")])
    return InlineKeyboardMarkup(buttons)
