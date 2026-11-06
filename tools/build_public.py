"""Turn the artifact page (site/index.html) into a public static site (public/) for GitHub Pages.
Usage: python3 build_public.py DOMAIN   e.g. kloungesiquijor.com"""
import json, os, re, shutil, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(HERE, '..', 'site')
OUT = os.path.join(HERE, '..', 'public')
FONT = '/mnt/attach/project-files/brand/fonts/JosefinSans-Variable.ttf'
DOMAIN = sys.argv[1] if len(sys.argv) > 1 else 'kloungesiquijor.com'
BASE = 'https://%s/' % DOMAIN

src = open(os.path.join(SITE, 'index.html'), encoding='utf-8').read()
src = re.sub(r'^<title>.*?</title>\n', '', src)
src = re.sub(r'<meta name="claude:[^>]*>\n', '', src)
head_part, body_part = src.split('</style>', 1)
head_part += '</style>'

ig = 'https://www.instagram.com/'; fb = 'https://www.facebook.com/'; tt = 'https://www.tiktok.com/@'
addr = {"@type": "PostalAddress", "streetAddress": "Lalao", "addressLocality": "San Juan",
        "addressRegion": "Siquijor", "addressCountry": "PH"}
allweek = {"@type": "OpeningHoursSpecification",
           "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
           "opens": "00:00", "closes": "23:59"}
ld = {"@context": "https://schema.org", "@graph": [
    {"@type": "LodgingBusiness", "@id": BASE + "#stay", "name": "K Stay Lounge", "url": BASE,
     "telephone": "+63 962 565 0876", "address": addr, "priceRange": "₱4,600–₱5,800 per night",
     "hasMap": "https://www.google.com/maps?cid=14456365166156686497", "image": BASE + "media/bld-3.jpg",
     "amenityFeature": [{"@type": "LocationFeatureSpecification", "name": n, "value": True}
                        for n in ["Starlink Wi-Fi", "Air conditioning", "Solar power", "Sea-view balcony"]],
     "sameAs": [ig + "kstaylounge/", fb + "kstaylounge", tt + "kstaylounge"]},
    {"@type": "CafeOrCoffeeShop", "@id": BASE + "#sip", "name": "K Sip Lounge", "url": BASE,
     "telephone": "+63 962 565 0876", "address": addr, "openingHoursSpecification": allweek,
     "servesCuisine": ["Coffee", "Sandwiches", "Halo-halo"], "menu": BASE + "media/menu.jpg",
     "hasMap": "https://www.google.com/maps?cid=3700748620220942777", "image": BASE + "media/sip-a.jpg",
     "sameAs": [ig + "ksiplounge/", fb + "1034306786441687", tt + "ksiplounge"]},
    {"@type": "TouristAttraction", "@id": BASE + "#heavensdoor", "name": "Heaven's Door", "url": BASE,
     "address": addr, "image": BASE + "media/hd-a.jpg",
     "sameAs": [ig + "heavensdoorsiquijor/", fb + "1307277505811933", tt + "heavens_door_siquijor"]}]}

title = "K Lounge Siquijor · Beachfront stay & 24/7 café in San Juan"
desc = ("K Stay Lounge sea-view rooms and K Sip Lounge, a 24/7 café on the beach in Lalao, San Juan, Siquijor. "
        "Today's sunset time, room prices, menu, Heaven's Door and KAKA the café cat.")
head = '''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{t}</title>
<meta name="description" content="{d}">
<link rel="canonical" href="{b}">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="icon" href="favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<meta name="theme-color" content="#f3f6f5" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#0c1f25" media="(prefers-color-scheme: dark)">
<meta property="og:type" content="website">
<meta property="og:site_name" content="K Lounge Siquijor">
<meta property="og:title" content="K Lounge Siquijor">
<meta property="og:description" content="Stay steps from the sand. Sip slow, day or night. Sunset served daily.">
<meta property="og:url" content="{b}">
<meta property="og:image" content="{b}og.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<script type="application/ld+json">{ld}</script>
'''.format(t=title, d=desc, b=BASE, ld=json.dumps(ld, ensure_ascii=False))
html = head + head_part + '\n</head>\n<body>\n' + body_part.strip() + '\n</body>\n</html>\n'

if os.path.isdir(OUT): shutil.rmtree(OUT)
os.makedirs(os.path.join(OUT, 'media'))
open(os.path.join(OUT, 'index.html'), 'w', encoding='utf-8').write(html)
used = sorted(set(re.findall(r'media/([\w.-]+)', html)) - {'menu.jpg"'})
for f in used:
    shutil.copy2(os.path.join(SITE, 'media', f), os.path.join(OUT, 'media', f))

