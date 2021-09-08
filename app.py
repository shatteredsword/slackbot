import logging
from flask import Flask
from slack import WebClient
from slackeventsapi import SlackEventAdapter

app = Flask(__name__)

slack_events_adapter = SlackEventAdapter(
    os.getenv("SLACK_EVENTS_TOKEN"), "/slack/events", app
)

slack_web_client = WebClient(token=os.getenv("SLACKBOT_TOKEN"))


@slack_events_adapter.on("message")
def message(payload):
    event = payload.get("event", {})

    MESSAGE_BLOCK = {
        "type": "section",
        "text": {"type": "mrkdwn", "text": "Howdy! :face_with_cowboy_hat:"},
    }

    text = event.get("text")

    if "hello pytexas" in text.lower():
        channel_id = event.get("channel")

        message = {"channel": channel_id, "blocks": [MESSAGE_BLOCK]}

        slack_web_client.chat_postMessage(**message)


if __name__ == "__main__":
    logger = logging.getLogger()

    logger.setLevel(logging.DEBUG)

    logger.addHandler(logging.StreamHandler())

    app.run(host="0.0.0.0", port=8080)