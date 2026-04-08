import glob
import hashlib
import html
import io
import os
import re
import shutil
import unicodedata
import urllib.parse
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

# Configuration
BASE_DIR = Path(r"c:\Users\since\Blue Ocean\whiskey_blog")
CONTENT_DIR = BASE_DIR / "content"
DOCS_DIR = BASE_DIR / "docs"
PUBLIC_DIR = BASE_DIR / "public"
IMAGES_DIR = BASE_DIR / "images"
PRODUCT_SOURCE_DIRS = [
    DOCS_DIR / "images" / "products",
    PUBLIC_DIR / "images" / "products",
    IMAGES_DIR / "products",
]

AMAZON_TAG = "keny0823-22"

LOCAL_IMAGE_SPECS = {
    "chita_washoku.png": {
        "source": "chita_washoku.png",
        "slug": "chita-japanese-food-pairing",
        "alt": "サントリー知多と和食のペアリングイメージ",
        "title": "知多と和食のペアリング",
    },
    "islay_whisky.png": {
        "source": "islay_whisky.png",
        "slug": "islay-whisky-tasting-image",
        "alt": "アイラウイスキーのテイスティングイメージ",
        "title": "アイラウイスキーのテイスティングイメージ",
    },
    "monkey_shoulder_cola.png": {
        "source": "monkey_shoulder_cola.png",
        "slug": "monkey-shoulder-cola-highball",
        "alt": "モンキーショルダーのコーラ割りイメージ",
        "title": "モンキーショルダーのコーラ割り",
    },
    "monkey_cola.png": {
        "source": "monkey_shoulder_cola.png",
        "slug": "monkey-shoulder-cola-highball",
        "alt": "モンキーショルダーのコーラ割りイメージ",
        "title": "モンキーショルダーのコーラ割り",
    },
    "talisker_pepper.png": {
        "source": "talisker_pepper.png",
        "slug": "talisker-pepper-highball",
        "alt": "タリスカーのペッパー系ハイボールイメージ",
        "title": "タリスカーのスパイシーなハイボール",
    },
}

PRODUCT_META = {
    "B0DHKQBHBD": {"name": "グレンモーレンジィ オリジナル", "slug": "glenmorangie-original"},
    "B01MZ2B5GO": {"name": "メーカーズマーク", "slug": "makers-mark-bourbon"},
    "B011WPDV70": {"name": "サントリー 知多", "slug": "suntory-chita"},
    "B075HQ6QJD": {"name": "ボウモア 12年", "slug": "bowmore-12"},
    "B002EPBL1Q": {"name": "タリスカー 10年", "slug": "talisker-10"},
    "B085KWKPB4": {"name": "グレンフィディック 12年", "slug": "glenfiddich-12"},
    "B01LW0GC0R": {"name": "マッカラン 12年 ダブルカスク", "slug": "macallan-12-double-cask"},
    "B0F4QNQ5S7": {"name": "モンキーショルダー", "slug": "monkey-shoulder"},
    "B01BOTRYB8": {"name": "シーバスリーガル ミズナラ 12年", "slug": "chivas-regal-mizunara-12"},
    "B002VZY7KW": {"name": "アードベッグ 10年", "slug": "ardbeg-10"},
    "B001HUA0P2": {"name": "ラフロイグ 10年", "slug": "laphroaig-10"},
    "B000VHL7AY": {"name": "バランタイン 12年", "slug": "ballantines-12"},
    "B004ZK2T0O": {"name": "グレンリベット 12年", "slug": "glenlivet-12"},
    "B000VHL7BK": {"name": "ジョニーウォーカー ブラックラベル", "slug": "johnnie-walker-black-label"},
    "B0015BPBVY": {"name": "サントリー オールド", "slug": "suntory-old"},
    "B000VHL7C4": {"name": "デュワーズ 12年", "slug": "dewars-12"},
}

UNAVAILABLE_ASINS = {
    "B000VHL7AY",
    "B000VHL7BK",
    "B000VHL7C4",
    "B0015BPBVY",
    "B001HUA0P2",
    "B002VZY7KW",
    "B004ZK2T0O",
}

