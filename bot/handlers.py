from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from bot.keyboards import main_menu, servers_menu, buy_menu
from bot.db import get_user, add_user
from bot.hcloud import get_servers
from bot.utils import is_admin

ADMIN_ID = int(os.getenv("ADMIN_ID"))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    add_user(user.id, user.username, user.first_name)
    
    if is_admin(user.id):
        text = f"سلام ادمین {user.first_name} 👋\nبه پنل HetzBot خوش اومدی"
        keyboard = main_menu(is_admin=True)
    else:
        text = f"سلام {user.first_name} 👋\nبه ربات خرید سرور هتزنر خوش اومدی"
        keyboard = main_menu(is_admin=False)
    
    await update.message.reply_text(text, reply_markup=keyboard)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    
    if data == "buy_server":
        await query.edit_message_text("پلن مورد نظر رو انتخاب کن:", reply_markup=buy_menu())
    elif data == "my_servers":
        servers = get_servers(query.from_user.id)
        await query.edit_message_text("سرورهای شما:", reply_markup=servers_menu(servers))
    elif data == "back":
        await query.edit_message_text("منو اصلی:", reply_markup=main_menu(is_admin=is_admin(query.from_user.id)))
