from os import environ
from datetime import datetime
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from picamera import PiCamera
from pyimgur import Imgur
from time import sleep

load_dotenv()
camera = PiCamera()
try:
    camera.resolution = (
        int(environ.get("CAMERA_WIDTH")),
        int(environ.get("CAMERA_HEIGHT")),
    )
except:
    camera.resolution = (2592, 1944)
camera.rotation = environ.get("CAMERA_ROTATION")
im = Imgur(environ.get("IMGUR_CLIENT_ID"), environ.get("IMGUR_CLIENT_SECRET"))
im.refresh_token = environ.get("IMGUR_REFRESH_TOKEN")
app = Flask(__name__)


@app.route("/", methods=["POST"])
def post_logfile():
    if (request.method == "POST") & (
        request.form.get("key") == environ.get("PYTHON_APP_KEY")
    ):
        camera.start_preview()
        sleep(environ.get("CAMERA_DELAY"))
        camera.capture("/tmp/foo.jpg")
        title = str(datetime.now().timestamp())
        im.refresh_access_token()
        newimage = im.upload_image(
            path="foo.jpg", title=title, description=title, album=environ.get("IMGUR_ALBUM_ID")
        )
        return newimage.link
    else:
        return "Record not found", status.HTTP_400_BAD_REQUEST


if __name__ == "__main__":
    app.run(host="0.0.0.0")
