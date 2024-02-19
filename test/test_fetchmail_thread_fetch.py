# import pytest
import telebot
from unittest.mock import patch, MagicMock
import logging
from subprocess import CalledProcessError
from bot import receive_msg


class MockMessage:
    def __init__(self, chat_id):
        self.chat = MagicMock()
        self.chat.id = chat_id
        self.from_user = MagicMock()
        self.from_user.id = "123456789"


class TestFetchMailProcess:
    @patch("bot.receive_msg.subprocess.check_output")
    def test_fetch_mail_process_success(self, mock_check_output):
        mock_check_output.return_value = "Mail fetched successfully"
        bot = MagicMock(telebot.TeleBot)
        config = MagicMock()
        message = MagicMock(telebot.types.Message)
        receiving_message = receive_msg.ReceivingMessage(bot, config)
        receiving_message.logger = MagicMock(logging.Logger)
        receiving_message.fetch_mail_process("testuser", message)
        bot.reply_to.assert_called_once_with(
            message, "New mails fetched - process completed."
        )
        receiving_message.logger.info.assert_called_with(
            msg="fetch mail process completed: Mail fetched successfully"
        )

    @patch(
        "bot.receive_msg.subprocess.check_output",
        side_effect=CalledProcessError(
            returncode=1,
            cmd="fetchmail",
            output="fetchmail: another foreground fetchmail is running at",
        ),
    )
    def test_fetch_mail_process_already_running(self, mock_check_output):
        bot = MagicMock(telebot.TeleBot)
        config = MagicMock()
        message = MagicMock(telebot.types.Message)
        receiving_message = receive_msg.ReceivingMessage(bot, config)
        receiving_message.logger = MagicMock(logging.Logger)
        receiving_message.fetch_mail_process("testuser", message)
        
        bot.reply_to.assert_called_once_with(
            message, "Another fetchmail process is running - retry later again."
        )
        receiving_message.logger.info.assert_called_with(
            "Another fetchmail process is running: fetchmail: another foreground fetchmail is running at"
        )

    @patch(
        "bot.receive_msg.subprocess.check_output", side_effect=Exception("General error")
    )
    def test_fetch_mail_process_exception_handling(self, mock_check_output):
        bot = MagicMock(telebot.TeleBot)
        config = MagicMock()
        message = MockMessage(chat_id="12345")
        receiving_message = receive_msg.ReceivingMessage(bot, config)
        receiving_message.logger = MagicMock(logging.Logger)
        receiving_message.fetch_mail_process("testuser", message)
        bot.send_message.assert_called_once_with(
            message.chat.id, "Error during fetch mail process: General error"
        )
        receiving_message.logger.info.assert_called_with(
            msg="Error during fetch mail process: General error"
        )
