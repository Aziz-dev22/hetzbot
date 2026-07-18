import asyncio, os
from telegram.ext import Application, CommandHandler, CallbackQueryHandler
from bot.handlers import start, button_handler
from bot.jobs import traffic_checker, expiry_notifier

async def main():
    app = Application.builder().token(os.getenv("BOT_TOKEN")).build()
    
    # هندلر ها
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    # جاب های زمانبندی
    # 11. چک ترافیک هر 10 دقیقه
    app.job_queue.run_repeating(traffic_checker, interval=600, first=10)
    # 12. نوتیف انقضا روزی 2 بار
    app.job_queue.run_repeating(expiry_notifier, interval=43200, first=60)

    print("HetzBot is running...")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
