# Telegram Bot to run fetchmail process for users

**Fetchmail_bot** is a telegram bot and is intended to perform a 
fetchmail command for specific user on the same system.  
  
The use case is that fetchmail process runs for specific configured user on a cron based schedule.  
But in case you want to get immediately mail's fetched,  
you've to wait or to login to the system and run the command manual.  
Fetchmail_bot will do that for you via telegram message.  
  

Just use the telegram command with the targeted username  
`/myuser` or with the message `mail`.  
To simplyfy it's possible to run the bot on a telegram group channel.
Just add the bot the required persons to the group.  
Configure the `config.yaml` to limit access / reaction of the bot  
to only specified users - telegram-id's modify the `allow_list`in `config.yaml`.
It's also possible to run the with one or more allowed to user.
The allowed user are able to initiate a fetchmail process for other users and the same system.  
Allowed user have just to run the command with the target username `/<target username>`  
This *target_usernames* must configured as well in `config.yaml` in the `additional_list`.  
  
## Telegram Bot setup
[telegram bot setup docu](telegram_bot_setup.md)

## Script config

## Install / setup script

### How to install / python requirements 

Python 3, pip3 and git cli is required.  
Clone repo to your RPi.  
```git clone git@github.com:OliverDrechsler/fetchmail_bot.git```

now run pip3 to install python requirments  
```pip3 install requirements.txt```

### How to run project code as a systemd service

Adjust file `fetchmail_bot.service` to your path.  
To run fetchmail_bot as a service on startup with root permissions  
copy `fetchmail_bot.service`to `/etc/systemd/system/`to your RPi systemd deamon folder.  
Run `systemctl daemon-reload` and `systemctl start fetchmail.service`to start it as a service.  

## Configure / setup config.yaml file
Copy `config/config_template.yaml` to `config/config.yaml`  
Edit `config/config.yaml` and fill with right values.  

## Fetchmail requirements
It's required to have fetchmail installed and  
`.fetchmailrc` configured in each user home dir. 
  

## Script run
The script must run on that system where fetchmail is configured.  
Script requires to run within `root`context to switch to the target user to run  
shell command `su <username> -c fetchmail`.  
  
To run the script switch to directory and type `./fetchmail_bot.py`  

## Debug options
To enable DEBUG logging options edit `fatchmail_bot.py` line 13  
value `level=logging.INFO` to `level=logging.DEBUG`.  
Rerun script to get more log output.  
  
