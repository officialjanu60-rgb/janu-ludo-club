import os
import threading
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

PORT = int(os.environ.get("PORT", "10000"))


class WebHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path in ("/", "/index.html"):
            with open("index.html", "rb") as f:
                data = f.read()

            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        pass


def start_web():
    server = ThreadingHTTPServer(("0.0.0.0", PORT), WebHandler)
    server.serve_forever()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎲 Janu Ludo Club में आपका स्वागत है!\n\n"
        "Bot चालू है ✅"
    )


async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "✅ Bot चालू है भाई!\n"
        "आपका मैसेज मिल गया।"
    )


def main():
    token = os.environ.get("BOT_TOKEN")

    if not token:
        raise RuntimeError("BOT_TOKEN environment variable missing")

    threading.Thread(target=start_web, daemon=True).start()

    app = ApplicationBuilder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply))

    print("Bot starting...")
    app.run_polling()


if __name__ == "__main__":
    main()
