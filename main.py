import os
import requests
import feedparser
import json

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")
LAST_FILE = "last_mod_obb.json"

RSS_FEEDS = [
    "https://apkdone.com/feed/"
]

def send_message(text, photo=None):
    if photo:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
        data = {
            "chat_id": CHANNEL_ID,
            "photo": photo,
            "caption": text,
            "parse_mode": "HTML"
        }
    else:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        data = {
            "chat_id": CHANNEL_ID,
            "text": text,
            "parse_mode": "HTML"
        }
    requests.post(url, json=data)

def load_last():
    try:
        with open(LAST_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_last(data):
    with open(LAST_FILE, "w") as f:
        json.dump(data, f)

posted = load_last()
new_posted = posted.copy()

for feed_url in RSS_FEEDS:
    feed = feedparser.parse(feed_url)
    if not feed.entries:
        continue

    game = feed.entries[0]
    game_id = game.get("id") or game.get("link")

    if game_id in posted:
        continue

    title = game.title
    link = game.link.lower()
    image = game.get("media_content", [{}])[0].get("url")

    # Detect OBB
    obb = "OBB" if ("obb" in link or "data" in title.lower()) else "No OBB"

    msg = (
        f"🎮 <b>MOD + OBB GAME</b>\n\n"
        f"🔥 <b>{title}</b>\n"
        f"🛠 MOD: Unlimited Money / Premium\n"
        f"📦 OBB: {obb}\n"
        f"⬇️ Download: {game.link}\n\n"
        f"#ModAPK #OBBGame #AndroidGames"
    )

    send_message(msg, image)
    new_posted[game_id] = True

save_last(new_posted)
