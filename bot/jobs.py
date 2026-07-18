from telegram.ext import ContextTypes
from bot.db import get_session, Server, User
from bot.hcloud import client
from datetime import datetime, timedelta

ADMIN_ID = int(os.getenv("ADMIN_ID"))

async def traffic_checker(context: ContextTypes.DEFAULT_TYPE):
    session = get_session()
    servers = session.query(Server).filter_by(is_active=True).all()
    
    for s in servers:
        hcloud_server = client.servers.get_by_id(s.hcloud_id)
        if hcloud_server:
            # محاسبه ترافیک مصرفی از API هتزنر
            traffic_gb = hcloud_server.included_traffic / (1024**3)
            s.traffic_used = traffic_gb
            
            # اگه 90 درصد ترافیک پر شد هشدار بده
            if s.traffic_used >= s.traffic_limit * 0.9:
                user = session.query(User).filter_by(telegram_id=s.telegram_id).first()
                if user:
                    text = f"⚠️ هشدار ترافیک\nسرور {s.name} به 90% محدودیت ترافیک رسیده.\nمصرف: {s.traffic_used:.2f}GB / {s.traffic_limit}GB"
                    await context.bot.send_message(chat_id=user.telegram_id, text=text)
    session.commit()
    session.close()

async def expiry_notifier(context: ContextTypes.DEFAULT_TYPE):
    session = get_session()
    now = datetime.now()
    three_days_later = now + timedelta(days=3)
    
    # سرورهایی که تا 3 روز دیگه منقضی میشن
    servers = session.query(Server).filter(
        Server.expiry_date <= three_days_later,
        Server.is_active == True
    ).all()
    
    for s in servers:
        user = session.query(User).filter_by(telegram_id=s.telegram_id).first()
        if user:
            days_left = (s.expiry_date - now).days
            text = f"⏰ سرور {s.name} تا {days_left} روز دیگه منقضی میشه.\nبرای تمدید به پنل مراجعه کن."
            await context.bot.send_message(chat_id=user.telegram_id, text=text)
    session.close()
