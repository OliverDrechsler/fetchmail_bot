import pytest
from unittest.mock import MagicMock
import telebot.types
from config import config_util
from fetchmail_bot import get_allowed


# Mocking the necessary parts for testing
class MockMessage:
    def __init__(self, chat_id):
        self.chat = MagicMock()
        self.chat.id = chat_id
        self.from_user = MagicMock()
        self.from_user.id = "123456789"


class MockConfig:
    def __init__(self, telegram_chat_nr, list_id):
        self.telegram_chat_nr = telegram_chat_nr
        self.list_id = list_id


@pytest.fixture
def allowed_user_config():
    return MockConfig(telegram_chat_nr="12345", list_id=["123456789"])


@pytest.fixture
def disallowed_user_config():
    return MockConfig(telegram_chat_nr="12345", list_id=["987654321"])


def test_get_allowed_with_allowed_user_in_correct_chat(allowed_user_config):
    message = MockMessage(chat_id="12345")
    assert get_allowed(message=message, config=allowed_user_config) == True


def test_get_allowed_with_allowed_user_in_incorrect_chat(allowed_user_config):
    message = MockMessage(chat_id="54321")
    assert get_allowed(message=message, config=allowed_user_config) == False


def test_get_allowed_with_disallowed_user_in_correct_chat(disallowed_user_config):
    message = MockMessage(chat_id="12345")
    assert get_allowed(message=message, config=disallowed_user_config) == False
