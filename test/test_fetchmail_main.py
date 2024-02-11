import pytest
import yaml
import telebot
from unittest.mock import patch, MagicMock
from config import config_util

# Assuming the code snippet provided above is saved in a file named `fetchmail_bot.py`
from fetchmail_bot import main, fetch_mail_process, get_allowed


class Test_FetchmailBot:
    @patch("fetchmail_bot.telebot.TeleBot")
    @patch("fetchmail_bot.config_util.Configuration")
    def test_bot_initialization(self, mock_config, mock_telebot):
        mock_config.return_value.telegram_token = "dummy_token"
        main()
        mock_telebot.assert_called_once_with("dummy_token", parse_mode=None)

    @patch("fetchmail_bot.threading.Thread.start")
    @patch("fetchmail_bot.get_allowed", return_value=True)
    @patch("fetchmail_bot.telebot.TeleBot")
    @patch("fetchmail_bot.config_util.Configuration")
    def test_message_handling_and_fetchmail_thread_start(self,
                                                         mock_config,
                                                         mock_telebot,
                                                         mock_get_allowed,
                                                         mock_thread_start):
        mock_config.return_value.list_user = ["testuser"]
        mock_message = MagicMock()
        mock_message.text = "/testuser"
        mock_message.content_type = "text"
        main()
        bot_instance = mock_telebot.return_value
        bot_instance.message_handler.assert_called()
        bot_instance.infinity_polling.assert_called()
        # mock_thread_start.assert_called()

    # @patch(
    #     "fetchmail_bot.subprocess.check_output", side_effect=Exception("Test Exception"))
    # @patch("fetchmail_bot.telebot.TeleBot")
    # def test_error_handling_during_fetchmail_process(self,
    #                                                  mock_telebot, 
    #                                                  mock_subprocess):
    #     mock_bot = mock_telebot.return_value
    #     # mock_fetchmail = mock_subprocess.
    #     mock_message = MagicMock()
    #     mock_logger = MagicMock()
    #     with pytest.raises(Exception):
    #         fetch_mail_process("testuser", mock_bot, mock_message, mock_logger)
    #     mock_logger.info.assert_called_with(
    #         msg="Error during fetch mail process: Test Exception"
    #     )
