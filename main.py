import os
import feedparser
from telegram import Bot

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHANNEL_ID = os.environ["CHANNEL_ID"]

bot = Bot(token=BOT_TOKEN)


def load_accounts():
    with open("accounts.txt", "r", encoding="utf-8") as f:
        return [
            line.strip().replace("@", "")
            for line in f
            if line.strip()
        ]


def send_post(account, entry):
    message = (
        f"📌 @{account}\n\n"
        f"{entry.title}\n\n"
        f"🔗 {entry.link}"
    )

    bot.send_message(
        chat_id=CHANNEL_ID,
        text=message
    )


accounts = load_accounts()

total = 0

for account in accounts:
    url = f"https://nitter.net/{account}/rss"

    feed = feedparser.parse(url)

    print(account, ":", len(feed.entries), "تغريدة")

    if feed.entries:
        send_post(account, feed.entries[0])
        total += 1

print("تم إرسال", total, "تغريدة")
