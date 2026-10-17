import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

def run_approval_gate(args: list[str]) -> subprocess.CompletedProcess:
    node_bin = shutil.which("node")
    assert node_bin is not None, "Node.js executable must be installed"
    script = ROOT / "tools" / "check_approval.mjs"
    cmd = [node_bin, str(script)] + args
    return subprocess.run(cmd, cwd=str(ROOT), capture_output=True, text=True, encoding="utf-8", errors="replace")

def test_approval_gate_fails_when_unapproved(tmp_path):
    plan_file = tmp_path / "edit_plan.json"
    with open(plan_file, "w", encoding="utf-8") as f:
        json.dump({"approved": False, "beats": []}, f)

    res = run_approval_gate([str(plan_file)])
    assert res.returncode == 1
    assert "APPROVAL GATE" in res.stderr

    res_flag = run_approval_gate(["--plan", str(plan_file)])
    assert res_flag.returncode == 1

def test_approval_gate_passes_when_approved(tmp_path):
    plan_file = tmp_path / "edit_plan.json"
    with open(plan_file, "w", encoding="utf-8") as f:
        json.dump({"approved": True, "beats": []}, f)

    res = run_approval_gate([str(plan_file)])
    assert res.returncode == 0
    assert "утвержден" in res.stdout

    res_dir = run_approval_gate([str(tmp_path)])
    assert res_dir.returncode == 0

    res_flag = run_approval_gate(["--plan", str(plan_file)])
    assert res_flag.returncode == 0

def test_approval_gate_fails_when_plan_missing(tmp_path):
    missing_file = tmp_path / "non_existent_plan.json"
    res = run_approval_gate([str(missing_file)])
    assert res.returncode == 1
    assert "НЕ НАЙДЕН" in res.stderr

    missing_dir = tmp_path / "empty_dir"
    missing_dir.mkdir(parents=True, exist_ok=True)
    res_dir = run_approval_gate([str(missing_dir)])
    assert res_dir.returncode == 1
