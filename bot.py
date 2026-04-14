from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup
import config

bot = Bot(token=config.BOT_TOKEN)

def send_job(job):
    try:
        keyboard = [
            [InlineKeyboardButton("🔗 Apply Now", url=job["link"])]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        text = f"""
🚀 {job['title']}
📌 Source: {job['source']}
"""

        bot.send_message(
            chat_id=config.CHAT_ID,
            text=text,
            reply_markup=reply_markup
        )

    except Exception as e:
        print("[ERROR] Telegram send failed:", e)