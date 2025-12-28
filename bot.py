import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TARGET_CHAT_ID")
SITE_URL = os.getenv("SITE_URL", "http://XXXX")
POLL_INTERVAL = int(os.getenv("POLL_INTERVAL", "10"))

if not BOT_TOKEN or not CHAT_ID:
    print("Please set TELEGRAM_BOT_TOKEN and TARGET_CHAT_ID in environment or .env")
    raise SystemExit(1)

last_id = None


def format_message(ad: dict) -> str:
    parts = []
    parts.append("#набір_відкрито")
    if ad.get("tags"):
        parts.append(f"\n{ad.get('tags')}")
    meta = []
    if ad.get('system'):
        meta.append(f"Система: {ad.get('system')}")
    if ad.get('master_name'):
        master = ad.get('master_name')
        t = f" Майстер: {master}"
        if ad.get('master_telegram'):
            t += f" ({ad.get('master_telegram')})"
        meta.append(t)
    if meta:
        parts.append(" ".join(meta))

    if ad.get('type_game'):
        parts.append(f"\nТип гри: {ad.get('type_game')}")
    if ad.get('setting_genre'):
        parts.append(f" Сетинг, жанр: {ad.get('setting_genre')}")
    if ad.get('level'):
        parts.append(f"\nРівень персонажа: {ad.get('level')}")
    if ad.get('cost'):
        parts.append(f" Вартість: {ad.get('cost')}")
    if ad.get('date') or ad.get('time'):
        date = ad.get('date', '')
        timev = ad.get('time', '')
        parts.append(f"\n🗓 {date} ⏰ {timev}")
    if ad.get('duration'):
        parts.append(f" ⌛️ {ad.get('duration')}")
    if ad.get('age_limit'):
        parts.append(f" 🔞 Обмеження по віку - {ad.get('age_limit')}")
    if ad.get('warnings'):
        parts.append(f"\nПопередження: {ad.get('warnings')}")
    if ad.get('tags'):
        parts.append(f"\nДодаткові теги: {ad.get('tags')}")
    if ad.get('description'):
        parts.append(f"\nОпис: {ad.get('description')}")
    if ad.get('filled'):
        parts.append(f"\nЗаповненість: {ad.get('filled')}")

    return " ".join(parts)


def send_telegram(text: str):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": True,
    }
    r = requests.post(url, json=payload, timeout=10)
    if not r.ok:
        print("Telegram send failed:", r.status_code, r.text)


if __name__ == '__main__':
    print(f"Polling {SITE_URL}/adventures/latest every {POLL_INTERVAL}s")
    global last_id
    while True:
        try:
            resp = requests.get(f"{SITE_URL}/adventures/latest", timeout=5)
            if resp.status_code == 200:
                ad = resp.json()
                if last_id is None:
                    last_id = ad.get('id')
                elif ad.get('id') != last_id:
                    msg = format_message(ad)
                    send_telegram(msg)
                    last_id = ad.get('id')
            else:
                # 404 or other: ignore when placeholder
                pass
        except Exception as e:
            # when SITE_URL is placeholder http://XXXX it'll fail — that's expected
            print("Poll error (maybe SITE_URL is placeholder):", e)
        time.sleep(POLL_INTERVAL)
