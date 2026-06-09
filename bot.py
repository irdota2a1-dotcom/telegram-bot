from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = "8839805791:AAFllOCwnvWo9XjTScgxJW2kpRg3I_FTAr0"

# برای اینکه فقط یک‌بار پیام خوشامدگویی بده
welcomed_users = set()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام 👋 به ربات پشتیبانی خوش آمدید")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    # فقط بار اول پیام خوشامدگویی بده
    if user_id not in welcomed_users:
        welcomed_users.add(user_id)

        await update.message.reply_text(
            "سلام، وقت بخیر 🌹\n\n"
            "از ارتباط شما سپاسگزاریم. پیام شما دریافت شد و در حال بررسی است. "
            "تیم پشتیبانی در اسرع وقت پاسخگوی شما خواهد بود. لطفاً تا زمان دریافت پاسخ منتظر بمانید."
        )

app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("Bot is running...")
app.run_polling()
