"""Script to replace Streamlit deprecated `use_container_width` kwarg
with the new `width` parameter across the frontend folder.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / 'frontend'

patterns = [
    (re.compile(r'use_container_width\s*=\s*True'), "width='stretch'"),
    (re.compile(r'use_container_width\s*=\s*False'), "width='content'"),
]

files = list(ROOT.rglob('*.py'))
changed = 0
for p in files:
    text = p.read_text(encoding='utf-8')
    new = text
    for pat, rep in patterns:
        new = pat.sub(rep, new)
    if new != text:
        p.write_text(new, encoding='utf-8')
        changed += 1

print(f"Rewrote {changed} files containing use_container_width replacements.")
