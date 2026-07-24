import os
import json
import requests
from telegram import Bot

# قراءة الإعدادات
with open("config.json", "r") as f:
    config = json.load(f)

LIST_ID = config["list_id"]

# الأسرار من GitHub
BEARER_TOKEN = os.environ["X_BEARER_TOKEN"]
BOT_TOKEN = os.environ["BOT_TOKEN"]
CHANNEL_ID = os.environ["CHANNEL_ID"]

bot = Bot(token=BOT_TOKEN)


def get_list_tweets():
    url = f"https://api.x.com/2/lists/{LIST_ID}/tweets"

    headers = {
        "Authorization": f"Bearer {BEARER_TOKEN}"
    }

    params = {
        "max_results": 10,
        "tweet.fields": "created_at,author_id,attachments",
        "expansions": "author_id"
    }

    response = requests.get(
        url,
        headers=headers,
        params=params
    )

    if response.status_code != 200:
        print(response.text)
        return []

    return response.json().get("data", [])


def send_to_telegram(text):
    bot.send_message(
        chat_id=CHANNEL_ID,
        text=text
    )


tweets = get_list_tweets()

for tweet in tweets:
    message = tweet["text"]
    send_to_telegram(message)

print("Finished") 
