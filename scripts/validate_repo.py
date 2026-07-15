from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
ACTIVE = [
    'index.html', 'template.html', 'camera.html', 'filter.html',
    'result.html', 'ganci.html', 'merge-strips.html'
]
FORBIDDEN = [r'supabase', r'/login', r'photo_sessions', r'content_sharing_settings']
errors = []

for name in ACTIVE:
    path = ROOT / name
    if not path.exists():
        errors.append(f'missing {name}')
        continue
    page_text = path.read_text(encoding='utf-8').lower()
    for token in FORBIDDEN:
        if re.search(token, page_text):
            errors.append(f'{name}: forbidden backend/login token {token}')

text = (ROOT / 'template.html').read_text(encoding='utf-8')
frame_count = len(re.findall(r"\{ id:'[^']+', category:'(?:Korean|Film|Elegant|Floral|Seasonal|Gaming|Pattern|Social Media)'", text))
photobox_count = len(re.findall(r"\{ id:'photobox_[^']+', name:'", text))
color_count = len(re.findall(r"\{ label: '[^']+',\s+bg:", text))
slot_counts = [len(re.findall(rf"slots:{i},", text)) for i in range(1, 9)]

if frame_count != 120:
    errors.append(f'expected 120 decorative templates, got {frame_count}')
if photobox_count != 30:
    errors.append(f'expected 30 photobox templates, got {photobox_count}')
if color_count != 26:
    errors.append(f'expected 26 basic colors, got {color_count}')
if slot_counts != [3, 4, 4, 5, 4, 4, 3, 3]:
    errors.append(f'unexpected photobox slot distribution: {slot_counts}')

index_text = (ROOT / 'index.html').read_text(encoding='utf-8')
sw_text = (ROOT / 'sw.js').read_text(encoding='utf-8')
merge_text = (ROOT / 'merge-strips.html').read_text(encoding='utf-8')
if '/merge-strips.html' not in index_text:
    errors.append('merge-strips route missing from index.html')
if '/merge-strips.html' not in sw_text:
    errors.append('merge-strips route missing from service worker cache')
if 'const OUTPUT_W = 1181' not in merge_text or 'const OUTPUT_H = 1772' not in merge_text:
    errors.append('merge output is not fixed at 1181x1772')
if 'accept="image/*"' not in merge_text:
    errors.append('merge page image inputs missing')

for removed in ['login.html', 'admin.html', 'cms.html', 'gallery.html', 'api', 'supabase']:
    if (ROOT / removed).exists():
        errors.append(f'backend/removed artifact still present: {removed}')

if errors:
    print('VALIDATION FAILED')
    for error in errors:
        print('-', error)
    sys.exit(1)

print(
    f'OK: {frame_count} decorative + {color_count} basic photostrip templates; '
    f'{photobox_count} photobox templates; slot groups {slot_counts}; merge output 1181x1772.'
)
