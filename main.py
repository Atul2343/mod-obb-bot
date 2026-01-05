import requests, json, os, hashlib
from bs4 import BeautifulSoup

BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
CHANNEL = "@yourchannelusername"

HEADERS = {"User-Agent": "Mozilla/5.0"}
POSTED_FILE = "posted.json"

# ---------- DUPLICATE ----------
if os.path.exists(POSTED_FILE):
    posted = set(json.load(open(POSTED_FILE)))
else:
    posted = set()

def is_new(text):
    h = hashlib.md5(text.encode()).hexdigest()
    if h in posted:
        return False
    posted.add(h)
    return True

def save():
    json.dump(list(posted), open(POSTED_FILE, "w"))

# ---------- TELEGRAM ----------
def send(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={
        "chat_id": CHANNEL,
        "text": msg,
        "parse_mode": "HTML",
        "disable_web_page_preview": False
    })

# ---------- ANDROID GAME SITES (25) ----------
SITES = [
    ("https://www.androidauthority.com/gaming", "h2 a"),
    ("https://www.androidpolice.com/games/", "h3 a"),
    ("https://www.xda-developers.com/tag/games/", "h3 a"),
    ("https://www.pocketgamer.com/android/", "h3 a"),
    ("https://www.gsmarena.com/games.php3", ".news-item h3 a"),
    ("https://www.droid-life.com/category/games/", "h2 a"),
    ("https://www.phonearena.com/games", "h3 a"),
    ("https://www.gamezebo.com/android-games/", "h3 a"),
    ("https://www.androidcentral.com/gaming", "h2 a"),
    ("https://www.techradar.com/mobile-gaming", "h3 a"),
    ("https://www.indiatoday.in/gaming", "h2 a"),
    ("https://www.hindustantimes.com/gaming", "h3 a"),
    ("https://www.livemint.com/technology/gaming", "h2 a"),
    ("https://www.cnet.com/tech/mobile/", "h3 a"),
    ("https://www.wired.com/tag/games/", "h3 a"),
    ("https://www.theverge.com/games", "h2 a"),
    ("https://www.digitaltrends.com/gaming/", "h3 a"),
    ("https://www.techadvisor.com/gaming/", "h3 a"),
    ("https://www.tomsguide.com/gaming", "h3 a"),
    ("https://www.pcgamer.com/mobile-gaming/", "h3 a"),
    ("https://www.ign.com/mobile", "h3 a"),
    ("https://www.gamesradar.com/mobile/", "h3 a"),
    ("https://www.eurogamer.net/mobile", "h3 a"),
    ("https://www.androidheadlines.com/category/games", "h2 a"),
    ("https://www.talkandroid.com/category/gaming/", "h2 a"),
]

# ---------- SCRAPE ----------
for url, selector in SITES:
    try:
        html = requests.get(url, headers=HEADERS, timeout=10).text
        soup = BeautifulSoup(html, "html.parser")

        for a in soup.select(selector)[:2]:   # per site limit
            title = a.text.strip()
            link = a.get("href")

            if not link:
                continue
            if link.startswith("/"):
                link = url.split("/")[0] + "//" + url.split("/")[2] + link

            key = title + link
            if is_new(key):
                msg = f"🎮 <b>{title}</b>\n\n🔗 {link}"
                send(msg)
    except:
        pass

save()
