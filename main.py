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


def get_rss(account):
    return f"https://nitter.net/{account}/rss"


def send_post(account, entry):
    text = (
        f"📌 @{account}\n\n"
        f"{entry.title}\n\n"
        f"🔗 {entry.link}"
    )

    bot.send_message(
        chat_id=CHANNEL_ID,
        text=text
    )


accounts = load_accounts()

for account in accounts:
    rss = feedparser.parse(get_rss(account))

    for entry in rss.entries[:3]:
        send_post(account, entry)

print("تم الانتهاء")