FONT_PATH = Path(r"C:\Windows\Fonts\NotoSansJP-VF.ttf")

CSS_CONTENT = """
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;0,700;1,400&family=Inter:wght@300;400;500;600&family=Noto+Sans+JP:wght@300;400;500;700&family=Noto+Serif+JP:wght@400;500;600;700&display=swap');

:root {
    --bg: #0a0a0f;
    --bg-warm: #0e0c08;
    --surface: rgba(22, 20, 16, 0.85);
    --surface-solid: #161410;
    --surface-hover: rgba(30, 27, 20, 0.95);
    --surface-glass: rgba(255, 255, 255, 0.03);
    --amber: #c8973e;
    --amber-light: #e8c46d;
    --amber-glow: rgba(200, 151, 62, 0.15);
    --amber-subtle: rgba(200, 151, 62, 0.06);
    --text: #ddd8d0;
    --text-bright: #f0ece4;
    --text-muted: #8a8478;
    --text-dim: #5a554d;
    --border: rgba(200, 151, 62, 0.08);
    --border-hover: rgba(200, 151, 62, 0.25);
    --radius: 16px;
    --radius-sm: 10px;
    --shadow-ambient: 0 8px 40px rgba(0, 0, 0, 0.4);
    --shadow-glow: 0 0 60px rgba(200, 151, 62, 0.06);
    --transition: cubic-bezier(0.22, 1, 0.36, 1);
}

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html { scroll-behavior: smooth; }

body {
    font-family: 'Inter', 'Noto Sans JP', -apple-system, BlinkMacSystemFont, sans-serif;
    background-color: var(--bg);
    color: var(--text);
    line-height: 1.95;
    font-weight: 300;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    overflow-x: hidden;
}

body::before {
    content: '';
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background:
        radial-gradient(ellipse 80% 50% at 50% 0%, rgba(200, 130, 40, 0.08) 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 80% 100%, rgba(140, 80, 20, 0.06) 0%, transparent 50%);
    box-shadow: inset 0 0 120px rgba(0, 0, 0, 0.85);
    pointer-events: none;
    z-index: 999;
}

/* ===== HEADER ===== */
.site-header {
    background: rgba(10, 10, 15, 0.75);
    border-bottom: 1px solid var(--border);
    padding: 0 24px;
    position: sticky;
    top: 0;
    z-index: 1000;
    backdrop-filter: blur(20px) saturate(1.8);
    -webkit-backdrop-filter: blur(20px) saturate(1.8);
    transition: background 0.4s var(--transition);
}
.header-inner {
    max-width: 1000px;
    margin: 0 auto;
    display: flex;
    align-items: center;
    justify-content: space-between;
    height: 64px;
}
.site-logo {
    font-family: 'Cormorant Garamond', serif;
    color: var(--amber-light);
    font-size: 22px;
    font-weight: 600;
    text-decoration: none;
    letter-spacing: 2px;
    text-transform: uppercase;
    transition: color 0.3s;
    position: relative;
}
.site-logo::after {
    content: '';
    position: absolute;
    bottom: -4px;
    left: 0;
    width: 100%;
    height: 1px;
    background: linear-gradient(90deg, var(--amber), transparent);
    opacity: 0.4;
}
.site-logo:hover { color: #fff; }

nav {
    display: flex;
    gap: 2px;
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
}
nav::-webkit-scrollbar { display: none; }
nav a {
    color: var(--text-muted);
    text-decoration: none;
    font-size: 12px;
    font-weight: 500;
    padding: 8px 16px;
    border-radius: var(--radius-sm);
    white-space: nowrap;
    letter-spacing: 0.5px;
    text-transform: uppercase;
    transition: all 0.3s var(--transition);
    position: relative;
}
nav a:hover {
    color: var(--amber-light);
    background: var(--amber-subtle);
}

/* ===== CONTAINER ===== */
.container {
    max-width: 760px;
    margin: 0 auto;
    padding: 48px 24px 100px;
    position: relative;
    z-index: 1;
}

/* ===== ARTICLE ===== */
article {
    background: none;
    padding: 0;
}
article h1 {
    font-family: 'Cormorant Garamond', 'Noto Serif JP', serif;
    color: var(--text-bright);
    font-size: 36px;
    font-weight: 700;
    line-height: 1.4;
    margin-bottom: 40px;
    letter-spacing: 0.5px;
}
article h2 {
    font-family: 'Cormorant Garamond', 'Noto Serif JP', serif;
    color: var(--amber-light);
    font-size: 24px;
    font-weight: 600;
    margin-top: 56px;
    margin-bottom: 20px;
    padding: 0 0 12px 0;
    border-bottom: 1px solid var(--border);
    letter-spacing: 0.3px;
    position: relative;
}
article h2::after {
    content: '';
    position: absolute;
    bottom: -1px;
    left: 0;
    width: 60px;
    height: 2px;
    background: linear-gradient(90deg, var(--amber), transparent);
}
article h3 {
    font-family: 'Cormorant Garamond', 'Noto Serif JP', serif;
    color: var(--text-bright);
    font-size: 18px;
    font-weight: 500;
    margin-top: 36px;
    margin-bottom: 14px;
    letter-spacing: 0.2px;
}
article p, article li {
    color: var(--text);
    font-size: 15px;
    line-height: 2;
    font-weight: 300;
}
article ul, article ol {
    padding-left: 20px;
    margin: 20px 0;
}
article li {
    margin-bottom: 10px;
    padding-left: 4px;
}
article li::marker {
    color: var(--amber);
}
article strong {
    color: var(--amber-light);
    font-weight: 600;
}
article a {
    color: var(--amber);
    text-decoration: none;
    border-bottom: 1px solid rgba(200, 151, 62, 0.2);
    transition: all 0.3s var(--transition);
}
article a:hover {
    color: var(--amber-light);
    border-bottom-color: var(--amber);
}
article hr {
    border: none;
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--border-hover), transparent);
    margin: 48px 0;
}
article img {
    display: block;
    max-width: 100%;
    height: auto;
    border-radius: var(--radius);
}
.content-image {
    width: 100%;
    margin: 28px auto;
    border: 1px solid rgba(200, 151, 62, 0.08);
    box-shadow: var(--shadow-ambient);
}

/* ===== PRODUCT CARD ===== */
.product-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 36px 28px;
    margin: 36px auto;
    max-width: 480px;
    text-align: center;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 20px;
    transition: all 0.4s var(--transition);
    position: relative;
    overflow: hidden;
    box-shadow: var(--shadow-ambient);
}
.product-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--amber), transparent);
    opacity: 0;
    transition: opacity 0.4s;
}
.product-card:hover {
    border-color: var(--border-hover);
    transform: translateY(-4px);
    box-shadow: var(--shadow-ambient), var(--shadow-glow);
}
.product-card:hover::before { opacity: 0.6; }
.product-card a { display: inline-block; }
.product-card img {
    max-width: 200px;
    width: 100%;
    height: auto;
    margin: 0 auto;
    border-radius: var(--radius-sm);
    transition: transform 0.4s var(--transition);
}
.product-card:hover img { transform: scale(1.03); }
.product-card iframe {
    border: 0;
    max-width: 100%;
}

/* ===== BUTTON ===== */
.btn {
    display: inline-block;
    background: linear-gradient(135deg, var(--amber) 0%, #a67c28 100%);
    color: #0a0a0f !important;
    padding: 14px 36px;
    text-decoration: none !important;
    border: none;
    border-bottom: none !important;
    border-radius: var(--radius-sm);
    font-weight: 600;
    font-size: 13px;
    letter-spacing: 0.8px;
    text-transform: uppercase;
    margin: 12px 0;
    transition: all 0.3s var(--transition);
    cursor: pointer;
    position: relative;
    overflow: hidden;
}
.btn::after {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.15), transparent);
    transition: left 0.5s;
}
.btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 24px rgba(200, 151, 62, 0.3);
    border-bottom: none !important;
}
.btn:hover::after { left: 100%; }

/* ===== ARTICLE GRID ===== */
.article-grid {
    display: grid;
    gap: 20px;
    margin-top: 40px;
}
.article-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 28px 24px;
    text-decoration: none;
    transition: all 0.4s var(--transition);
    display: block;
    position: relative;
    overflow: hidden;
    box-shadow: 0 2px 16px rgba(0, 0, 0, 0.2);
}
.article-card::before {
    content: '';
    position: absolute;
    left: 0;
    top: 0;
    bottom: 0;
    width: 3px;
    background: linear-gradient(180deg, var(--amber), transparent);
    opacity: 0;
    transition: opacity 0.4s;
}
.article-card:hover {
    border-color: var(--border-hover);
    background: var(--surface-hover);
    transform: translateY(-3px) translateX(2px);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3), 0 0 40px rgba(200, 151, 62, 0.04);
}
.article-card:hover::before { opacity: 1; }
.article-card h3 {
    font-family: 'Noto Serif JP', serif;
    color: var(--text-bright);
    font-size: 16px;
    font-weight: 500;
    margin: 0 0 10px;
    line-height: 1.6;
    transition: color 0.3s;
}
.article-card:hover h3 { color: #fff; }
.article-card p {
    color: var(--text-muted);
    font-size: 13px;
    margin: 0;
    line-height: 1.7;
    font-weight: 300;
}

/* ===== HERO ===== */
.hero {
    text-align: center;
    padding: 80px 0 48px;
    position: relative;
}
.hero::before {
    content: '';
    position: absolute;
    top: -20px;
    left: 50%;
    transform: translateX(-50%);
    width: 200px;
    height: 200px;
    background: radial-gradient(circle, rgba(200, 151, 62, 0.08) 0%, transparent 70%);
    pointer-events: none;
}
.hero h1 {
    font-family: 'Cormorant Garamond', serif;
    color: var(--text-bright);
    font-size: 42px;
    font-weight: 700;
    margin-bottom: 8px;
    line-height: 1.2;
    letter-spacing: 3px;
    text-transform: uppercase;
}
.hero-subtitle {
    font-family: 'Cormorant Garamond', serif;
    color: var(--amber);
    font-size: 14px;
    font-weight: 400;
    letter-spacing: 6px;
    text-transform: uppercase;
    margin-bottom: 24px;
    display: block;
}
.hero p {
    color: var(--text-muted);
    font-size: 15px;
    line-height: 1.9;
    font-weight: 300;
}
.hero-divider {
    width: 60px;
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--amber), transparent);
    margin: 32px auto;
}

/* ===== FOOTER ===== */
.footer {
    text-align: center;
    padding: 48px 24px;
    font-size: 11px;
    font-weight: 300;
    color: var(--text-dim);
    border-top: 1px solid var(--border);
    margin-top: 80px;
    letter-spacing: 1px;
}
.footer a { color: var(--text-muted); text-decoration: none; }
.footer a:hover { color: var(--amber); }

/* ===== SCROLLBAR ===== */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb {
    background: rgba(200, 151, 62, 0.15);
    border-radius: 3px;
}
::-webkit-scrollbar-thumb:hover { background: rgba(200, 151, 62, 0.3); }

/* ===== SELECTION ===== */
::selection {
    background: rgba(200, 151, 62, 0.25);
    color: var(--text-bright);
}

/* ===== RESPONSIVE ===== */
@media (max-width: 600px) {
    .header-inner { height: 56px; }
    .site-logo { font-size: 18px; letter-spacing: 1.5px; }
    nav a { font-size: 11px; padding: 6px 12px; }
    .container { padding: 28px 18px 60px; }
    article h1 { font-size: 26px; margin-bottom: 28px; }
    article h2 { font-size: 20px; margin-top: 40px; }
    article h3 { font-size: 16px; }
    article p, article li { font-size: 14px; }
    .hero { padding: 52px 0 28px; }
    .hero h1 { font-size: 30px; letter-spacing: 2px; }
    .hero-subtitle { font-size: 11px; letter-spacing: 4px; }
    .product-card { padding: 20px 16px; }
    .product-card img { max-width: 160px; }
    .btn { padding: 12px 28px; font-size: 12px; }
    .article-card { padding: 20px 18px; }
    .article-card h3 { font-size: 15px; }
}

@media (min-width: 601px) and (max-width: 900px) {
    .container { max-width: 680px; }
    article h1 { font-size: 30px; }
    .hero h1 { font-size: 36px; }
}
"""

