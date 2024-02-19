import telebot
import logging
import threading
import subprocess
from config import config_util

logger: logging.Logger = logging.getLogger(name="receive_msg")


class ReceivingMessage:
    """Receiving Telegram Bot messages"""

    telebot.apihelper.RETRY_ON_ERROR = True

    def __init__(self, bot: telebot.TeleBot, config: config_util.Configuration) -> None:
        """Initial class definition."""
        self.logger: logging.Logger = logging.getLogger(name="config")
        self.config: config_util.Configuration = config
        self.logger.debug(msg="initialize receive_msg class instance")
        self.bot: telebot.TeleBot = bot
        self.commands = self.bot.message_handler(commands=self.config.list_user)(self.receive_user_mails)
        self.message_request = self.bot.message_handler(func=lambda message: message.content_type == "text")(self.receive_mail_for_requested_user)

    def start(self):
        self.logger.debug(msg="start bot endless polling")
        self.bot.infinity_polling(logger_level=logging.DEBUG, timeout=10, long_polling_timeout=5)
    
    def receive_user_mails(self, message: telebot.types.Message) -> None:
        # check if received from allowed telegram chat group and
        # if it was send from allowed user id.
        if self.get_allowed(message=message):
            # get username from command to fetch mail for
            username_from_msg: str = str(message.text).lstrip("/").lower()
            
            self.bot.reply_to(message, f"{username_from_msg} - I'll start fetching new mails")
            # start new thread for fetchmail
            fetch_mail_thread = threading.Thread(
                target=self.fetch_mail_process, args=(username_from_msg, message)
            )
            fetch_mail_thread.start()
            fetch_mail_thread.join()

    # @bot.message_handler(func=lambda message: message.content_type == "text")
    def receive_mail_for_requested_user(self, message):
        # check if received from allowed telegram chat group and allowed
        # user id has send.
        if self.get_allowed(message=message):
            # check is text message is mail, otherwise do nothing
            if str(message.text).lower() == "mail":
                # Loop over config user dict with username and its telegram id
                # to resolve received telegram.from.user_id into username
                for k, v in self.config.user_dict.items():
                    # Get's username to run fetchmail for.
                    # Compares received id with list id to map to username
                    if str(message.from_user.id) in v:
                        # takes now the user dict key (which hold username)
                        # for run fetchmail process for.
                        self.bot.reply_to(
                            message, f" - I'll start fetching new mails for {k}"
                        )
                        fetch_mail_thread = threading.Thread(
                            target=self.fetch_mail_process,
                            args=(k.lower(), message),
                        )
                        fetch_mail_thread.start()
                        fetch_mail_thread.join()
    
    def fetch_mail_process(self,
                           username: str,
                           message: telebot.types.Message
                           ) -> None:
        """Fetches mail for specified user in separate thread

        :param username: context were fetchmail process should run
        :type username: str
        :param message: received telegram message
        :type message: telebot.types.Message
        """
        try:
            self.logger.info(msg=f"will call fetchmail with username: {username}")
            output: str = subprocess.check_output(
                args=["su", username, "-c", "fetchmail"],
                text=True,
                stderr=subprocess.STDOUT,
            )
            self.logger.info(msg=f"fetch mail process completed: {output}")
            self.bot.reply_to(message, "New mails fetched - process completed.")
        except subprocess.CalledProcessError as e:
            self.logger.info(msg="check output")
            if str(e.output.partition("\n")[0]).startswith(
                "fetchmail: another foreground fetchmail is running at"
            ):
                self.logger.info(f"Another fetchmail process is running: {e.output}")
                self.bot.reply_to(
                    message, "Another fetchmail process is running - retry later again."
                )
            else:
                self.logger.info(msg=f"No mails to fetch: {e.output}")
                self.bot.reply_to(message, "No mail to fetch found.")
        except Exception as e:
            self.logger.info(msg=f"Error during fetch mail process: {e}")
            self.bot.send_message(message.chat.id, f"Error during fetch mail process: {e}")

    def get_allowed(self, message: telebot.types.Message) -> bool:
        """Checks given telegram chat id is allowed id from config
        and perform further check get_allowed_user

        :param message: received telegram message
        :type message: telebot.types.Message
        :return: check result as boolean
        :rtype: bool
        """
        if str(message.chat.id) == self.config.telegram_chat_nr:
            return self.get_allowed_user(message=message)
        return False

    def get_allowed_user(self, message: telebot.types.Message) -> bool:
        """Checks if given telegram from user id is allowed from config file

        :param message: received telegram message
        :type message: telebot.types.Message
        :return: check result as boolean
        :rtype: bool
        """
        if str(message.from_user.id) in self.config.list_id:
            return True
        return False
