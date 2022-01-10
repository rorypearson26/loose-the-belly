"""Module containing routing for messages coming from slack.


"""
from decouple import config
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

from helper_functions import get_weight

BOT_TOKEN = config("SLACK_BOT_TOKEN")
APP_TOKEN = config("SLACK_APP_TOKEN")
SIGNING_SECRET = config("SLACK_SIGNING_SECRET")

app = App(token=BOT_TOKEN)


@app.message("add")
def add_message(message, say):
    weight = get_weight(message_str=message["text"])
    if weight:
        say(f"<@{message['user']}>: Added {weight} to app.")
    else:
        say(rf"THAT IS NOT A WEIGHT IN FORMAT `\d{2}.\d{1}` (80.0) for 80kg.")


def main():
    handler = SocketModeHandler(app, APP_TOKEN)
    handler.start()


if __name__ == "__main__":
    main()
