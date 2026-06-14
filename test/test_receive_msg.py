import unittest
from unittest.mock import MagicMock, patch
import sys
import types

telebot_stub = types.SimpleNamespace(
    TeleBot=object,
    types=types.SimpleNamespace(Message=object),
)
yaml_stub = types.SimpleNamespace(load=lambda *args, **kwargs: {}, SafeLoader=object)
sys.modules.setdefault("telebot", telebot_stub)
sys.modules.setdefault("yaml", yaml_stub)

from bot import receive_msg


class TestReceivingMessage(unittest.TestCase):
    def _make_config(self) -> MagicMock:
        config = MagicMock()
        config.telegram_chat_nr = "12345"
        config.list_id = ["67890"]
        config.user_dict = {"Oli": "67890", "Micha": "1010"}
        config.additional_list = ["Tim"]
        config.list_user = ["OLI", "oli", "Oli", "MICHA", "micha", "Micha", "TIM", "tim", "Tim"]
        return config

    def _make_message(
        self,
        text: str,
        chat_id: str = "12345",
        user_id: str = "67890",
    ) -> MagicMock:
        message = MagicMock()
        message.text = text
        message.chat.id = chat_id
        message.from_user.id = user_id
        return message

    @patch("bot.receive_msg.threading.Thread")
    def test_receive_user_mails_uses_configured_username_from_command(self, mock_thread):
        bot = MagicMock()
        config = self._make_config()
        message = self._make_message("/oli")

        receiving_message = receive_msg.ReceivingMessage(bot, config)

        receiving_message._ReceivingMessage__receive_user_mails(message)

        mock_thread.assert_called_once_with(
            target=receiving_message._ReceivingMessage__fetch_mail_process,
            args=("Oli", message),
        )
        bot.reply_to.assert_called_once_with(
            message,
            "Oli - I'll start fetching new mails",
        )

    @patch("bot.receive_msg.threading.Thread")
    def test_receive_user_mails_ignores_unknown_command(self, mock_thread):
        bot = MagicMock()
        config = self._make_config()
        message = self._make_message("/unknown")

        receiving_message = receive_msg.ReceivingMessage(bot, config)

        receiving_message._ReceivingMessage__receive_user_mails(message)

        mock_thread.assert_not_called()
        bot.reply_to.assert_not_called()

    @patch("bot.receive_msg.threading.Thread")
    def test_receive_user_mails_denies_disallowed_sender(self, mock_thread):
        bot = MagicMock()
        config = self._make_config()
        message = self._make_message("/oli", chat_id="99999", user_id="55555")

        receiving_message = receive_msg.ReceivingMessage(bot, config)

        receiving_message._ReceivingMessage__receive_user_mails(message)

        mock_thread.assert_not_called()
        bot.reply_to.assert_not_called()

    @patch("bot.receive_msg.threading.Thread")
    def test_receive_mail_request_uses_yaml_username_for_sender(self, mock_thread):
        bot = MagicMock()
        config = self._make_config()
        message = self._make_message("mail")

        receiving_message = receive_msg.ReceivingMessage(bot, config)

        receiving_message._ReceivingMessage__receive_mail_for_requested_user(message)

        mock_thread.assert_called_once_with(
            target=receiving_message._ReceivingMessage__fetch_mail_process,
            args=("Oli", message),
        )
        bot.reply_to.assert_called_once_with(
            message,
            " - I'll start fetching new mails for Oli",
        )

    @patch("bot.receive_msg.subprocess.check_output", side_effect=RuntimeError("boom"))
    def test_fetch_mail_process_sends_generic_error_message(self, mock_check_output):
        bot = MagicMock()
        config = self._make_config()
        message = self._make_message("mail")

        receiving_message = receive_msg.ReceivingMessage(bot, config)

        receiving_message._ReceivingMessage__fetch_mail_process("Oli", message)

        mock_check_output.assert_called_once_with(
            args=["su", "Oli", "-c", "fetchmail"],
            text=True,
            stderr=receive_msg.subprocess.STDOUT,
        )
        bot.send_message.assert_called_once_with(
            message.chat.id,
            "Error during fetch mail process. Please retry later.",
        )

    def test_get_allowed_returns_true_for_allowed_chat_and_user(self):
        bot = MagicMock()
        config = self._make_config()
        message = self._make_message("mail")

        receiving_message = receive_msg.ReceivingMessage(bot, config)

        self.assertTrue(receiving_message._ReceivingMessage__get_allowed(message))

    def test_get_allowed_returns_false_for_wrong_chat(self):
        bot = MagicMock()
        config = self._make_config()
        message = self._make_message("mail", chat_id="9911")

        receiving_message = receive_msg.ReceivingMessage(bot, config)

        self.assertFalse(receiving_message._ReceivingMessage__get_allowed(message))

    def test_get_allowed_user_returns_false_for_unknown_user(self):
        bot = MagicMock()
        config = self._make_config()
        message = self._make_message("mail", user_id="0911")

        receiving_message = receive_msg.ReceivingMessage(bot, config)

        self.assertFalse(receiving_message._ReceivingMessage__get_allowed_user(message))


if __name__ == "__main__":
    unittest.main()
