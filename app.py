import datetime
import os
import logging
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

app = App(
    token=os.environ.get("SLACKBOT_OAUTH_TOKEN"),
    # signing_secret=os.environ.get("SLACK_SIGNING_SECRET") # not required for socket mode
)

# Listens to incoming messages that contain "hello"
@app.message(":wave:")
def message_hello(message, say):
    # say() sends a message to the channel where the event was triggered
    say(
        blocks=[
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": f"Hey there <@{message['user']}>!"},
                "accessory": {
                    "type": "button",
                    "text": {"type": "plain_text", "text": "Click Me"},
                    "action_id": "button_click",
                },
            }
        ],
        text=f"Hey there <@{message['user']}>!",
    )


# Start your app
if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
