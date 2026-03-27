import glob
import hashlib
import html
import io
import os
import re
import shutil
import unicodedata
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

FONT_PATH = Path(r"C:\Windows\Fonts\NotoSansJP-VF.ttf")

CSS_CONTENT = """
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;700&family=Playfair+Display:wght@700&display=swap');

:root {
    --bg: #0f0f0f;
    --surface: #1a1a1a;
    --surface-hover: #242424;
    --gold: #c9a84c;
    --gold-light: #e8d48b;
    --text: #e8e8e8;
    --text-muted: #999;
    --border: #2a2a2a;
    --radius: 12px;
}

* { box-sizing: border-box; margin: 0; padding: 0; }

body {
    font-family: 'Noto Sans JP', -apple-system, BlinkMacSystemFont, sans-serif;
    background-color: var(--bg);
    color: var(--text);
    line-height: 1.9;
    -webkit-font-smoothing: antialiased;
}

.site-header {
    background: linear-gradient(180deg, #000 0%, #0a0a0a 100%);
    border-bottom: 1px solid var(--border);
    padding: 0 20px;
    position: sticky;
    top: 0;
    z-index: 100;
    backdrop-filter: blur(12px);
}
.header-inner {
    max-width: 960px;
    margin: 0 auto;
    display: flex;
    align-items: center;
    justify-content: space-between;
    height: 60px;
}
.site-logo {
    font-family: 'Playfair Display', serif;
    color: var(--gold);
    font-size: 20px;
    text-decoration: none;
    letter-spacing: 1px;
}

nav {
    display: flex;
    gap: 4px;
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
}
nav::-webkit-scrollbar { display: none; }
nav a {
    color: var(--text-muted);
    text-decoration: none;
    font-size: 13px;
    padding: 8px 14px;
    border-radius: 8px;
    white-space: nowrap;
    transition: all 0.2s;
}
nav a:hover {
    color: var(--gold);
    background: var(--surface);
}

.container {
    max-width: 720px;
    margin: 0 auto;
    padding: 40px 20px 80px;
}

article {
    background: none;
    padding: 0;
}
article h1 {
    font-family: 'Playfair Display', 'Noto Sans JP', serif;
    color: #fff;
    font-size: 32px;
    line-height: 1.4;
    margin-bottom: 32px;
}
article h2 {
    color: var(--gold);
    font-size: 22px;
    margin-top: 48px;
    margin-bottom: 16px;
    padding: 0 0 8px 0;
    border-bottom: 1px solid var(--border);
}
article h3 {
    color: #fff;
    font-size: 18px;
    margin-top: 32px;
    margin-bottom: 12px;
}
article p, article li {
    color: var(--text);
    font-size: 15px;
    line-height: 1.9;
}
article ul, article ol {
    padding-left: 24px;
    margin: 16px 0;
}
article li {
    margin-bottom: 8px;
}
article strong {
    color: var(--gold-light);
}
article a {
    color: var(--gold);
    text-decoration: none;
    border-bottom: 1px solid transparent;
    transition: border-color 0.2s;
}
article a:hover {
    border-bottom-color: var(--gold);
}
article hr {
    border: none;
    border-top: 1px solid var(--border);
    margin: 40px 0;
}
article img {
    display: block;
    max-width: 100%;
    height: auto;
    border-radius: var(--radius);
}
.content-image {
    width: 100%;
    margin: 24px auto;
    border: 1px solid rgba(255, 255, 255, 0.06);
    background: var(--surface);
}

.product-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 32px 24px;
    margin: 32px auto;
    max-width: 480px;
    text-align: center;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 16px;
    transition: border-color 0.3s, box-shadow 0.3s;
}
.product-card:hover {
    border-color: var(--gold);
    box-shadow: 0 4px 24px rgba(201, 168, 76, 0.1);
}
.product-card a {
    display: inline-block;
}
.product-card img {
    max-width: 200px;
    width: 100%;
    height: auto;
    margin: 0 auto;
    border-radius: 8px;
}
.product-card iframe {
    border: 0;
    max-width: 100%;
}

.btn {
    display: inline-block;
    background: linear-gradient(135deg, var(--gold), #b8952e);
    color: #000 !important;
    padding: 14px 32px;
    text-decoration: none !important;
    border: none;
    border-bottom: none !important;
    border-radius: 8px;
    font-weight: 700;
    font-size: 14px;
    margin: 12px 0;
    transition: transform 0.2s, box-shadow 0.2s;
    cursor: pointer;
}
.btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 20px rgba(201, 168, 76, 0.3);
    border-bottom: none !important;
}

.article-grid {
    display: grid;
    gap: 16px;
    margin-top: 32px;
}
.article-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 24px;
    text-decoration: none;
    transition: all 0.25s;
    display: block;
}
.article-card:hover {
    border-color: var(--gold);
    background: var(--surface-hover);
    transform: translateY(-2px);
}
.article-card h3 {
    color: #fff;
    font-size: 17px;
    margin: 0 0 8px;
    line-height: 1.5;
}
.article-card p {
    color: var(--text-muted);
    font-size: 13px;
    margin: 0;
}

.hero {
    text-align: center;
    padding: 60px 0 40px;
}
.hero h1 {
    font-family: 'Playfair Display', serif;
    color: #fff;
    font-size: 36px;
    margin-bottom: 16px;
    line-height: 1.3;
}
.hero p {
    color: var(--text-muted);
    font-size: 16px;
    line-height: 1.8;
}

.footer {
    text-align: center;
    padding: 40px 20px;
    font-size: 12px;
    color: #555;
    border-top: 1px solid var(--border);
    margin-top: 60px;
}

@media (max-width: 600px) {
    .header-inner { height: 52px; }
    .site-logo { font-size: 17px; }
    nav a { font-size: 12px; padding: 6px 10px; }
    .container { padding: 24px 16px 60px; }
    article h1 { font-size: 24px; }
    article h2 { font-size: 19px; margin-top: 36px; }
    article p, article li { font-size: 14px; }
    .hero { padding: 40px 0 24px; }
    .hero h1 { font-size: 26px; }
    .product-card { padding: 16px; }
    .product-card img { max-width: 160px; }
    .btn { padding: 12px 24px; font-size: 13px; }
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
    <link rel="stylesheet" href="style.css">
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
        <p>&copy; 2026 Whiskey Guide. All rights reserved.</p>
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
    amazon_url = f"https://www.amazon.co.jp/dp/{asin}?tag={AMAZON_TAG}"
    product_image = asset_registry["products"].get(asin)
    product_meta = PRODUCT_META.get(asin, {"name": f"Amazon商品 {asin}"})
    product_name = product_meta["name"]

    if product_image:
        return (
            f'<div class="product-card">'
            f'<a href="{amazon_url}" target="_blank" rel="nofollow sponsored noopener">'
            f'<img src="{product_image["src"]}" alt="{product_image["alt"]}" title="{product_name}" '
            f'loading="lazy" decoding="async" width="{product_image["width"]}" height="{product_image["height"]}"></a>'
            f'<a href="{amazon_url}" target="_blank" rel="nofollow sponsored noopener" class="btn" '
            f'title="{product_name}をAmazonで見る">Amazonで詳細・購入はこちら</a>'
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
        f'title="{product_name}をAmazonで見る">Amazonで詳細・購入はこちら</a>'
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
        <h1>Whiskey Guide</h1>
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
            shutil.rmtree(directory)
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
