#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
batch_render.py — Sequential Queue Renderer for Approved Client Plans.
Usage:
  python tools/batch_render.py <client_slug>
Or via npm:
  npm run batch -- <client_slug>
"""

import os
import sys
import json
import time
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

def run_batch(client_slug: str):
    client_dir = ROOT / "clients" / client_slug
    if not client_dir.exists():
        print(f"Error: Client directory not found: {client_dir}", file=sys.stderr)
        sys.exit(1)

    plan_dir = client_dir / "work" / "plan"
    out_dir = client_dir / "out"
    out_dir.mkdir(parents=True, exist_ok=True)

    if not plan_dir.exists():
        print(f"Error: Plan directory not found: {plan_dir}", file=sys.stderr)
        sys.exit(1)

    # Find all JSON plan files
    plan_files = sorted(list(plan_dir.glob("*plan*.json")))
    if not plan_files:
        print(f"No plan JSON files found in: {plan_dir}", file=sys.stderr)
        sys.exit(1)

    print(f"\n==========================================")
    print(f"BATCH RENDER QUEUE FOR CLIENT: '{client_slug}'")
    print(f"Found {len(plan_files)} candidate plan files.")
    print(f"==========================================")

    queue = []
    for pf in plan_files:
        try:
            with open(pf, "r", encoding="utf-8") as f:
                data = json.load(f)
            if data.get("approved") is True:
                queue.append((pf, data))
            else:
                print(f"  [QUEUE SKIP] '{pf.name}': approved is FALSE (requires human sign-off).")
        except Exception as e:
            print(f"  [WARN] Failed to read '{pf.name}': {e}", file=sys.stderr)

    if not queue:
        print(f"\nNo approved plans found in queue. Nothing to render.")
        print(f"To approve a plan, set '\"approved\": true' in the respective JSON file in:\n{plan_dir}")
        sys.exit(0)

    print(f"\nProcessing {len(queue)} approved plans sequentially (one by one)...")

    rendered_count = 0
    for idx, (pf, data) in enumerate(queue, start=1):
        proj_id = data.get("project_id", pf.stem.replace("_plan", ""))
        target_out = out_dir / f"{client_slug}_{proj_id}_v1.mp4"
        dur_sec = data.get("target_duration_sec", 15.0)
        dur_frames = int(round(dur_sec * 30))

        print(f"\n[{idx}/{len(queue)}] Rendering: '{pf.name}' -> '{target_out.name}' ({dur_frames} frames @ 30fps)")
        t0 = time.time()

        cmd = [
            "npx.cmd" if sys.platform == "win32" else "npx",
            "remotion", "render",
            "src/index.ts", "ReelFromPlan",
            str(target_out),
            f"--props={json.dumps({'plan': data})}",
            f"--frames=0-{max(1, dur_frames - 1)}"
        ]

        try:
            res = subprocess.run(cmd, cwd=str(ROOT), capture_output=True, text=True, check=True)
            elapsed = round(time.time() - t0, 2)
            print(f"  SUCCESS: Rendered '{target_out.name}' in {elapsed}s")
            rendered_count += 1
        except subprocess.CalledProcessError as e:
            print(f"  FAILED: Render failed for '{pf.name}':\n{e.stderr}", file=sys.stderr)

    print(f"\nBatch rendering completed: {rendered_count}/{len(queue)} clips rendered.")

    # Automatically trigger packaging
    pkg_script = ROOT / "tools" / "package_delivery.py"
    if pkg_script.exists():
        print(f"\nPackaging delivery artifacts...")
        subprocess.run([sys.executable, str(pkg_script), client_slug], cwd=str(ROOT))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python tools/batch_render.py <client_slug>")
        sys.exit(1)
    run_batch(sys.argv[1])