TEMPLATE = """<!DOCTYPE html>
<html lang="ja">
<head>
    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-VZEJ7T9HXZ"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){{dataLayer.push(arguments);}}
      gtag('js', new Date());
      gtag('config', 'G-VZEJ7T9HXZ');
    </script>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{description}">
    <title>{title} | Whiskey Guide</title>
    <link rel="stylesheet" href="style.css?v=1.2">
</head>
<body>
    <header class="site-header">
        <div class="header-inner">
            <a href="index.html" class="site-logo">Whiskey Guide</a>
            <nav>
                <a href="index.html">HOME</a>
                <a href="article1.html">甘口</a>
                <a href="article2.html">ハイボール</a>
                <a href="article3.html">プレゼント</a>
                <a href="article4.html">アイラ</a>
                <a href="article7.html">コスパ</a>
            </nav>
        </div>
    </header>

    <div class="container">
        <article>
            {content}
        </article>
    </div>

    <div class="footer">
        <p>Premium Whiskey Discoveries</p>
        <p style="margin-top: 8px;">&copy; 2026 Whiskey Guide. All rights reserved.</p>
    </div>
</body>
</html>
"""


def slugify(value):
    normalized = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    cleaned = re.sub(r"[^a-zA-Z0-9]+", "-", normalized.lower()).strip("-")
    return cleaned or "image"


