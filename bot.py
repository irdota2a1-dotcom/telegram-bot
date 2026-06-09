from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = "8839805791:AAFllOCwnvWo9XjTScgxJW2kpRg3I_FTAr0"
ADMIN_ID = 318070412  # آیدی خودت

# فقط برای پیام خوشامدگویی
welcomed_users = set()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "سلام 👋\nبه پشتیبانی فروشگاه خوش آمدید."
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text

    # پیام خوشامدگویی فقط بار اول
    if user_id not in welcomed_users:
        welcomed_users.add(user_id)
        await update.message.reply_text(
            "سلام، وقت بخیر 🌹\n\n"
            "از ارتباط شما سپاسگزاریم. پیام شما دریافت شد و در حال بررسی است. "
            "تیم پشتیبانی در اسرع وقت پاسخگوی شما خواهد بود. لطفاً تا زمان دریافت پاسخ منتظر بمانید."
        )

    # ارسال پیام کاربر به ادمین
    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=f"📩 پیام جدید از کاربر:\n\n{text}\n\nUser ID: {user_id}"
    )

async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # فقط ادمین اجازه پاسخ دارد
    if update.effective_user.id != ADMIN_ID:
        return

    try:
        user_id = int(context.args[0])
        msg = " ".join(context.args[1:])

        await context.bot.send_message(
            chat_id=user_id,
            text=f"📢 پاسخ پشتیبانی:\n\n{msg}"
        )

        await update.message.reply_text("✅ پاسخ ارسال شد")

    except:
        await update.message.reply_text(
            "فرمت درست:\n/reply user_id message"
        )

app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
app.add_handler(CommandHandler("reply", reply))

print("Bot is running...")
app.run_polling()
