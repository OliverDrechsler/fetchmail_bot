#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import telebot
import logging
import threading
import subprocess
from config import config_util

telebot.apihelper.RETRY_ON_ERROR = True
# telebot.logger.setLevel(logging.DEBUG)

format = "%(asctime)s  -  %(name)s  -  %(funcName)s :        %(message)s"
logging.basicConfig(format=format, level=logging.INFO, datefmt="%Y-%m-%d %H:%M:%S")
logger = logging.getLogger("fetchmail_bot")


def main() -> None:
    """Main Program flow"""
    logger.info("Start Main Program")

    logger.debug("create config class instance")
    config = config_util.Configuration()

    logger.debug("initialize telegram bot instance")
    bot = telebot.TeleBot(config.telegram_token, parse_mode=None)

    # dynamic telegram bot commands = users to fetchmail for
    logger.debug(msg="prepare telegram receive command instance")

    @bot.message_handler(commands=config.list_user)
    def receive_user_mails(message) -> None:
        # check if received from allowed telegram chat group and
        # allowed user id has send.
        if get_allowed(message=message, config=config):
            # get username from command to fetch mail for
            message_text: str = str(message.text).lstrip("/").lower()
            bot.reply_to(message, f"{message_text} - I'll start fetching new mails")
            # start new thread for fetchmail
            fetch_mail_thread = threading.Thread(
                target=fetch_mail_process, args=(message_text, bot, message, logger)
            )
            fetch_mail_thread.start()
            fetch_mail_thread.join()

    # standard telegram bot for fetch mail for requested user
    logger.debug(msg="prepare telegram receive text instance")

    @bot.message_handler(func=lambda message: message.content_type == "text")
    def receive_mail_for_requested_user(message):
        # check if received from allowed telegram chat group and allowed
        # user id has send.
        if get_allowed(message=message, config=config):
            # check is text message is mail, otherwise do nothing
            if str(message.text).lower() == "mail":
                # Loop over config user dict with username and its telegram id
                # to resolve received telegram.from.user_id into username
                for k, v in config.user_dict.items():
                    # Get's username to run fetchmail for.
                    # Compares received id with list id to map to username
                    if str(message.from_user.id) in v:
                        # takes now the user dict key (which hold username)
                        # for run fetchmail process for.
                        bot.reply_to(
                            message, f" - I'll start fetching new mails for {k}"
                        )
                        fetch_mail_thread = threading.Thread(
                            target=fetch_mail_process,
                            args=(k.lower(), bot, message, logger),
                        )
                        fetch_mail_thread.start()

    bot.infinity_polling(logger_level=logging.DEBUG, timeout=10, long_polling_timeout=5)
    # bot.infinity_polling()
    # bot.polling(none_stop=True, timeout=30)


def fetch_mail_process(
    username: str,
    bot: telebot.TeleBot,
    message: telebot.types.Message,
    logger: logging.Logger,
) -> None:
    """Fetches mail for specified user in separate thread

    :param username: context were fetchmail process should run
    :type username: str
    :param bot: telebot instance
    :type bot: telebot.TeleBot
    :param message: received telegram message
    :type message: telebot.types.Message
    :param logger: logging instance
    :type logger: logging.Logger
    """
    try:
        logger.info(msg=f"will call fetchmail with username: {username}")
        output: str = subprocess.check_output(
            args=["su", username, "-c", "fetchmail"],
            text=True,
            stderr=subprocess.STDOUT,
        )
        logger.info(msg=f"fetch mail process completed: {output}")
        bot.reply_to(message, "New mails fetched - process completed.")
    except subprocess.CalledProcessError as e:
        logger.info(msg="check output")
        if str(e.output.partition("\n")[0]).startswith(
            "fetchmail: another foreground fetchmail is running at"
        ):
            logger.info(f"Another fetchmail process is running: {e.output}")
            bot.reply_to(
                message, "Another fetchmail process is running - retry later again."
            )
        else:
            logger.info(msg=f"No mails to fetch: {e.output}")
            bot.reply_to(message, "No mail to fetch found.")
    except Exception as e:
        logger.info(msg=f"Error during fetch mail process: {e}")
        bot.send_message(message.chat.id, f"Error during fetch mail process: {e}")


def get_allowed(
    message: telebot.types.Message, config: config_util.Configuration
) -> bool:
    """Checks given telegram chat id is allowed id from config
    and perform further check get_allowed_user

    :param message: received telegram message
    :type message: telebot.types.Message
    :param config: config param instance
    :type config: config_util.Configuration
    :return: check result as boolean
    :rtype: bool
    """
    if str(message.chat.id) == config.telegram_chat_nr:
        return get_allowed_user(message=message, config=config)
    return False


def get_allowed_user(
    message: telebot.types.Message, config: config_util.Configuration
) -> bool:
    """Checks if given telegram from user id is allowed from config file

    :param message: received telegram message
    :type message: telebot.types.Message
    :param config: config param instance
    :type config: config_util.Configuration
    :return: check result as boolean
    :rtype: bool
    """
    if str(message.from_user.id) in config.list_id:
        return True
    return False


if __name__ == "__main__":
    """
    Python main program start
    """
    main()