def ensure_dir(path):
    Path(path).mkdir(parents=True, exist_ok=True)


def collect_product_sources():
    sources = {}
    for directory in PRODUCT_SOURCE_DIRS:
        if not directory.exists():
            continue
        for path in directory.glob("*.jpg"):
            if path.stat().st_size > 1000:
                sources[path.stem.upper()] = path
    return sources


def optimize_image_to_webp(source_path, output_dir, slug, max_width=1200, quality=82):
    ensure_dir(output_dir)
    with Image.open(source_path) as image:
        image = image.convert("RGB")
        if image.width > max_width:
            ratio = max_width / float(image.width)
            image = image.resize((int(image.width * ratio), int(image.height * ratio)), Image.LANCZOS)

        buffer = io.BytesIO()
        image.save(buffer, format="WEBP", quality=quality, method=6, optimize=True)
        payload = buffer.getvalue()
        digest = hashlib.md5(payload).hexdigest()[:8]
        filename = f"{slug}-{digest}.webp"
        target_path = Path(output_dir) / filename
        target_path.write_bytes(payload)
        return {
            "filename": filename,
            "width": image.width,
            "height": image.height,
            "size": len(payload),
        }


def get_font(size):
    try:
        return ImageFont.truetype(str(FONT_PATH), size)
    except Exception:
        return ImageFont.load_default()


