import pytest
import telebot
from unittest.mock import patch, MagicMock
import logging
from subprocess import CalledProcessError

from fetchmail_bot import (
    fetch_mail_process,
)  # Assuming the function is in a module named your_module


class MockMessage:
    def __init__(self, chat_id):
        self.chat = MagicMock()
        self.chat.id = chat_id
        self.from_user = MagicMock()
        self.from_user.id = "123456789"


class TestFetchMailProcess:
    @patch("fetchmail_bot.subprocess.check_output")
    def test_fetch_mail_process_success(self, mock_check_output):
        mock_check_output.return_value = "Mail fetched successfully"
        bot = MagicMock(telebot.TeleBot)
        message = MagicMock(telebot.types.Message)
        logger = MagicMock(logging.Logger)
        fetch_mail_process("testuser", bot, message, logger)
        bot.reply_to.assert_called_once_with(
            message, "New mails fetched - process completed."
        )
        logger.info.assert_called_with(
            msg="fetch mail process completed: Mail fetched successfully"
        )

    @patch(
        "fetchmail_bot.subprocess.check_output",
        side_effect=CalledProcessError(
            returncode=1,
            cmd="fetchmail",
            output="fetchmail: another foreground fetchmail is running at",
        ),
    )
    def test_fetch_mail_process_already_running(self, mock_check_output):
        bot = MagicMock(telebot.TeleBot)
        message = MagicMock(telebot.types.Message)
        logger = MagicMock(logging.Logger)
        fetch_mail_process("testuser", bot, message, logger)
        bot.reply_to.assert_called_once_with(
            message, "Another fetchmail process is running - retry later again."
        )
        logger.info.assert_called_with(
            "Another fetchmail process is running: fetchmail: another foreground fetchmail is running at"
        )

    @patch(
        "fetchmail_bot.subprocess.check_output", side_effect=Exception("General error")
    )
    def test_fetch_mail_process_exception_handling(self, mock_check_output):
        bot = MagicMock(telebot.TeleBot)
        message = MockMessage(chat_id="12345")
        logger = MagicMock(logging.Logger)
        fetch_mail_process("testuser", bot, message, logger)
        bot.send_message.assert_called_once_with(
            message.chat.id, "Error during fetch mail process: General error"
        )
        logger.info.assert_called_with(
            msg="Error during fetch mail process: General error"
        )
