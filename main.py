import os
import json
import requests
from telegram import Bot

with open("config.json", "r") as f:
    config = json.load(f)

LIST_ID = config["list_id"]

BEARER_TOKEN = os.environ["X_BEARER_TOKEN"]
BOT_TOKEN = os.environ["BOT_TOKEN"]
CHANNEL_ID = os.environ["CHANNEL_ID"]

bot = Bot(token=BOT_TOKEN)

headers = {
    "Authorization": f"Bearer {BEARER_TOKEN}"
}

url = f"https://api.x.com/2/lists/{LIST_ID}/tweets"

params = {
    "max_results": 10,
    "tweet.fields": "created_at,author_id,attachments",
    "expansions": "author_id,attachments.media_keys",
    "media.fields": "url"
}

response = requests.get(url, headers=headers, params=params)

if response.status_code != 200:
    print(response.text)
    exit()

data = response.json()

tweets = data.get("data", [])
users = {
    u["id"]: u["username"]
    for u in data.get("includes", {}).get("users", [])
}

media = {
    m["media_key"]: m.get("url")
    for m in data.get("includes", {}).get("media", [])
}


for tweet in tweets:

    username = users.get(tweet.get("author_id"), "unknown")

    text = (
        f"📌 @{username}\n\n"
        f"{tweet['text']}\n\n"
        f"🔗 https://x.com/{username}/status/{tweet['id']}"
    )

    photos = []

    if "attachments" in tweet:
        for key in tweet["attachments"].get("media_keys", []):
            if key in media:
                photos.append(media[key])

    if photos:
        bot.send_photo(
            chat_id=CHANNEL_ID,
            photo=photos[0],
            caption=text
        )
    else:
        bot.send_message(
            chat_id=CHANNEL_ID,
            text=text
        )

print(f"تمت معالجة {len(tweets)} تغريدة")
