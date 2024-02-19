#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import telebot
import logging
from config import config_util
from bot import receive_msg

# 
# SET LOG LEVEL OF SCRIPT
#
LOG_LEVEL = logging.INFO
# telebot.logger.setLevel(logging.DEBUG)


format = "%(asctime)s  -  %(name)s  -  %(funcName)s :        %(message)s"
logging.basicConfig(format=format, level=LOG_LEVEL, datefmt="%Y-%m-%d %H:%M:%S")
logger: logging.Logger = logging.getLogger(name="fetchmail_bot")


def main() -> None:
    """Main Program flow"""
    logger.info("Start Main Program")

    logger.debug("create config class instance")
    config = config_util.Configuration()

    logger.debug("initialize telegram bot instance")
    bot = telebot.TeleBot(config.telegram_token, parse_mode=None)

    # dynamic telegram bot commands = users to fetchmail for
    logger.debug(msg="prepare telegram receive command instance")

    receive_msg.ReceivingMessage(bot, config).start()


if __name__ == "__main__":
    """
    Python main program start
    """
    main()
