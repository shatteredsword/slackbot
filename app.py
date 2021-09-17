import datetime
import os
import logging
from slack_bolt import App
#os.environ["SLACK_BOT_TOKEN"] = ""
#os.environ["SIGNING_SECRET"] = ""

app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SIGNING_SECRET")
)

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
    app.start(port=int(os.environ.get("PORT", 8080)))