def wrap_lines(draw, text, font, max_width):
    chars = list(text)
    lines = []
    current = ""
    for char in chars:
        candidate = current + char
        if current and draw.textlength(candidate, font=font) > max_width:
            lines.append(current)
            current = char
        else:
            current = candidate
    if current:
        lines.append(current)
    return lines


def create_placeholder_webp(output_dir, slug, title, subtitle):
    ensure_dir(output_dir)
    width, height = 500, 500
    image = Image.new("RGB", (width, height), "#18120d")
    draw = ImageDraw.Draw(image)

    for y in range(height):
        mix = y / max(1, height - 1)
        r = int(24 + (84 - 24) * mix)
        g = int(18 + (46 - 18) * mix)
        b = int(13 + (22 - 13) * mix)
        draw.line([(0, y), (width, y)], fill=(r, g, b))

    draw.rounded_rectangle((24, 24, width - 24, height - 24), radius=28, outline="#c9a84c", width=3)
    draw.rounded_rectangle((42, 42, width - 42, height - 42), radius=24, outline="#5a4820", width=1)
    draw.text((44, 58), "Whiskey Guide", font=get_font(24), fill="#e8d48b")
    draw.text((44, 94), subtitle, font=get_font(18), fill="#d0c4ad")

    title_font = get_font(42)
    max_text_width = width - 88
    lines = wrap_lines(draw, title, title_font, max_text_width)
    if len(lines) > 4:
        lines = lines[:4]

    line_height = 56
    start_y = 170
    for index, line in enumerate(lines):
        draw.text((44, start_y + index * line_height), line, font=title_font, fill="#ffffff")

    draw.rounded_rectangle((44, height - 120, width - 44, height - 60), radius=18, fill="#c9a84c")
    draw.text((66, height - 107), "商品画像取得不可のため代替表示", font=get_font(18), fill="#1b1409")

    buffer = io.BytesIO()
    image.save(buffer, format="WEBP", quality=82, method=6)
    payload = buffer.getvalue()
    digest = hashlib.md5(payload).hexdigest()[:8]
    filename = f"{slug}-{digest}.webp"
    target_path = Path(output_dir) / filename
    target_path.write_bytes(payload)
    return {"filename": filename, "width": width, "height": height, "size": len(payload)}


