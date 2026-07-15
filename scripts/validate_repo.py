from pathlib import Path
import re, sys

ROOT = Path(__file__).resolve().parents[1]
ACTIVE = ['index.html','template.html','camera.html','filter.html','result.html','ganci.html']
FORBIDDEN = [r'supabase', r'/login', r'photo_sessions', r'content_sharing_settings']
errors = []

for name in ACTIVE:
    path = ROOT / name
    if not path.exists():
        errors.append(f'missing {name}')
        continue
    text = path.read_text(encoding='utf-8').lower()
    for token in FORBIDDEN:
        if re.search(token, text):
            errors.append(f'{name}: forbidden backend/login token {token}')

text = (ROOT/'template.html').read_text(encoding='utf-8')
frame_count = len(re.findall(r"\{ id:'[^']+', category:'(?:Korean|Film|Elegant|Floral|Seasonal|Gaming|Pattern|Social Media)'", text))
photobox_count = len(re.findall(r"\{ id:'photobox_[^']+', name:'", text))
color_count = len(re.findall(r"\{ label: '[^']+',\s+bg:", text))
if frame_count < 120: errors.append(f'only {frame_count} decorative templates')
if photobox_count < 18: errors.append(f'only {photobox_count} photobox templates')
if color_count < 16: errors.append(f'only {color_count} basic colors')

for removed in ['login.html','admin.html','cms.html','gallery.html','api','supabase']:
    if (ROOT/removed).exists(): errors.append(f'backend/removed artifact still present: {removed}')

if errors:
    print('VALIDATION FAILED')
    for err in errors: print('-', err)
    sys.exit(1)
print(f'OK: {frame_count} decorative + {color_count} basic photostrip templates; {photobox_count} photobox templates.')
