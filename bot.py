import sqlite3
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, ContextTypes, filters

TOKEN = "8839805791:AAFllOCwnvWo9XjTScgxJW2kpRg3I_FTAr0"
ADMIN_ID = 318070412

# ---------------- DATABASE ----------------
conn = sqlite3.connect("bot.db", check_same_thread=False)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS tickets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    text TEXT
)
""")
conn.commit()

# ---------------- USER MESSAGE ----------------
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text

    cur.execute("INSERT INTO tickets (user_id, text) VALUES (?, ?)", (user_id, text))
    conn.commit()

    ticket_id = cur.lastrowid

    keyboard = [
        [InlineKeyboardButton("💬 پاسخ", callback_data=f"reply_{user_id}")]
    ]

    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=f"🧾 تیکت #{ticket_id}\n\n{text}\n\n👤 User: {user_id}",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

    await update.message.reply_text(
        "🌹 پیام شما ثبت شد (تیکت دریافت شد)"
    )

# ---------------- ADMIN DASHBOARD ----------------
async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    keyboard = [
        [InlineKeyboardButton("📊 آمار", callback_data="stats")],
        [InlineKeyboardButton("📩 تیکت‌ها", callback_data="tickets")]
    ]

    await update.message.reply_text(
        "🖥 پنل مدیریت حرفه‌ای",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# ---------------- STATS ----------------
async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    cur.execute("SELECT COUNT(*) FROM tickets")
    total = cur.fetchone()[0]

    cur.execute("SELECT COUNT(DISTINCT user_id) FROM tickets")
    users = cur.fetchone()[0]

    await query.edit_message_text(
        f"📊 آمار سیستم:\n\n👥 کاربران: {users}\n📩 تیکت‌ها: {total}",
        reply_markup=back_btn()
    )

# ---------------- TICKETS LIST ----------------
async def tickets(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    cur.execute("SELECT id, user_id, text FROM tickets ORDER BY id DESC LIMIT 10")
    rows = cur.fetchall()

    text = "📩 آخرین تیکت‌ها:\n\n"
    for r in rows:
        text += f"🧾 #{r[0]} | 👤 {r[1]}\n{r[2]}\n\n"

    await query.edit_message_text(text, reply_markup=back_btn())

# ---------------- REPLY BUTTON ----------------
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data.startswith("reply_"):
        user_id = query.data.split("_")[1]
        context.user_data["reply_to"] = user_id

        await query.edit_message_text(
            "✍️ پیام خود را بنویس تا برای کاربر ارسال شود"
        )

# ---------------- ADMIN REPLY MESSAGE ----------------
async def admin_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    if "reply_to" in context.user_data:
        user_id = context.user_data["reply_to"]

        await context.bot.send_message(
            chat_id=user_id,
            text=f"📢 پاسخ پشتیبانی:\n\n{update.message.text}"
        )

        await update.message.reply_text("✅ ارسال شد")

        del context.user_data["reply_to"]

# ---------------- BACK BUTTON ----------------
def back_btn():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 برگشت", callback_data="back")]
    ])

async def back(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        "🖥 پنل مدیریت حرفه‌ای",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("📊 آمار", callback_data="stats")],
            [InlineKeyboardButton("📩 تیکت‌ها", callback_data="tickets")]
        ])
    )

# ---------------- ROUTER ----------------
async def router(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query

    if query.data == "stats":
        await stats(update, context)
    elif query.data == "tickets":
        await tickets(update, context)
    elif query.data == "back":
        await back(update, context)
    elif query.data.startswith("reply_"):
        await button_handler(update, context)

# ---------------- RUN ----------------
app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("admin", admin))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
app.add_handler(MessageHandler(filters.TEXT & filters.User(ADMIN_ID), admin_reply))
app.add_handler(CallbackQueryHandler(router))

print("Bot is running...")
app.run_polling()
