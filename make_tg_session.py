from telethon.sync import TelegramClient

from app.settings import Settings

client = TelegramClient(f"volumes/{Settings.TG_SESSION}", Settings.API_ID, Settings.API_HASH)
client.start("Your phone number")

client.send_message("me", 'Make session')
