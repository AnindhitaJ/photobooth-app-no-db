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
photobox_block_match = re.search(r"const PHOTOBOX_DEFS = \[(.*?)\n  \];", text, re.S)
photostrip_block_match = re.search(r"const BUILTIN_FRAME_DEFS = \[(.*?)\n  \];", text, re.S)
photobox_block = photobox_block_match.group(1) if photobox_block_match else ''
photostrip_block = photostrip_block_match.group(1) if photostrip_block_match else ''
frame_count = len(re.findall(r"\{ id:'[^']+', category:'(?:Korean|Film|Elegant|Floral|Seasonal|Gaming|Pattern|Social Media)'", photostrip_block))
photobox_count = len(re.findall(r"\{ id:'photobox_[^']+', category:'(?:Basic|Korean|Film|Elegant|Floral|Seasonal|Gaming|Pattern|Social Media)', name:'", photobox_block))
color_count = len(re.findall(r"\{ label: '[^']+',\s+bg:", text))
slot_counts = [len(re.findall(rf"slots:{i},", photobox_block)) for i in range(1, 9)]
photobox_categories = ['Basic', 'Korean', 'Film', 'Elegant', 'Floral', 'Seasonal', 'Gaming', 'Pattern', 'Social Media']
category_counts = {
    category: len(re.findall(rf"category:'{re.escape(category)}'", photobox_block))
    for category in photobox_categories
}

if frame_count != 120:
    errors.append(f'expected 120 decorative templates, got {frame_count}')
if photobox_count != 30:
    errors.append(f'expected 30 photobox templates, got {photobox_count}')
if color_count != 26:
    errors.append(f'expected 26 basic colors, got {color_count}')
if re.search(r"text\(ctx, ['\"]print size", text, re.I):
    errors.append('photobox canvas still contains print-size text')
if re.search(r"FRAME\$\{slots\.length\}|slots\.length\} FRAME", text):
    errors.append('photobox canvas still contains frame-count text')
if slot_counts != [4, 4, 4, 4, 4, 4, 3, 3]:
    errors.append(f'unexpected photobox slot distribution: {slot_counts}')
if any(count == 0 for count in category_counts.values()):
    errors.append(f'one or more photobox theme categories are empty: {category_counts}')
if sum(category_counts.values()) != 30:
    errors.append(f'unexpected photobox category distribution: {category_counts}')
if "let currentCat = isPhotoboxMode ? 'Basic'" not in text:
    errors.append('photobox default category is not Basic')
if "return PHOTOBOX_CATEGORIES.map(category => ({ label: category, value: category }))" not in text:
    errors.append('photobox category tabs do not mirror photostrip themes')
if "function drawPhotostripBranding" not in text:
    errors.append('photostrip branding renderer is missing')
if "drawPhotostripBranding(ctx, { text: colorObj.text" not in text:
    errors.append('basic photostrip templates are missing LUX branding')
if "drawPhotostripBranding(ctx, def, slots);" not in text:
    errors.append('decorative photostrip templates are missing LUX branding')
for brand_label in ['LUX PHOTOBOOTH', 'lux photobooth']:
    if brand_label not in text:
        errors.append(f'missing photostrip brand label: {brand_label}')

social_match = re.search(r"function drawSocialDecor\(ctx, def\) \{(.*?)\n  \}\n\s*function drawHeaderRibbon", text, re.S)
social_block = social_match.group(1) if social_match else ''
if social_block.count('luxphotobooth.id') < 1:
    errors.append(f'social media templates do not consistently use luxphotobooth.id: {social_block.count("luxphotobooth.id")} occurrences')
for old_social_brand in ['luxphotobootd.id', 'lux.photobooth', '@luxphotobooth']:
    if old_social_brand in social_block:
        errors.append(f'old social identity remains: {old_social_brand}')


# Social photostrip geometry: compact 3-photo layout with no generic name zone.
for token in [
    "sidePad = 76;", "topPad = 156;", "bottomPad = 168;", "gap = 32;",
    "if (def.category !== 'Social Media') drawNameZone(ctx, def, slots);"
]:
    if token not in text:
        errors.append(f'missing compact social layout safeguard: {token}')
if "const SOCIAL_ID = 'luxphotobooth.id';" not in social_block:
    errors.append('Instagram/TikTok social identity is not luxphotobooth.id')
if 'metadata is rendered inside each photo card' not in text:
    errors.append('social inter-slot metadata cleanup is missing')
if 'luxphotobootd.id' in text:
    errors.append('misspelled luxphotobootd.id remains in template.html')

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

# Ganci local-only export must never depend on the removed Auth module.
ganci_print = (ROOT / 'ganci-print.js').read_text(encoding='utf-8')
if 'Auth.exportCanvasDataURL' in ganci_print:
    errors.append('ganci-print.js still depends on removed Auth helper')
if ".toDataURL('image/jpeg', 0.98)" not in ganci_print:
    errors.append('ganci print JPEG canvas export is missing')

if errors:
    print('VALIDATION FAILED')
    for error in errors:
        print('-', error)
    sys.exit(1)

print(
    f'OK: {frame_count} decorative + {color_count} basic photostrip templates; '
    f'{photobox_count} photobox templates; slot groups {slot_counts}; themes {category_counts}; merge output 1181x1772.'
)
