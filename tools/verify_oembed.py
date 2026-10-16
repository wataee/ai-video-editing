import socket
import urllib.request
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')
orig_gai = socket.getaddrinfo
socket.getaddrinfo = lambda h, p, f=0, t=0, pr=0, fl=0: orig_gai(h, p, socket.AF_INET, t, pr, fl)

candidates = [
    # 5 Psychology / Self-help
    ('ru-17-labkovskiy-acceptance', '-_bPuNEtoOE', 'Психология и отношения'),
    ('ru-18-labkovskiy-finance', 'jUV4WmrD8kQ', 'Психология и отношения'),
    ('ru-19-labkovskiy-narcissism', 'cP9exAVbdDw', 'Психология личности'),
    ('ru-15-sitnikov-sleep', 'c8fx_Y_EqCk', 'Психология и нейробиология'),
    ('ru-16-sitnikov-stress', 'QQQK8Y9e43Y', 'Психология и нейробиология'),
    
    # 5 Education / Science
    ('ru-20-postnauka-cancer', '15v4BU7pM8Y', 'Наука и медицина'),
    ('ru-21-postnauka-genetherapy', 'oijnbXWnnr0', 'Биология и генетика'),
    ('ru-22-nauchpok-eyes', 'u3gjmKheynA', 'Популярная наука'),
    ('ru-23-nauchpok-biology', '0MMjHm5svHU', 'Биология и эволюция'),
    ('ru-24-pobedinsky-bridges', 'tX_wcLrpIgk', 'Физика и инженерия'),
    
    # 5 Expert Personal Brand
    ('ru-25-ilyakhov-message', 'zEoZcoCJkJs', 'Редактура и деловая переписка'),
    ('ru-26-ilyakhov-tips', 'KRGmKB1yqjo', 'Коммуникация и сервисы'),
    ('ru-27-tarasenko-johnson', 'VR79_40Rn2M', 'Маркетинг и мышление'),
    ('ru-28-tarasenko-habits', '8NW6L1jKTJ4', 'Личный бренд и психология'),
    ('ru-04-sokolovskiy-mindset', 'NBqK6g0AScQ', 'Интервью и личный бренд')
]

results = []
for tag, vid, niche in candidates:
    url = f'https://www.youtube.com/oembed?url=https://www.youtube.com/shorts/{vid}&format=json'
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=8) as r:
            data = json.loads(r.read().decode('utf-8'))
            title = data.get('title')
            author = data.get('author_name')
            author_url = data.get('author_url')
            results.append({
                'tag': tag,
                'vid': vid,
                'niche': niche,
                'status': 'OK',
                'title': title,
                'author': author,
                'author_url': author_url
            })
            print(f"VERIFIED | {tag} | {vid} | {author} | {title}")
    except Exception as e:
        results.append({
            'tag': tag,
            'vid': vid,
            'niche': niche,
            'status': f'ERROR: {e}'
        })
        print(f"FAILED | {tag} | {vid} | {e}")

with open('references/library/oembed_verification.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
print("Saved to references/library/oembed_verification.json")
