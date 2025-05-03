import sys
import os
import pytest
from telegram import Update

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from robot import get_crypto_price

class DummyMessage:
    def __init__(self, text):
        self.text = text
    async def reply_text(self, text, reply_markup=None):
        print(f"Bot says: {text}")
        return text

class DummyContext:
    def __init__(self):
        self.bot = None
        
@pytest.mark.asyncio
async def test_get_crypto_price_bitcoin():
    update = Update(update_id=1, message=DummyMessage("بیت‌کوین"))
    context = DummyContext()
    response = await get_crypto_price(update, context)
    assert response is None
