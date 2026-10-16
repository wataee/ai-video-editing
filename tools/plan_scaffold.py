import os
import sys
import json
import argparse
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

def build_scaffold(words_data: list, project_id: str = "clip", proxy_path: str = None, sdr_path: str = None) -> dict:
    beats = []
    current_words = []
    
    total_words = len(words_data)
    for idx, w in enumerate(words_data):
        current_words.append(w)
        text = w.get("text", "").strip()
        end_ms = w.get("endMs", 0)
        
        is_last = (idx == total_words - 1)
        next_w = words_data[idx + 1] if not is_last else None
        pause_ms = (next_w.get("startMs", end_ms) - end_ms) if next_w else 0
        
        ends_with_punct = any(text.endswith(p) for p in [".", "!", "?", ";"])
        comma_with_pause = text.endswith(",") and pause_ms > 400
        long_pause = pause_ms > 550
        too_long_beat = len(current_words) >= 12 and pause_ms > 300

        if is_last or ends_with_punct or comma_with_pause or long_pause or too_long_beat:
            b_start_ms = current_words[0].get("startMs", 0)
            b_end_ms = current_words[-1].get("endMs", b_start_ms)
            b_text = " ".join(cw.get("text", "").strip() for cw in current_words).strip()
            
            beat_words = [
                {
                    "text": cw.get("text", "").strip(),
                    "start_sec": round(cw.get("startMs", 0) / 1000.0, 2),
                    "end_sec": round(cw.get("endMs", 0) / 1000.0, 2)
                }
                for cw in current_words
            ]
            
            t_start = round(b_start_ms / 1000.0, 2)
            t_end = round(b_end_ms / 1000.0, 2)
            b_dur = round(t_end - t_start, 2)

            beats.append({
                "beat_index": len(beats),
                "time_range": [t_start, t_end],
                "duration_sec": b_dur,
                "line": b_text,
                "words": beat_words,
                "visual": "TODO",
                "proof_source": None,
                "camera": "TODO",
                "cut_motivation": "TODO",
                "sfx": "TODO",
                "why": "TODO"
            })
            current_words = []

    total_dur = beats[-1]["time_range"][1] if beats else 0.0

    plan = {
        "project_id": project_id,
        "version": "2.2",
        "engine": "remotion",
        "approved": False,
        "target_duration_sec": total_dur,
        "proxy_path": proxy_path,
        "sdr_path": sdr_path,
        "style_preset": "editorial-authority",
        "beats": beats
    }
    return plan

def validate_plan_schema(plan: dict) -> tuple[bool, str]:
    required_root = ["project_id", "version", "engine", "approved", "target_duration_sec", "beats"]
    for r in required_root:
        if r not in plan:
            return False, f"Missing required root field: '{r}'"

    beats = plan.get("beats", [])
    if not isinstance(beats, list) or len(beats) == 0:
        return False, "Plan 'beats' must be a non-empty list"

    required_beat = ["beat_index", "time_range", "line", "visual", "camera", "sfx"]
    for b in beats:
        for rb in required_beat:
            if rb not in b:
                return False, f"Beat #{b.get('beat_index')} missing field: '{rb}'"
        tr = b.get("time_range")
        if not (isinstance(tr, list) and len(tr) == 2 and tr[1] >= tr[0]):
            return False, f"Beat #{b.get('beat_index')} has invalid time_range: {tr}"

    return True, "OK"

def main():
    parser = argparse.ArgumentParser(description="Build edit_plan.json scaffold from word-level transcript JSON")
    parser.add_argument("transcript_json", help="Path to transcript JSON from Whisper")
    parser.add_argument("--project_id", default=None, help="Project ID / slug")
    parser.add_argument("--output", "-o", default=None, help="Output edit_plan.json path")
    parser.add_argument("--proxy", default=None, help="Path to proxy video")
    parser.add_argument("--sdr", default=None, help="Path to SDR video")
    args = parser.parse_args()

    in_path = Path(args.transcript_json).resolve()
    if not in_path.exists():
        print(f"Error: Transcript file not found: {in_path}", file=sys.stderr)
        sys.exit(1)

    with open(in_path, "r", encoding="utf-8") as f:
        words_data = json.load(f)

    if not isinstance(words_data, list):
        print("Error: Expected JSON array of word objects", file=sys.stderr)
        sys.exit(1)

    proj_id = args.project_id or in_path.stem.replace("_proxy", "").replace("_sdr_cfr30", "")
    out_path = Path(args.output).resolve() if args.output else (ROOT / "work" / "plan" / f"{proj_id}_plan_scaffold.json")
    out_path.parent.mkdir(parents=True, exist_ok=True)

    scaffold = build_scaffold(words_data, project_id=proj_id, proxy_path=args.proxy, sdr_path=args.sdr)

    is_valid, err_msg = validate_plan_schema(scaffold)
    if not is_valid:
        print(f"Schema Validation Error: {err_msg}", file=sys.stderr)
        sys.exit(1)

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(scaffold, f, indent=2, ensure_ascii=False)

    print(f"Plan scaffold successfully created: {out_path}")
    print(f"  Beats: {len(scaffold['beats'])}")
    print(f"  Total Duration: {scaffold['target_duration_sec']}s")

    beat_table_py = ROOT / "tools" / "beat_table.py"
    if beat_table_py.exists():
        test_md = out_path.parent / f"{proj_id}_scaffold_table.md"
        cmd = [sys.executable, str(beat_table_py), str(out_path), "--output", str(test_md)]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode == 0:
            print(f"  Verified by beat_table.py: PASS ({test_md.name})")
        else:
            print(f"  Warning: beat_table.py validation failed:\n{res.stderr}", file=sys.stderr)

if __name__ == "__main__":
    main()
