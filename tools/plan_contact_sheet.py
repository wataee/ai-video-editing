import argparse
import base64
import json
import os
import subprocess
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


def extract_frame_at(video_path: str, timestamp_sec: float, out_path: str) -> bool:
    if not os.path.exists(video_path):
        return False
    cmd = [
        "ffmpeg",
        "-y",
        "-ss", str(max(0.0, timestamp_sec)),
        "-i", video_path,
        "-vframes", "1",
        "-q:v", "2",
        out_path
    ]
    res = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return res.returncode == 0 and os.path.exists(out_path)


def file_to_data_uri(path: str) -> str:
    if not os.path.exists(path):
        return ""
    with open(path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("ascii")
    return f"data:image/jpeg;base64,{b64}"


def create_contact_sheet(image_paths: list[str], output_path: str, title: str = "Contact Sheet"):
    valid_images = [p for p in image_paths if os.path.exists(p)]
    if not valid_images:
        print("Ошибка: нет кадров для объединения в контактный лист.", file=sys.stderr)
        return False

    n = len(valid_images)
    cols = 2 if n <= 4 else 3 if n <= 9 else 4
    rows = (n + cols - 1) // cols

    loaded = [Image.open(p) for p in valid_images]
    w, h = loaded[0].size

    thumb_w = 400
    thumb_h = int(h * (thumb_w / w))

    pad = 20
    header_h = 70
    sheet_w = cols * thumb_w + (cols + 1) * pad
    sheet_h = rows * thumb_h + (rows + 1) * pad + header_h

    sheet = Image.new("RGB", (sheet_w, sheet_h), (14, 14, 18))
    draw = ImageDraw.Draw(sheet)

    draw.text((pad, 20), title, fill=(255, 255, 255))

    for idx, img in enumerate(loaded):
        r = idx // cols
        c = idx % cols
        x = pad + c * (thumb_w + pad)
        y = header_h + pad + r * (thumb_h + pad)

        resized = img.resize((thumb_w, thumb_h), Image.Resampling.LANCZOS)
        sheet.paste(resized, (x, y))
        draw.rectangle([x, y, x + thumb_w, y + thumb_h], outline=(50, 50, 60), width=2)

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    sheet.save(output_path, "PNG")
    return True


def main():
    parser = argparse.ArgumentParser(description="Генерация контактного листа плана до рендера")
    parser.add_argument("plan_path", help="Путь к edit_plan.json")
    parser.add_argument("--proxy", default=None, help="Путь к прокси-видео")
    parser.add_argument("--output", "-o", default="work/plan/contact_sheet_plan.png", help="Выходной файл")
    args = parser.parse_args()

    plan_file = Path(args.plan_path).resolve()
    if not plan_file.exists():
        print(f"Ошибка: файл плана не найден: {plan_file}", file=sys.stderr)
        sys.exit(1)

    with open(plan_file, "r", encoding="utf-8") as f:
        plan_data = json.load(f)

    beats = plan_data.get("beats", [])
    if not beats:
        print("Ошибка: в плане нет битов.", file=sys.stderr)
        sys.exit(1)

    proxy_file = args.proxy
    if not proxy_file:
        work_ingest = Path("work/ingest")
        if work_ingest.exists():
            proxies = list(work_ingest.glob("*_proxy.mp4"))
            if proxies:
                proxy_file = str(proxies[0])

    work_plan = Path("work/plan")
    stills_dir = work_plan / "stills"
    stills_dir.mkdir(parents=True, exist_ok=True)

    still_paths = []
    print(f"Генерация {len(beats)} кадров раскадровки через Remotion...")

    for b in beats:
        idx = b.get("beat_index", 0)
        tr = b.get("time_range", [0, 3])
        mid_time = (tr[0] + tr[1]) / 2.0

        raw_frame = str(stills_dir / f"raw_frame_{idx}.jpg")
        frame_data_uri = ""
        if proxy_file and os.path.exists(proxy_file):
            if extract_frame_at(proxy_file, mid_time, raw_frame):
                frame_data_uri = file_to_data_uri(raw_frame)

        props = {
            "beatIndex": idx,
            "timeRange": tr,
            "line": b.get("line", ""),
            "visual": b.get("visual", "speaker"),
            "camera": b.get("camera", "static"),
            "proofSource": b.get("proof_source"),
            "sfx": b.get("sfx", "none"),
            "why": b.get("why", ""),
            "frameImagePath": frame_data_uri,
        }

        props_file = stills_dir / f"props_{idx}.json"
        with open(props_file, "w", encoding="utf-8") as pf:
            json.dump(props, pf, ensure_ascii=False)

        still_out = stills_dir / f"beat_{idx}.png"
        cmd = [
            "npx.cmd" if os.name == "nt" else "npx",
            "remotion",
            "still",
            "src/index.ts",
            "PlanBeatStill",
            str(still_out),
            f"--props={str(props_file)}",
            "--scale=0.5",
            "--image-format=png",
            "--log=error"
        ]

        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode != 0:
            print(f"Ошибка при рендере бита {idx}: {res.stderr}", file=sys.stderr)
        else:
            still_paths.append(str(still_out))
            print(f"  [OK] Бит #{idx} ({tr[0]:.1f}s - {tr[1]:.1f}s) -> {still_out.name}")

    if still_paths:
        title = f"Plan Contact Sheet: {plan_data.get('project_id', 'clip')} | Beats: {len(beats)} | Approved: {plan_data.get('approved', False)}"
        success = create_contact_sheet(still_paths, args.output, title)
        if success:
            print(f"\nКонтактный лист успешно сохранен: {args.output}")
        else:
            print("Ошибка создания итогового контактного листа.", file=sys.stderr)
            sys.exit(1)


if __name__ == "__main__":
    main()
