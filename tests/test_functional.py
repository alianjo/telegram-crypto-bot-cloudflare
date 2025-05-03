import sys
import os
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from robot import start

class DummyUser:
    def __init__(self, name):
        self.first_name = name

class DummyMessage:
    async def reply_text(self, text, reply_markup=None):
        assert "رمزارز مورد نظر رو انتخاب کن" in text
        print(f"Bot says: {text}")

class DummyUpdate:
    def __init__(self):
        self.effective_user = DummyUser("Ali")
        self.message = DummyMessage()

class DummyContext:
    def __init__(self):
        self.bot = None

@pytest.mark.asyncio
async def test_start_command():
    update = DummyUpdate()
    context = DummyContext()
    await start(update, context)
