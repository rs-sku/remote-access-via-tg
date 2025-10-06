from telegram.ext import ApplicationBuilder, MessageHandler

from app.settings import Settings
from app.virus import VirusBot

app = ApplicationBuilder().token(Settings.TOKEN).build()

app.add_handler(MessageHandler(None, VirusBot().handle_message))

app.run_polling()