def build_asset_registry(output_dir):
    registry = {"content": {}, "products": {}}
    images_output_dir = Path(output_dir) / "images"
    product_output_dir = images_output_dir / "products"
    ensure_dir(images_output_dir)
    ensure_dir(product_output_dir)

    for alias, spec in LOCAL_IMAGE_SPECS.items():
        source_path = IMAGES_DIR / spec["source"]
        if not source_path.exists():
            continue
        optimized = optimize_image_to_webp(source_path, images_output_dir, spec["slug"])
        registry["content"][alias] = {
            "src": f"images/{optimized['filename']}",
            "width": optimized["width"],
            "height": optimized["height"],
            "alt": spec["alt"],
            "title": spec["title"],
        }

    for asin, source_path in collect_product_sources().items():
        meta = PRODUCT_META.get(asin, {"name": f"Amazon商品 {asin}", "slug": f"amazon-product-{asin.lower()}"})
        optimized = optimize_image_to_webp(source_path, product_output_dir, meta["slug"], max_width=500, quality=80)
        registry["products"][asin] = {
            "src": f"images/products/{optimized['filename']}",
            "width": optimized["width"],
            "height": optimized["height"],
            "alt": f"{meta['name']} の商品画像",
            "title": meta["name"],
        }

    for asin, meta in PRODUCT_META.items():
        if asin in registry["products"]:
            continue
        placeholder = create_placeholder_webp(product_output_dir, meta["slug"], meta["name"], f"ASIN: {asin}")
        registry["products"][asin] = {
            "src": f"images/products/{placeholder['filename']}",
            "width": placeholder["width"],
            "height": placeholder["height"],
            "alt": f"{meta['name']} の代替商品画像",
            "title": meta["name"],
        }
    return registry


def parse_img_attrs(tag):
    return dict(re.findall(r'([a-zA-Z:-]+)="(.*?)"', tag))


def build_img_tag(attrs):
    ordered_keys = [
        "src",
        "alt",
        "title",
        "loading",
        "decoding",
        "width",
        "height",
        "class",
        "style",
    ]
    ordered = []
    used = set()
    for key in ordered_keys:
        if key in attrs and attrs[key]:
            ordered.append(f'{key}="{html.escape(str(attrs[key]), quote=True)}"')
            used.add(key)
    for key in sorted(k for k in attrs.keys() if k not in used):
        if attrs[key]:
            ordered.append(f'{key}="{html.escape(str(attrs[key]), quote=True)}"')
    return "<img " + " ".join(ordered) + ">"


