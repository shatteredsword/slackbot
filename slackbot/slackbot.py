import datetime
import os
import pyimgur
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from time import sleep
from dotenv import load_dotenv
load_dotenv()
from loguru import logger

app = App(token=os.environ.get("SLACK_BOT_TOKEN"))
im = pyimgur.Imgur(
    os.environ.get("IMGUR_CLIENT_ID"), os.environ.get("IMGUR_CLIENT_SECRET")
)
im.refresh_token = os.environ.get("IMGUR_REFRESH_TOKEN")

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


# The test_callback shortcut listens to a shortcut with the callback_id "test_callback"
@app.shortcut("test_callback")
def open_modal(ack, shortcut, client):
    # Acknowledge the shortcut request
    ack()
    # Call the views_open method using the built-in WebClient
    client.views_open(
        trigger_id=shortcut["trigger_id"],
        # A simple view payload for a modal
        view={
            "type": "modal",
            "title": {"type": "plain_text", "text": "My App"},
            "close": {"type": "plain_text", "text": "Close"},
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "About the simplest modal you could conceive of :smile:\n\nMaybe <https://api.slack.com/reference/block-kit/interactive-components|*make the modal interactive*> or <https://api.slack.com/surfaces/modals/using#modifying|*learn more advanced modal use cases*>.",
                    },
                },
                {
                    "type": "context",
                    "elements": [
                        {
                            "type": "mrkdwn",
                            "text": "Psssst this modal was designed using <https://api.slack.com/tools/block-kit-builder|*Block Kit Builder*>",
                        }
                    ],
                },
            ],
        },
    )


# The echo command simply echoes on command
@app.command("/echo")
def repeat_text(ack, respond, command):
    # Acknowledge command request
    ack()
    respond(f"{command['text']}")


# attempt to recreate the beertime app
@app.command("/beertime2")
def beertime(ack, respond, command):
    # Acknowledge command request
    ack()
    respond(
        blocks=[
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "Use command `/beertime` to set an acceptable day and time where you and your team can share a beer in the office.\nAvailable commands are:\n- `/beertime list` get a list of beer times already configured\n- `/beertime set <day> <time>` set a new beer time (ex: /beertime set friday 4pm)\n- `/beertime remove <day>` remove beer time for a day (ex: /beertime remove friday)\n- `/beertime clear` remove all beer times\n- `/beertime next` displays how long until the next beer time\n\nNote: you cannot have more than 1 beer time on a single day.\n\nFor more help, go to <http://beertime.mathieuimbert.com/help|beertime.mathieuimbert.com/help>. This app is completely free, please support me on <https://patreon.com/mimbert|Patreon> to help me pay for the infrastructure / beer, thanks!",
                },
            }
        ]
    )


@app.command("/whiteboard")
def whiteboard(ack, say, respond, client, command):
    ack()
    respond(
        text=f"taking photo. please wait..."
    )
    #get photo here somewhere
    title = str(datetime.datetime.now().timestamp())
    im.refresh_access_token()
    newimage = im.upload_image(
        path="/tmp/foo.jpg",
        title=title,
        description=title,
        album=os.environ.get("IMGUR_ALBUM_ID"),
    )
    reply = newimage.link
    say(
        blocks=[
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "<https://imgur.com/a/"
                    + os.environ.get("IMGUR_ALBUM_ID")
                    + "|Album> / <"
                    + reply
                    + "|Image>",
                },
            },
            {"type": "image", "image_url": reply, "alt_text": "whiteboard image"},
        ],
        text=f"{reply}",
        as_user="true",
        username="Whiteboard Camera"
    )


# Start your app
if __name__ == "__main__":
    logger.debug('debug message')
    logger.info('info message')
    logger.warning('warn message')
    logger.error('error message')
    logger.critical('critical message')
    SocketModeHandler(app, os.environ.get("SLACK_APP_TOKEN")).start()
