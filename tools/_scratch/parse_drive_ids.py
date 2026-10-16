import re
import json

file_path = r"C:\Users\timur\.gemini\antigravity\brain\8ecb0e0a-2fef-4e90-8ece-0a3a44d21f37\.system_generated\steps\2283\content.md"

with open(file_path, "r", encoding="utf-8") as f:
    text = f.read()

# Let's search for JSON data containing file names and IDs
# In Google Drive, items often appear in data structures like:
# [["id", "name", ...], ...] or within AF_initDataCallback
patterns = [
    r'\[\"([a-zA-Z0-9_\-]{25,40})\"(?:,[^,\]]+)*?,\[\"([^\"]+\.(?:md|docx|mp4|mov|wav|zip|pdf|txt|prproj))\"',
    r'\[\"([a-zA-Z0-9_\-]{25,40})\",\[\"([^\"]+)\"',
    r'\"id\":\"([a-zA-Z0-9_\-]{25,40})\"[^\}]*?\"name\":\"([^\"]+)\"',
    r'\"([^\"]+\.(?:md|docx|mp4|mov|wav|zip|pdf|txt))\"'
]

print("--- Searching for files and IDs ---")
# Let's scan around the filenames we found
known_files = [
    "UE-Sound-Design-Claude-Training-COMPLETE.md",
    "Prompts List.docx",
    "3 things from beginner to pro.mp4",
    "3 things - Edit v1 + SFX.mp4"
]

for kf in known_files:
    idx = 0
    while True:
        pos = text.find(kf, idx)
        if pos == -1:
            break
        snippet = text[max(0, pos-200):min(len(text), pos+200)]
        print(f"\nSnippet around '{kf}':\n{snippet}\n")
        idx = pos + len(kf)

# Let's extract any 33-char Google Drive IDs near those files
drive_id_pattern = re.compile(r'[a-zA-Z0-9_\-]{28,38}')
for kf in known_files:
    pos = text.find(kf)
    if pos != -1:
        snippet = text[max(0, pos-300):min(len(text), pos+300)]
        ids = [i for i in drive_id_pattern.findall(snippet) if not i.startswith("http") and not i.startswith("google")]
        print(f"IDs near {kf}: {ids}")
