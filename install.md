# How to install fetchmail_bot within a pyenv and virtualenv and run as a systemd service on a Raspberry Pi

```bash
sudo apt-get install -y make build-essential libssl-dev zlib1g-dev libbz2-dev \
libreadline-dev libsqlite3-dev wget curl llvm libncursesw5-dev xz-utils tk-dev \
libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev python3-openssl git
```
# Install pyenv
```bash
git clone https://github.com/pyenv/pyenv.git ~/.pyenv
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init --path)"' >> ~/.bashrc
echo 'eval "$(pyenv init -)"' >> ~/.bashrc
source ~/.bashrc
pyenv --version
```

# Install Python 3.11
```bash
pyenv install --list | grep 3.13
pyenv install 3.13.5
pyenv global 3.13.5
python --version
```

# Create a virtual environment
```bash
git clone https://github.com/pyenv/pyenv-virtualenv.git ~/.pyenv/plugins/pyenv-virtualenv
echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bashrc
source ~/.bashrc
pyenv virtualenv 3.13.2 venv
cd /usr/local/bin/fetchmail_bot
pyenv local venv
```

# Install dependencies
```bash
pip3 install -r requirements.txt
```

# Create a systemd service
create a file named `fetchmail_bot.service` in `/etc/systemd/system/` with the following content:

```
[Unit]
Description=Telegram fetchmal bot
After=network.target

[Service]
User=pi
Group=pi
WorkingDirectory=/usr/local/bin/fetchmail_bot
SyslogIdentifier=fetchmail_bot

# Umgebungsvariablen setzen, damit pyenv und virtualenv aktiviert sind
Environment=PYENV_ROOT=/home/pi/.pyenv
Environment=PATH=/home/pi/.pyenv/shims:/home/pi/.pyenv/bin:/usr/local/bin:/usr/bin:/bin
Environment=VIRTUAL_ENV=/home/pi/.pyenv/versions/venv
Environment=PATH=/home/pi/.pyenv/versions/venv/bin:$PATH

# Startbefehl (Python direkt aus dem Virtualenv verwenden)
ExecStart=/home/pi/.pyenv/versions/venv/bin/python /usr/local/bin/fetchmail_bot/fetchmail_bot.py

Restart=on-failure

[Install]
WantedBy=multi-user.target
```

# Register and start new service to systemd
```bash
sudo systemctl daemon-reload
sudo systemctl enable fetchmail_bot.service
sudo systemctl start fetchmail_bot.service
sudo systemctl status fetchmail_bot.service
```

