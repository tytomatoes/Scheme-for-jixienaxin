"""Run semantic edge cases and CLI integration checks without dependencies."""
import subprocess
import sys
from pathlib import Path
root = Path(__file__).resolve().parents[1]
tests = root / "tests"
cmd = [sys.executable, str(root / "src/main.py")]
result = subprocess.run(cmd + [str(tests / "edge_cases.scm")], capture_output=True, text=True, encoding="utf-8")
assert result.returncode == 0, result.stderr
assert result.stdout == (tests / "edge_cases.expected").read_text(encoding="utf-8"), result.stdout
result = subprocess.run(cmd + [str(tests / "shared_1.scm"), str(tests / "shared_2.scm")], capture_output=True, text=True)
assert result.returncode == 0 and result.stdout == "shared\n42\n", result.stderr
result = subprocess.run(cmd, input="(+ 1 2)", capture_output=True, text=True)
assert result.returncode == 0 and result.stdout == "3\n", result.stderr
print("PASS: semantic edge cases, shared environment, stdin")
