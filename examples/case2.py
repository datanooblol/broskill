"""ToolControl 101 — turn a skill's script into a callable tool schema, then run it.

Run from anywhere in the project:
    uv run python examples/case2.py
"""
import subprocess
import sys

from broskill.processing.path import find_root
from broskill.processing.skill import SkillControl
from broskill.processing.tool import ToolControl, to_args

root = find_root()
sc = SkillControl(root=root / "skills")
sc.load_skill("read-file")

tc = ToolControl(sc)
tool = tc.load_tool("read-file", "scripts/list_files.py")

print(f"tool: {tool.name}")
print(f"description: {tool.description}")
for arg in tool.args:
    print(f"  - {arg.name} ({arg.type}, required={arg.required}): {arg.description}")

result = subprocess.run(
    [sys.executable, str(tool.path), *to_args({"path": "skills/**/*.md"})],
    capture_output=True, text=True, cwd=root,
)
print("\noutput:\n")
print(result.stdout)