def rewrite_image_tags(html_text, asset_registry):
    def replacer(match):
        tag = match.group(0)
        attrs = parse_img_attrs(tag)
        src = attrs.get("src", "")
        basename = os.path.basename(src)

        if basename in asset_registry["content"]:
            asset = asset_registry["content"][basename]
            attrs["src"] = asset["src"]
            attrs["alt"] = asset["alt"]
            attrs["title"] = asset["title"]
            attrs["width"] = str(asset["width"])
            attrs["height"] = str(asset["height"])
            attrs["loading"] = "lazy"
            attrs["decoding"] = "async"
            attrs["class"] = "content-image"

        attrs.setdefault("loading", "lazy")
        attrs.setdefault("decoding", "async")
        if attrs.get("alt") and not attrs.get("title"):
            attrs["title"] = attrs["alt"]

        return build_img_tag(attrs)

    return re.sub(r"<img\b[^>]*>", replacer, html_text)


def make_amazon_widget(asin, asset_registry):
    product_image = asset_registry["products"].get(asin)
    product_meta = PRODUCT_META.get(asin, {"name": f"Amazon商品 {asin}"})
    product_name = product_meta["name"]
    if asin in UNAVAILABLE_ASINS:
        query = urllib.parse.quote_plus(f"{product_name} ウイスキー")
        amazon_url = f"https://www.amazon.co.jp/s?k={query}&tag={AMAZON_TAG}"
        button_label = "Amazonで候補商品を見る"
    else:
        amazon_url = f"https://www.amazon.co.jp/dp/{asin}?tag={AMAZON_TAG}"
        button_label = "Amazonで詳細・購入はこちら"

    if product_image:
        return (
            f'<div class="product-card">'
            f'<a href="{amazon_url}" target="_blank" rel="nofollow sponsored noopener">'
            f'<img src="{product_image["src"]}" alt="{product_image["alt"]}" title="{product_name}" '
            f'loading="lazy" decoding="async" width="{product_image["width"]}" height="{product_image["height"]}"></a>'
            f'<a href="{amazon_url}" target="_blank" rel="nofollow sponsored noopener" class="btn" '
            f'title="{product_name}をAmazonで見る">{button_label}</a>'
            f'</div>'
        )

    return (
        f'<div class="product-card">'
        f'<iframe src="https://rcm-fe.amazon-adsystem.com/e/cm?lt1=_blank&bc1=000000&IS2=1'
        f'&bg1=1a1a1a&fc1=c9a84c&lc1=c9a84c&t={AMAZON_TAG}&language=ja_JP&o=9&p=8&l=as4'
        f'&m=amazon&f=ifr&ref=as_ss_li_til&asins={asin}" '
        f'style="width:120px;height:240px;" scrolling="no" marginwidth="0" marginheight="0" '
        f'frameborder="0" loading="lazy" title="{product_name}のAmazon商品カード"></iframe>'
        f'<a href="{amazon_url}" target="_blank" rel="nofollow sponsored noopener" class="btn" '
        f'title="{product_name}をAmazonで見る">{button_label}</a>'
        f'</div>'
    )


def md_to_html(md_text, asset_registry):
    html_text = md_text

    desc_match = re.search(r"^Description: (.*?)$", html_text, re.MULTILINE)
    description = desc_match.group(1) if desc_match else ""
    html_text = re.sub(r"^Description: .*?$", "", html_text, flags=re.MULTILINE)

    html_text = re.sub(
        r"^AMAZON:\s*(\w+)\s*$",
        lambda m: make_amazon_widget(m.group(1), asset_registry),
        html_text,
        flags=re.MULTILINE,
    )

    def replace_old_amazon_block(match):
        asin_match = re.search(r"/dp/([A-Z0-9]{10})", match.group(0))
        if asin_match:
            return make_amazon_widget(asin_match.group(1), asset_registry)
        return match.group(0)

    html_text = re.sub(
        r'<div style="text-align: center; margin: 20px 0;">.*?</div>',
        replace_old_amazon_block,
        html_text,
        flags=re.DOTALL,
    )

    html_text = re.sub(r"^---\s*$", "<hr>", html_text, flags=re.MULTILINE)
    html_text = re.sub(r"^### (.*?)$", r"<h3>\1</h3>", html_text, flags=re.MULTILINE)
    html_text = re.sub(r"^## (.*?)$", r"<h2>\1</h2>", html_text, flags=re.MULTILINE)
    html_text = re.sub(r"^# (.*?)$", r"<h1>\1</h1>", html_text, flags=re.MULTILINE)
    html_text = re.sub(r"^\*   (.*?)$", r"<li>\1</li>", html_text, flags=re.MULTILINE)
    html_text = re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", html_text)
    html_text = re.sub(r"!\[(.*?)\]\((.*?)\)", r'<img src="\2" alt="\1">', html_text)
    html_text = re.sub(r"\[(.*?)\]\((.*?)\)", r'<a href="\2">\1</a>', html_text)

    lines = html_text.split("\n")
    result = []
    for line in lines:
        stripped = line.strip()
        if not stripped:
            result.append("")
        elif stripped.startswith("<"):
            result.append(line)
        elif stripped.startswith("*"):
            result.append(line)
        else:
            result.append(f"<p>{stripped}</p>")
    html_text = "\n".join(result)

    html_text = re.sub(r"((?:<li>.*?</li>\n?)+)", r"<ul>\1</ul>", html_text)
    html_text = re.sub(r"\n{3,}", "\n\n", html_text)
    html_text = rewrite_image_tags(html_text.strip(), asset_registry)

    return html_text, description


