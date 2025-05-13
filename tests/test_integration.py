import sys
import os
import pytest
from unittest.mock import AsyncMock, MagicMock

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from robot import button_handler

class DummyQuery:
    def __init__(self, data, chat_id=1234):
        self.data = data
        self.message = MagicMock()
        self.message.chat_id = chat_id
        self.answer = AsyncMock()

class DummyUpdate:
    def __init__(self, data):
        self.callback_query = DummyQuery(data)

class DummyContext:
    def __init__(self):
        self.bot = MagicMock()
        self.bot.send_message = AsyncMock()

@pytest.mark.asyncio
async def test_button_handler_bitcoin():
    update = DummyUpdate("bitcoin")
    context = DummyContext()

    await button_handler(update, context)

    context.bot.send_message.assert_called_once()
    args, kwargs = context.bot.send_message.call_args
    assert "💲 قیمت بیت‌کوین" in kwargs['text']

@pytest.mark.asyncio
async def test_button_handler_all_prices():
    update = DummyUpdate("all")
    context = DummyContext()

    await button_handler(update, context)

    context.bot.send_message.assert_called_once()
    args, kwargs = context.bot.send_message.call_args
    assert "💸 قیمت لحظه‌ای" in kwargs['text']
