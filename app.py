import os

from decouple import config
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

BOT_TOKEN = config("SLACK_BOT_TOKEN")
APP_TOKEN = config("SLACK_APP_TOKEN")
SIGNING_SECRET = config("SLACK_SIGNING_SECRET")

# Initializes your app with your bot token and signing secret
app = App(token=BOT_TOKEN, signing_secret=SIGNING_SECRET)
app.client.apps_connections_open(app_token=APP_TOKEN)


# Listens to incoming messages that contain "hello"
@app.event("hello")
def message_hello(message, say):
    # say() sends a message to the channel where the event was triggered
    app.client.chat_postMessage(
        channel="#weight-tracker", text=f"Hey there <@{message['user']}>!"
    )


# Start your app
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))
    app.start(port=port)
    # handler = SocketModeHandler(app, APP_TOKEN)
    # handler.start()
