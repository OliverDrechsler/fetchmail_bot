![build](https://github.com/OliverDrechsler/fetchmail_bot/workflows/Fetchmail_Bot/badge.svg) 
[![CodeQL](https://github.com/OliverDrechsler/fetchmail_bot/actions/workflows/github-code-scanning/codeql/badge.svg)](https://github.com/OliverDrechsler/fetchmail_bot/actions/workflows/github-code-scanning/codeql)

[![GitHub release](https://img.shields.io/github/release/OliverDrechsler/fetchmail_bot.svg)](https://GitHub.com/OliverDrechsler/fetchmail_bot/releases/) 
[![GPLv3 License](https://img.shields.io/badge/License-GPL%20v2-yellow.svg)](https://www.gnu.org/licenses/old-licenses/gpl-2.0)

[![Python 3.8](https://img.shields.io/badge/python-3.8-blue.svg)](https://www.python.org/downloads/release/python-380/)
[![Python 3.9](https://img.shields.io/badge/python-3.9-blue.svg)](https://www.python.org/downloads/release/python-390/) 
[![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/release/python-3100/)
[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/release/python-3110/)
[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/release/python-3120/)

# Telegram Bot to run fetchmail process for users

**Telegram bot invokes on request a fetchmail for users**

- [Telegram Bot to run fetchmail process for users](#telegram-bot-to-run-fetchmail-process-for-users)
  - [Short description](#short-description)
  - [Project Structure](#project-structure)
  - [Telegram Bot setup](#telegram-bot-setup)
  - [Script config](#script-config)
  - [Install / setup script](#install--setup-script)
    - [General dependency - requirements](#general-dependency---requirements)
    - [Fetchmail requirements](#fetchmail-requirements)
    - [How to install / python requirements](#how-to-install--python-requirements)
    - [Configure / setup config.yaml file](#configure--setup-configyaml-file)
  - [Script run](#script-run)
  - [How to run project code as a systemd service](#how-to-run-project-code-as-a-systemd-service)
  - [Debug options](#debug-options)
    - [How to run unit-tests](#how-to-run-unit-tests)

## Short description
**Fetchmail_bot** is a telegram bot and is intended to perform a 
fetchmail command for specific user on the same system.  
  
The use case is that fetchmail process runs for specific configured user on a cron based schedule.  
But in case you want to get immediately mail's fetched,  
you've to wait or to login to the system and run the command manual.  
Fetchmail_bot will do that for you via telegram message.  
  

Just use the telegram command with the targeted username  
`/myuser` or with the message `mail`.  
To simplify it's possible to run the bot on a telegram group channel.
Just add the bot the required persons to the group.  
Configure the `config.yaml` to limit access / reaction of the bot  
to only specified users - telegram-id's modify the `allow_list`in `config.yaml`.
It's also possible to run the with one or more allowed to user.
The allowed user are able to initiate a fetchmail process for other users and the same system.  
Allowed user have just to run the command with the target username `/<target username>`  
This *target_usernames* must configured as well in `config.yaml` in the `additional_list`.  
  
## Project Structure
```
.
├── ./LICENSE      # License file
├── ./README.md
├── ./config       # Config directory for script
│   ├── ./config/config_template.yaml   # config template file must be renamed to config.yaml and content adjusted.
│   └── ./config/config_util.py         # Python module to read config
├── ./bot       # Config directory for script
│   └── ./bot/receive_msg.py            # Telegram Bot class for receiving messages and run fetchmail process
├── ./fetchmail_bot.py                  # Main telegram fetchmail bot script
├── ./fetchmail_bot.service             # template for creating a Linux systemd service
├── ./licenses.sh                       # bash script for creating library decency license file
├── ./requirements.txt                  # required python libraries
├── ./requirements_license.txt          # used libraries license file
├── ./telegram_bot_setup.md             # doc for creating a telegram bot
└── ./test                              # unit-tests  folder
    ├── ./test/test_config_util.py
    ├── ./test/test_receive_msg.py
    └── ./test/test_fetchmail_thread_fetch.py
```

## Telegram Bot setup
[telegram bot setup doc](telegram_bot_setup.md)

## Script config

## Install / setup script

### General dependency - requirements

This script is intended to run only on any(x86-64, arm, ..) linux systems.  
It's required to run the script in root shell environment to perform a `su <username>`
to switch into user context.

### Fetchmail requirements
It's required to have fetchmail installed and  
`.fetchmailrc` configured in each user home dir. 

### How to install / python requirements 

Python 3, pip3 and git cli is required.  
Clone repo to your RPi.  
```git clone git@github.com:OliverDrechsler/fetchmail_bot.git```

now run pip3 to install python requirements  
```pip3 install requirements.txt```

### Configure / setup config.yaml file
Copy `config/config_template.yaml` to `config/config.yaml`  
Edit `config/config.yaml` and fill with right values.  

## Script run
The script must run on that system where fetchmail is configured.  
Script requires to run within `root`context to switch to the target user to run  
shell command `su <username> -c fetchmail`.  
  
To run the script switch to directory and type `python3 fetchmail_bot.py`  

## How to run project code as a systemd service

Adjust file `fetchmail_bot.service` to your path.  
To run fetchmail_bot as a service on startup with root permissions  
copy `fetchmail_bot.service`to `/etc/systemd/system/`to your RPi systemd daemon folder.  
Run `systemctl daemon-reload` and `systemctl start fetchmail.service`to start it as a service.  

## Debug options
To enable DEBUG logging options edit `fatchmail_bot.py` line 11  
value `level=logging.INFO` to `level=logging.DEBUG`.  
Comment line `# telebot.logger.setLevel(logging.DEBUG)` in (remove #) for further telebot logs.  
Rerun script to get more log output.  
  
### How to run unit-tests

1. Install pytest  
`python3 -m pytest`  
2. run pytest
`pytest -v`
or to run with coverage 
`pytest --cov=./ --cov-report=xml`
