"""SkillControl 101 — discover, load, and read a skill's parts.

Run from anywhere in the project:
    uv run python examples/case1.py
"""
import sys

from broskill.processing.path import find_root
from broskill.processing.skill import SkillControl

sys.stdout.reconfigure(encoding="utf-8")

root = find_root()
sc = SkillControl(root=root / "skills")

print("skills we've got:")
for skill in sc.list_skills():
    print(f"  - {skill.name}: {skill.description}")

body = sc.load_skill("read-file")
print("\nread-file's SKILL.md body:\n")
print(body)

script = sc.load_skill_extension("read-file", "scripts/read_file.py")
print("\nread-file's read_file.py:\n")
print(script)
