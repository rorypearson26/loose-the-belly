"""Module containing routing for messages coming from slack.
"""
from email.mime import image
import re

from decouple import config
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_sdk import WebClient

from app.utilities.database_utils import (add_measurement,
                                          remove_last_measurement)
from app.utilities.weight import Weight, parse_weight_csv
from app.utilities.plotting import plot_time_series
from app.utilities.text_parsing import TextParser

BOT_TOKEN = config("SLACK_BOT_TOKEN")
APP_TOKEN = config("SLACK_APP_TOKEN")
SIGNING_SECRET = config("SLACK_SIGNING_SECRET")

app = App(token=BOT_TOKEN)
client = WebClient(token=BOT_TOKEN)


@app.message(re.compile(r"(?<=add )(\d+.\d+|\d+)", flags=re.IGNORECASE))
def add_message(message, say):
    """Listens for messages containing `add` so that weights can be added."""
    try:
        weight_obj = Weight(msg_str=message["text"])
    except ValueError as e:
        say(f"{e}")

    if weight_obj:
        msg = f"<@{message['user']}>: Added the {weight_obj.weight} to app."
        add_measurement(weight_obj)
        say(msg)
    else:
        say(rf"THAT IS NOT A WEIGHT IN FORMAT `\d{2}.\d{1}` (80.0) for 80kg.")


@app.message(re.compile(r"deletelast", flags=re.IGNORECASE))
def delete_message(message, say):
    """Listens for messages containing `delete` so that measurements can be deleted."""
    return_msg = remove_last_measurement()
    if not return_msg:
        return_msg = "No record to delete."
    else:
        return_msg = f"Deleted:\n{str(return_msg)}"
    say(return_msg)


@app.message(re.compile(r"plot", flags=re.IGNORECASE))
def plot_time_series_message(message, say):
    """Listens for messages containing `plot` to return a time series graph."""
    months = TextParser(input_text=message["text"], regex_name="plot", cast_to_type=int)
    months = months.parsed_text if months.valid else 6
    image_path = plot_time_series(months)
    app.client.files_upload(file=str(image_path), channels=message["channel"])


@app.message(re.compile(r"readcsv", flags=re.IGNORECASE))
def read_csv_message(message, say):
    """Listens for messages containing `readcsv` so bulk measurements can be added."""
    try:
        weight_list = parse_weight_csv(msg_str=message["text"])
        return_msg = add_measurement(weight_list)
        say(f"Successfully added {len(weight_list)} measurement(s).")
    except ValueError:
        say("Error whilst adding batch of measurements.")


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
