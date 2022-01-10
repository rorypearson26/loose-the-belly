"""Module containing routing for messages coming from slack.


"""
from decouple import config
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler


BOT_TOKEN = config("SLACK_BOT_TOKEN")
APP_TOKEN = config("SLACK_APP_TOKEN")
SIGNING_SECRET = config("SLACK_SIGNING_SECRET")

app = App(token=BOT_TOKEN)


@app.message("add")
def add_message(message, say):

    say(f"Hey there <@{message['user']}>!")


def main():
    handler = SocketModeHandler(app, APP_TOKEN)
    handler.start()


if __name__ == "__main__":
    main()
