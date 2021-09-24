sudo apt install python3-pip python3-venv
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python3 -
sudo cp slackbot/slackbot.service /lib/systemd/system
sudo systemctl daemon-reload
sudo systemctl enable slackbot && sudo systemctl start slackbot && sudo systemctl status slackbot
