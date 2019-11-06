from flask import Flask, request, abort

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

import os

app = Flask(__name__)

YOUR_CHANNEL_ACCESS_TOKEN = os.environ["e5PTwuR5+v7Nm0p/IsmyRhFR4Td3KTYgUl9NK5dn7adhoBwkHthHbddnwp16wh++ewqd1M93G0EKzW6fWXHR6wGcAedh7TOP10DtP94QDyOJ0zcUI/QIKOHzjl34o1z03xOPoF+5Q2pLh/K2qacYvwdB04t89/1O/w1cDnyilFU="]
YOUR_CHANNEL_SECRET = os.environ["fe8644ed37b290fc3f0dd54466aa2efa"]

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)


@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]

    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)

    except InvalidSignatureError:
        abort(400)

    return "OK"


@handler.add(MessageEvent, message=TextSendMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host='0.0.0.0', port=port)