def build_output(output_dir):
    asset_registry = build_asset_registry(output_dir)

    with open(Path(output_dir) / "style.css", "w", encoding="utf-8") as file:
        file.write(CSS_CONTENT)

    articles = []
    for md_file in glob.glob(str(CONTENT_DIR / "*.md")):
        name = Path(md_file).stem
        with open(md_file, "r", encoding="utf-8") as file:
            raw_content = file.read()

        title_match = re.search(r"^# (.*?)$", raw_content, re.MULTILINE)
        title = title_match.group(1) if title_match else "Untitled"

        desc_match = re.search(r"^Description: (.*?)$", raw_content, re.MULTILINE)
        card_desc = desc_match.group(1) if desc_match else ""
        if len(card_desc) > 80:
            card_desc = card_desc[:80] + "..."

        html_body, description = md_to_html(raw_content, asset_registry)
        if not description:
            description = f"{title} - ウイスキーの選び方・楽しみ方を解説"

        final_html = TEMPLATE.format(title=title, description=description, content=html_body)
        with open(Path(output_dir) / f"{name}.html", "w", encoding="utf-8") as file:
            file.write(final_html)

        if name != "product":
            articles.append({"title": title, "url": f"{name}.html", "order": name, "desc": card_desc})

    articles.sort(key=lambda item: item["order"])

    index_body = """
    <div class="hero">
        <span class="hero-subtitle">The Finest Selection</span>
        <h1>Whiskey Guide</h1>
        <div class="hero-divider"></div>
        <p>初心者から通まで。<br>あなたにぴったりの一杯が見つかるウイスキーメディア。</p>
    </div>

    <div class="article-grid">
    """
    for article in articles:
        index_body += f'''
        <a href="{article["url"]}" class="article-card">
            <h3>{article["title"]}</h3>
            <p>{article["desc"]}</p>
        </a>'''
    index_body += "\n    </div>"

    final_index = TEMPLATE.format(
        title="HOME",
        description="初心者から通まで。あなたにぴったりの一杯が見つかるウイスキーメディア。",
        content=index_body,
    )
    with open(Path(output_dir) / "index.html", "w", encoding="utf-8") as file:
        file.write(final_index)

    return len(articles)


def reset_output_dirs():
    for directory in (DOCS_DIR, PUBLIC_DIR):
        if directory.exists():
            for item in directory.iterdir():
                try:
                    if item.is_dir():
                        shutil.rmtree(item)
                    else:
                        item.unlink()
                except Exception:
                    pass
        ensure_dir(directory)


def build_site():
    reset_output_dirs()
    article_count = build_output(DOCS_DIR)
    shutil.rmtree(PUBLIC_DIR)
    shutil.copytree(DOCS_DIR, PUBLIC_DIR)
    print(f"Success! Built {article_count} articles in: {DOCS_DIR}")
    print(f"Mirrored optimized site to: {PUBLIC_DIR}")


if __name__ == "__main__":
    build_site()
