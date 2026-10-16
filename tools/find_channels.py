import socket
import urllib.request
import re
import json

orig_gai = socket.getaddrinfo
socket.getaddrinfo = lambda h, p, f=0, t=0, pr=0, fl=0: orig_gai(h, p, socket.AF_INET, t, pr, fl)

headers = {'User-Agent': 'Mozilla/5.0'}

channels = [
    ('roman.tarasenko', 'https://www.youtube.com/@roman.tarasenko/shorts'),
    ('maxim.ilyahov', 'https://www.youtube.com/@maxim.ilyahov/shorts'),
    ('AlexanderSokolovskiy', 'https://www.youtube.com/@AlexanderSokolovskiy/shorts'),
    ('Pobedinsky', 'https://www.youtube.com/@PhysPob/shorts'),
    ('SciOne', 'https://www.youtube.com/@SciOne/shorts')
]

for name, url in channels:
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=8) as r:
            html = r.read().decode('utf-8', errors='ignore')
            shorts = list(dict.fromkeys(re.findall(r'/shorts/([a-zA-Z0-9_-]{11})', html)))
            print(f"{name}: {len(shorts)} shorts -> {shorts[:5]}")
    except Exception as e:
        print(f"Error {name}: {e}")
