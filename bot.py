import os
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

PORT = int(os.environ.get("PORT", "10000"))

GROUP_LINK = "https://t.me/+2pU_A8RyKYA3Yjk9"


class WebHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path in ("/", "/index.html"):
            try:
                with open("index.html", "rb") as f:
                    data = f.read()

                self.send_response(200)
                self.send_header("Content-Type", "text/html")
                self.send_header("Content-Length", str(len(data)))
                self.end_headers()
                self.wfile.write(data)
            except FileNotFoundError:
                self.send_response(404)
                self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        pass


def start_web():
    server = ThreadingHTTPServer(("0.0.0.0", PORT), WebHandler)
    server.serve_forever()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton(
                "🎲 JOIN JANU LUDO CLUB",
                url=GROUP_LINK
            )
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    message = (
        "🎲🔥 JANU LUDO CLUB\n\n"
        "Welcome to JANU LUDO CLUB! 🎮\n\n"
        "💰 Easy & Simple Ludo Play\n"
        "⚡ Fast Game Updates\n"
        "💸 Quick Withdrawals\n"
        "🎁 Exciting Offers & Cashback\n\n"
        "👇 हमारे official group में join करें "
        "और game updates पाएं!"
    )

    await update.message.reply_text(
        message,
        reply_markup=reply_markup
    )


async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "✅ Bot चालू है भाई!\n"
        "नीचे दिए button से JANU LUDO CLUB join करें 👇",
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    "🎲 JOIN JANU LUDO CLUB",
                    url=GROUP_LINK
                )
            ]
        ])
    )


def main():
    token = os.environ.get("BOT_TOKEN")

    if not token:
        raise RuntimeError("BOT_TOKEN environment variable is missing")

    threading.Thread(target=start_web, daemon=True).start()

    app = ApplicationBuilder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, reply)
    )

    print("Bot starting...")
    app.run_polling()


if __name__ == "__main__":
    main()
