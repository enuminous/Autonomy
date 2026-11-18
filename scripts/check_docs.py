"""Check local Markdown file links without fetching external resources."""
from pathlib import Path
import re

root = Path(__file__).resolve().parents[1]
errors = []
for file in root.rglob('*.md'):
    if any(part in {'.git', '.venv', 'artifacts'} for part in file.relative_to(root).parts):
        continue
    for target in re.findall(r'\]\(([^)]+)\)', file.read_text()):
        if '://' in target or target.startswith('#'):
            continue
        target = target.split('#', 1)[0]
        if target and not (file.parent / target).exists():
            errors.append(f'{file.relative_to(root)}: missing {target}')
if errors:
    raise SystemExit('\n'.join(errors))
print('Local Markdown links resolve.')
