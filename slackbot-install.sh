#READ THE README BEFORE INSTALLING
sudo apt install python3-pip python3-venv
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python3 -
cd slackbot
poetry install
sudo cp slackbot.service /lib/systemd/system
sudo systemctl daemon-reload
sudo systemctl enable slackbot && sudo systemctl start slackbot
sleep 5s
sudo systemctl status slackbot
