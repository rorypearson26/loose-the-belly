"""Module containing routing for messages coming from slack.


"""
import re

from decouple import config
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

from app.utilities.helper_functions import parse_measurement
from app.utilities.database_utils import add_measurement

BOT_TOKEN = config("SLACK_BOT_TOKEN")
APP_TOKEN = config("SLACK_APP_TOKEN")
SIGNING_SECRET = config("SLACK_SIGNING_SECRET")

app = App(token=BOT_TOKEN)


@app.message(re.compile(r"(?<=add )(\d+.\d+|\d+)", flags=re.IGNORECASE))
def add_message(message, say):
    """Listens for messages containing `add` so that weights can be added."""
    weight_obj = parse_measurement(message_str=message["text"])

    if weight_obj:
        say(f"<@{message['user']}>: Added {weight_obj.weight} to app.")
    else:
        say(rf"THAT IS NOT A WEIGHT IN FORMAT `\d{2}.\d{1}` (80.0) for 80kg.")


@app.message(re.compile(r".*", flags=re.IGNORECASE))
def mop_up_message(message, say):
    """Mops up any messages that are not matched and acknowledges them."""
    message_str = message["text"]
    say(f"Listened to: `{message_str}` but did not invoke any actions.")


def main():
    handler = SocketModeHandler(app, APP_TOKEN)
    handler.start()


if __name__ == "__main__":
    main()