# Icons: Orange 1 chip (orange circle, palm-green line mark = logo A "Sunset reflection")
mark = ('<line x1="14" y1="74" x2="106" y2="74"/><path d="M40 74 A20 20 0 0 1 80 74"/>'
        '<line x1="44" y1="84" x2="76" y2="84"/><line x1="50" y1="93" x2="70" y2="93"/>'
        '<line x1="56" y1="102" x2="64" y2="102"/>')
svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120"><circle cx="60" cy="60" r="60" fill="#e8684a"/>'
       '<g transform="translate(60 60) scale(1.15) translate(-60 -72)" fill="none" stroke="#2F4A3A" stroke-width="5" '
       'stroke-linecap="square">' + mark + '</g></svg>')
open(os.path.join(OUT, 'favicon.svg'), 'w').write(svg)

def chip(size):
    s = 4 * size; im = Image.new('RGBA', (s, s), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.ellipse([0, 0, s - 1, s - 1], fill='#e8684a')
    k = s / 120 * 1.15; ox, oy = s / 2 - 60 * k, s / 2 - 72 * k
    P = lambda x, y: (ox + x * k, oy + y * k); w = max(2, int(5 * s / 120))
    for x1, y, x2 in [(14, 74, 106), (44, 84, 76), (50, 93, 70), (56, 102, 64)]:
        d.line([P(x1, y), P(x2, y)], fill='#2F4A3A', width=w)
    cx, cy = P(60, 74); r = 20 * k
    d.arc([cx - r, cy - r, cx + r, cy + r], 180, 360, fill='#2F4A3A', width=w)
    return im.resize((size, size), Image.LANCZOS)
chip(180).save(os.path.join(OUT, 'apple-touch-icon.png'))
chip(32).save(os.path.join(OUT, 'favicon-32.png'))

# Share preview image 1200x630: sunset photo + orange mark + K LOUNGE
ph = Image.open(os.path.join(SITE, 'media', 'sun-a.jpg')).convert('RGB')
w, h = ph.size; bh = int(w * 630 / 1200); top = int((h - bh) * 0.55)
og = ph.crop((0, top, w, top + bh)).resize((1200, 630), Image.LANCZOS)
shade = Image.new('L', (1200, 630), 0); sd = ImageDraw.Draw(shade)
for x in range(1200): sd.line([(x, 0), (x, 630)], fill=int(170 * max(0, 1 - x / 760)))
og = Image.composite(Image.new('RGB', og.size, (8, 26, 31)), og, shade)
d = ImageDraw.Draw(og)
f1 = ImageFont.truetype(FONT, 92); f1.set_variation_by_axes([300])
f2 = ImageFont.truetype(FONT, 30); f2.set_variation_by_axes([400])
f3 = ImageFont.truetype(FONT, 34); f3.set_variation_by_axes([600])
k = 1.6; ox, oy = 80, 70; P = lambda x, y: (ox + x * k, oy + y * k)
for x1, y, x2 in [(14, 74, 106), (44, 84, 76), (50, 93, 70), (56, 102, 64)]:
    d.line([P(x1, y), P(x2, y)], fill='#ff8a6b', width=5)
cx, cy = P(60, 74); r = 20 * k
d.arc([cx - r, cy - r, cx + r, cy + r], 180, 360, fill='#ff8a6b', width=5)
d.text((86, 250), 'K LOUNGE', font=f1, fill='white', spacing=0)
d.text((92, 360), 'SIQUIJOR  ·  PHILIPPINES', font=f2, fill='#ffd2c2')
d.text((92, 440), 'Stay · Sea · Sip · Sunset', font=f3, fill='#ff8a6b')
d.text((92, 492), 'Beachfront rooms & 24/7 café', font=f2, fill='white')
og.save(os.path.join(OUT, 'og.jpg'), quality=85)

open(os.path.join(OUT, 'robots.txt'), 'w').write('User-agent: *\nAllow: /\nSitemap: %ssitemap.xml\n' % BASE)
open(os.path.join(OUT, 'sitemap.xml'), 'w').write(
    '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
    '<url><loc>%s</loc></url></urlset>\n' % BASE)
open(os.path.join(OUT, '404.html'), 'w').write(
    '<!doctype html><meta charset="utf-8"><title>K Lounge Siquijor</title>'
    '<meta http-equiv="refresh" content="0; url=/"><a href="/">K Lounge Siquijor</a>\n')
open(os.path.join(OUT, '.nojekyll'), 'w').write('')
open(os.path.join(OUT, 'CNAME'), 'w').write(DOMAIN + '\n')
print('built', OUT, 'media files:', len(used))
