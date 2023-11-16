import threading as th
import time
from logging import getLogger

from django.conf import settings

from telegram import Bot
from telegram.constants import PARSEMODE_MARKDOWN

from utils.metaclasses import Singleton

logger = getLogger(__name__)


class Delayer:
    def __init__(self, max_bulk_size, delay_seconds):
        self.lock = th.Lock()
        self.bulk_size = 0
        self.max_bulk_size = max_bulk_size
        self.delay_seconds = delay_seconds

    def __enter__(self):
        with self.lock:
            self.bulk_size += 1

            if self.bulk_size >= self.max_bulk_size:
                time.sleep(self.delay_seconds)
                self.bulk_size = 0

    def __exit__(self, *args, **kwargs):
        pass


class Interface(metaclass=Singleton):
    def __init__(self):
        self.bot = Bot(token=settings.TELEGRAM_TOKEN)
        self.delayer = Delayer(max_bulk_size=30, delay_seconds=1)

    def _send(self, text):
        try:
            with self.delayer:
                self.bot.send_message(
                    chat_id=settings.TELEGRAM_CHAT_ID,
                    text=text,
                    parse_mode=PARSEMODE_MARKDOWN,
                )

        except Exception as e:
            logger.error(f"Unable to send a Telegram message: {e}")

    def send(self, text, async_=True):
        kwargs = {"text": text}

        if async_:
            thread = th.Thread(target=self._send, kwargs=kwargs)
            thread.start()
            return thread

        else:
            return self._send(**kwargs)
