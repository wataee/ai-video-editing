import urllib.request
import re
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7'
}

extra = [
    ('Михаил Лабковский', '@labkovskiy', 'https://www.youtube.com/@labkovskiy/shorts', 'Психология и отношения'),
    ('Игорь Рыбаков', '@rybakovigor', 'https://www.youtube.com/@rybakovigor/shorts', 'Бизнес и инвестиции'),
]

new_items = []
for name, handle, url, niche in extra:
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            ids = list(dict.fromkeys(re.findall(r'/shorts/([a-zA-Z0-9_-]{11})', html)))
            for vid in ids[:3]:
                v_url = f'https://www.youtube.com/shorts/{vid}'
                v_req = urllib.request.Request(v_url, headers=headers)
                try:
                    with urllib.request.urlopen(v_req, timeout=8) as v_resp:
                        v_html = v_resp.read().decode('utf-8', errors='ignore')
                        tm = re.search(r'<title>(.*?)</title>', v_html)
                        title = tm.group(1).replace(' - YouTube', '').strip() if tm else vid
                        new_items.append({
                            'creator': name,
                            'handle': handle,
                            'niche': niche,
                            'id': vid,
                            'url': v_url,
                            'title': title,
                            'status': 'ПОДТВЕРЖДЕНО'
                        })
                except Exception:
                    pass
    except Exception:
        pass

p = ROOT / 'work' / 'verified_18_shorts.json'
existing = json.loads(p.read_text(encoding='utf-8'))
combined = existing + new_items
p.write_text(json.dumps(combined, indent=2, ensure_ascii=False), encoding='utf-8')
print('Total combined confirmed shorts:', len(combined))
