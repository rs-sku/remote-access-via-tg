import os


class Settings:
    TOKEN = os.getenv("TOKEN")
    MAX_SIZE = int(os.getenv("MAX_SIZE"))
