import sys
import os
import pytest
from telegram.ext import ContextTypes
from telegram import Update

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from robot import button_handler

class DummyCallbackQuery:
    def __init__(self, data):
        self.data = data
        self.message = type('obj', (object,), {'chat_id': 123})
    async def answer(self, text=None):
        return text

class DummyUpdate:
    def __init__(self, data):
        self.callback_query = DummyCallbackQuery(data)

class DummyBot:
    async def send_message(self, chat_id, text):
        return text

@pytest.mark.asyncio
async def test_button_handler_integration():
    update = DummyUpdate("bitcoin")
    context = type('obj', (object,), {'bot': DummyBot()})
    await button_handler(update, context)
