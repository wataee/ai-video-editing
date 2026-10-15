import re
import json

file_path = r"C:\Users\timur\.gemini\antigravity\brain\8ecb0e0a-2fef-4e90-8ece-0a3a44d21f37\.system_generated\steps\2283\content.md"

with open(file_path, "r", encoding="utf-8") as f:
    text = f.read()

print(f"Total HTML length: {len(text)} chars")

# Find title
m_title = re.search(r"<title>(.*?)</title>", text)
if m_title:
    print(f"Folder Title: {m_title.group(1)}")

# Find all file extensions
exts = re.findall(r'[\"\'/]([a-zA-Z0-9_\-\.\s]+\.(?:mp4|mov|wav|mp3|prproj|aep|ffx|mogrt|cube|ttf|otf|png|jpg|pdf|txt|docx|zip|csv))[\"\'/]', text, re.IGNORECASE)
unique_exts = sorted(list(set(exts)))
print(f"\nFiles found ({len(unique_exts)}):")
for e in unique_exts:
    print(f"  - {e}")

# Search for Google Drive item data arrays
# Usually Google Drive has arrays like ["folder_id", "Folder Name", ...] or item metadata
items = re.findall(r'\[\"([a-zA-Z0-9_\-]{25,45})\",\[\"([^\"]+)\"', text)
print(f"\nPotential drive items ({len(items)}):")
for item_id, name in items[:25]:
    print(f"  - [{item_id}] {name}")

# Let's search for any words that look like folder names or video categories
keywords = ["SFX", "Sound", "Preset", "Font", "Overlay", "Template", "Graphic", "Music", "Hook", "Viral", "Joseph", "Prompt", "Script", "Pack"]
print("\nKeywords occurrences:")
for kw in keywords:
    matches = re.findall(rf'\"([^\"]{{2,40}}{kw}[^\"]{{0,40}})\"', text, re.IGNORECASE)
    clean = set(m for m in matches if not any(c in m for c in ["{", "}", "<", ">", "\\", "http", "google"]))
    if clean:
        print(f"  [{kw}]: {list(clean)[:8]}")
