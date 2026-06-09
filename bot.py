import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "8839805791:AAFllOCwnvWo9XjTScgxJW2kpRg3I_FTAr0"
ADMIN_ID = 318070412

pending_users = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "جناب، سلام 👋\nبه پشتیبانی خوش آمدید."
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.chat_id
    text = update.message.text

    await update.message.reply_text(
        "پیام شما دریافت شد 🤝 لطفاً صبر کنید..."
    )

    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=f"📩 پیام جدید:\n{text}\n\nUser ID: {user_id}"
    )

    pending_users[user_id] = True

    await asyncio.sleep(300)

    if pending_users.get(user_id):
        await context.bot.send_message(
            chat_id=user_id,
            text="جناب 🌟 هنوز در حال بررسی هستیم..."
        )

async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.chat_id != ADMIN_ID:
        return

    try:
        user_id = int(context.args[0])
        msg = " ".join(context.args[1:])

        await context.bot.send_message(chat_id=user_id, text=msg)
        pending_users[user_id] = False

    except:
        await update.message.reply_text("فرمت: /reply id message")

app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
app.add_handler(CommandHandler("reply", reply))

print("Bot is running...")
app.run_polling()
if name == "main":
    app.run_polling()
