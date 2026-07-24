"""
Telegram Runner

Telegram interface for TripleSide AI Agent.

Commands:
    /status
    /report
    /help
    /approvals
"""

import json

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

from config import TELEGRAM_BOT_TOKEN as TOKEN

from ai.storage.storage import Storage



# ==================================================
# COMMAND: /status
# ==================================================

async def status_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    await update.message.reply_text(
        "TripleSide AI Agent is online."
    )



# ==================================================
# COMMAND: /report
# ==================================================

async def report_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    storage = Storage(".")


    report = storage.load(
        "decision_report.json",
        {}
    )


    await update.message.reply_text(

        json.dumps(
            report,
            indent=2,
            ensure_ascii=False
        )[:4000]

    )



# ==================================================
# COMMAND: /help
# ==================================================

async def help_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    message = """
TripleSide AI Agent Commands:

/status
System status

/report
Latest AI decision report

/approvals
Show pending approval requests
"""

    await update.message.reply_text(
        message
    )



# ==================================================
# COMMAND: /approvals
# ==================================================

async def approvals_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    storage = Storage(".")


    data = storage.load(
        "approval_requests.json",
        {
            "requests":[]
        }
    )


    requests = data.get(
        "requests",
        []
    )


    pending = [

        item

        for item in requests

        if item.get("status") == "pending"

    ]



    if not pending:

        await update.message.reply_text(
            "Tidak ada approval pending."
        )

        return



    message = (
        "Pending Approval:\n\n"
    )


    for item in pending:

        message += (

            f"ID:\n"
            f"{item.get('id')}\n\n"

            f"Problem:\n"
            f"{item.get('problem')}\n\n"

            f"Action:\n"
            f"{item.get('action')}\n\n"

            f"Status:\n"
            f"{item.get('status')}\n"

            "----------------\n\n"

        )


    await update.message.reply_text(
        message[:4000]
    )



# ==================================================
# TEXT HANDLER
# ==================================================

async def text_message_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    result = {

        "message":
            "Command tidak dikenal. Gunakan /help"

    }


    if isinstance(result, dict) and "message" in result:


        await update.message.reply_text(
            result["message"][:4000]
        )


    else:


        await update.message.reply_text(

            json.dumps(
                result,
                indent=2,
                ensure_ascii=False
            )[:4000]

        )



# ==================================================
# MAIN
# ==================================================

def main():


    if not TOKEN:

        raise Exception(
            "TELEGRAM_BOT_TOKEN missing"
        )



    app = (

        Application
        .builder()
        .token(TOKEN)
        .build()

    )



    app.add_handler(

        CommandHandler(
            "status",
            status_command
        )

    )



    app.add_handler(

        CommandHandler(
            "report",
            report_command
        )

    )



    app.add_handler(

        CommandHandler(
            "help",
            help_command
        )

    )



    app.add_handler(

        CommandHandler(
            "approvals",
            approvals_command
        )

    )



    app.add_handler(

        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            text_message_handler
        )

    )



    print(
        "Telegram AI Agent started"
    )



    app.run_polling(
        stop_signals=None
    )



if __name__ == "__main__":

    main()
