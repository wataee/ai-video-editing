import os
import re
import json
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent

CREATOR_CHANNELS = [
    {"name": "Михаил Гребенюк", "handle": "@grebenukm", "niche": "Бизнес и продажи", "url": "https://www.youtube.com/@grebenukm/shorts"},
    {"name": "Михаил Лабковский", "handle": "@labkovskiyofficial", "niche": "Психология и отношения", "url": "https://www.youtube.com/@labkovskiyofficial/shorts"},
    {"name": "Оскар Хартманн", "handle": "@oskar_hartmann", "niche": "Бизнес и саморазвитие", "url": "https://www.youtube.com/@oskar_hartmann/shorts"},
    {"name": "Александр Соколовский", "handle": "@sokolovskiy", "niche": "Интервью и личный бренд", "url": "https://www.youtube.com/@sokolovskiy/shorts"},
    {"name": "Алексей Ситников", "handle": "@dr.alexey.sitnikov", "niche": "Психология и нейробиология", "url": "https://www.youtube.com/@dr.alexey.sitnikov/shorts"},
    {"name": "Максим Батырев", "handle": "@maxim_batyrev", "niche": "Менеджмент и управление", "url": "https://www.youtube.com/@maxim_batyrev/shorts"},
    {"name": "Артемий Лебедев", "handle": "@temalebedev", "niche": "Дизайн и медиа", "url": "https://www.youtube.com/@temalebedev/shorts"},
    {"name": "Радислав Гандапас", "handle": "@radislav_gandapas", "niche": "Ораторское искусство", "url": "https://www.youtube.com/@radislav_gandapas/shorts"},
    {"name": "Игорь Рыбаков", "handle": "@rybakov_igor", "niche": "Бизнес и инвестиции", "url": "https://www.youtube.com/@rybakov_igor/shorts"},
    {"name": "Илья Варламов", "handle": "@varlamov", "niche": "Медиа и урбанистика", "url": "https://www.youtube.com/@varlamov/shorts"},
]

def fetch_shorts_ids(channel_url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7"
    }
    req = urllib.request.Request(channel_url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode("utf-8", errors="ignore")
            ids = list(dict.fromkeys(re.findall(r'/shorts/([a-zA-Z0-9_-]{11})', html)))
            return ids
    except Exception as e:
        print(f"Error fetching {channel_url}: {e}")
        return []

def fetch_video_details(video_id):
    url = f"https://www.youtube.com/shorts/{video_id}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7"
    }
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode("utf-8", errors="ignore")
            tm = re.search(r'<title>(.*?)</title>', html)
            title = tm.group(1).replace(" - YouTube", "").strip() if tm else f"Shorts {video_id}"
            return {"id": video_id, "url": url, "title": title, "status": "ПОДТВЕРЖДЕНО"}
    except Exception as e:
        return {"id": video_id, "url": url, "title": f"Shorts {video_id}", "status": f"ERROR: {e}"}

def main():
    results = {}
    for c in CREATOR_CHANNELS:
        print(f"Scanning channel: {c['name']} ({c['handle']})...")
        v_ids = fetch_shorts_ids(c["url"])
        print(f"  Found {len(v_ids)} shorts IDs.")
        items = []
        for vid in v_ids[:3]:
            details = fetch_video_details(vid)
            details["creator"] = c["name"]
            details["handle"] = c["handle"]
            details["niche"] = c["niche"]
            items.append(details)
            safe_title = details['title'].encode('ascii', errors='replace').decode('ascii')
            print(f"    [OK] {details['id']}: {safe_title}")
        results[c["name"]] = items

    out_file = ROOT / "work" / "real_shorts_scanned.json"
    out_file.parent.mkdir(parents=True, exist_ok=True)
    out_file.write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nAll scanned items written to {out_file}")

if __name__ == "__main__":
    main()
