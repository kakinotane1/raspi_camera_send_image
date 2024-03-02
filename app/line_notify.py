import argparse
import io
import os
import time

import requests
from dotenv import load_dotenv
from picamera import PiCamera

load_dotenv()
NOTIFY_URL = os.environ["NOTIFY_URL"]
NOTIFY_TOKEN = os.environ["NOTIFY_TOKEN"]


def take_photo_stream() -> io.BytesIO:
    photo_stream = io.BytesIO()
    with PiCamera() as camera:
        camera.start_preview()
        time.sleep(1)
        camera.capture(output=photo_stream, format="png")
    return photo_stream


def send_photo_stream(
    photo_stream: io.BytesIO, message="", notification_disabled=False
):
    headers = {"Authorization": f"Bearer {NOTIFY_TOKEN}"}
    payload = {
        "message": message,
        "notificationDisabled": notification_disabled,
    }
    files = {"imageFile": photo_stream.getvalue()}
    res = requests.post(NOTIFY_URL, params=payload, headers=headers, files=files)


def send_image(filepath: str, message="", notification_disabled=False):
    headers = {"Authorization": "Bearer " + NOTIFY_TOKEN}
    payload = {
        "message": message,
        "notificationDisabled": notification_disabled,
    }
    files = {"imageFile": open(filepath, "rb")}
    res = requests.post(NOTIFY_URL, params=payload, headers=headers, files=files)


def main(args):
    num = args.num
    sleep = args.sleep
    message = args.message
    for _ in range(num):
        photo_stream = take_photo_stream()
        send_photo_stream(
            photo_stream=photo_stream,
            message=message,
            notification_disabled=True,
        )
        time.sleep(sleep)


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--num", "-n", type=int, default=1, help="How many times you want to take photos.")
    parser.add_argument("--sleep", "-s", type=int, default=1, help="Sleep time between taking photos.")
    parser.add_argument("--message", "-m", type=str, default="Send Image.", help="Message you want to send.")
    return parser.parse_args()


if __name__ == "__main__":
    args = get_args()
    main(args)
