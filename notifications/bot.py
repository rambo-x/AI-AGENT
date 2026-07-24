import subprocess
from database.state_manager import StateManager

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)

from config import TELEGRAM_BOT_TOKEN
data = StateManager().get("backend")

from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 TripleSide AI Agent aktif\n\n"
        "Command:\n"
        "/status - status agent\n"
        "/backend - status backend\n"
        "/pm2 - daftar PM2"
    )


async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "✅ Agent online\n"
        "Scheduler: running\n"
        "Monitor: active"
    )


async def pm2(update: Update, context: ContextTypes.DEFAULT_TYPE):

    try:
        result = subprocess.run(
            ["pm2", "list"],
            capture_output=True,
            text=True,
            timeout=10,
        )

        output = result.stdout

        if len(output) > 3500:
            output = output[-3500:]

        await update.message.reply_text(
            f"```\n{output}\n```",
            parse_mode="Markdown"
        )

    except Exception as e:
        await update.message.reply_text(
            f"Error PM2: {e}"
        )


async def backend(update: Update, context: ContextTypes.DEFAULT_TYPE):

    data = StateManager().get("backend")

    if not data:
        await update.message.reply_text(
            "⚠️ Data backend belum tersedia"
        )
        return

    text = (
        "🖥 TripleSide Backend\n\n"
        f"Name: {data.get('name')}\n"
        f"Status: {data.get('status')}\n"
        f"Restart: {data.get('restart')}\n"
        f"CPU: {data.get('cpu')}%\n"
        f"Memory: {round(data.get('memory',0)/1024/1024,2)} MB\n"
    )

    await update.message.reply_text(text)

async def logs(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not context.args:
        await update.message.reply_text(
            "Gunakan:\n/logs backend"
        )
        return

    service = context.args[0]

    if service != "backend":
        await update.message.reply_text(
            "Service tersedia:\nbackend"
        )
        return

    try:
        result = subprocess.run(
            [
                "pm2",
                "logs",
                "triplesidestudio-backend",
                "--lines",
                "20",
                "--nostream"
            ],
            capture_output=True,
            text=True,
            timeout=15,
        )

        output = result.stdout + result.stderr

        if not output:
            output = "Tidak ada log."

        # batas Telegram 4096 karakter
        if len(output) > 3500:
            output = output[-3500:]

        await update.message.reply_text(
            f"📋 Backend Logs\n\n{output}"
        )

    except Exception as e:
        await update.message.reply_text(
            f"❌ Gagal mengambil log:\n{e}"
        )

def start_bot():

    app = Application.builder().token(
        TELEGRAM_BOT_TOKEN
    ).build()

    app.add_handler(
        CommandHandler("start", start)
    )

    app.add_handler(
        CommandHandler("status", status)
    )

    app.add_handler(
        CommandHandler("pm2", pm2)
    )

    app.add_handler(
        CommandHandler("backend", backend)
    )
 
    app.add_handler(
    	CommandHandler("restart", restart)
    )

    app.add_handler(
    CommandHandler("logs", logs)
    )

    app.add_handler(
    CommandHandler("restart", restart)
    )

    app.add_handler(
    CommandHandler("confirm", confirm)
    )

    app.run_polling(
    stop_signals=None
    )

async def restart(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not context.args:
        await update.message.reply_text(
            "Gunakan:\n/restart backend"
        )
        return

    service = context.args[0]

    if service != "backend":
        await update.message.reply_text(
            "Service yang tersedia:\nbackend"
        )
        return

    try:
        result = subprocess.run(
            [
                "pm2",
                "restart",
                "triplesidestudio-backend"
            ],
            capture_output=True,
            text=True,
            timeout=30,
        )

        if result.returncode == 0:
            await update.message.reply_text(
                "✅ Backend berhasil direstart"
            )
        else:
            await update.message.reply_text(
                f"❌ Restart gagal:\n{result.stderr}"
            )

    except Exception as e:
        await update.message.reply_text(
            f"Error restart: {e}"
        )


pending_restart = {}

async def restart(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = str(update.effective_chat.id)

    if user_id != str(TELEGRAM_CHAT_ID):
        await update.message.reply_text(
            "❌ Tidak memiliki akses."
        )
        return

    if not context.args:
        await update.message.reply_text(
            "Gunakan:\n/restart backend"
        )
        return

    if context.args[0] != "backend":
        await update.message.reply_text(
            "Service tersedia:\nbackend"
        )
        return

    pending_restart[user_id] = "backend"

    await update.message.reply_text(
        "⚠️ Konfirmasi restart backend\n\n"
        "Ketik:\n"
        "/confirm"
    )


async def confirm(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = str(update.effective_chat.id)

    if user_id != str(TELEGRAM_CHAT_ID):
        await update.message.reply_text(
            "❌ Tidak memiliki akses."
        )
        return

    service = pending_restart.get(user_id)

    if not service:
        await update.message.reply_text(
            "Tidak ada restart yang menunggu."
        )
        return

    await update.message.reply_text(
        "🔄 Restart backend berjalan..."
    )

    try:
        result = subprocess.run(
            [
                "pm2",
                "restart",
                "triplesidestudio-backend"
            ],
            capture_output=True,
            text=True,
            timeout=30,
        )

        if result.returncode == 0:
            await update.message.reply_text(
                "✅ Backend berhasil direstart"
            )
        else:
            await update.message.reply_text(
                f"❌ Restart gagal:\n{result.stderr}"
            )

    except Exception as e:
        await update.message.reply_text(
            f"❌ Error:\n{e}"
        )

    pending_restart.pop(user_id, None)
