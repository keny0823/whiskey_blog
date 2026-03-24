import os
import re
import glob
import shutil

# Configuration
BASE_DIR = r"c:\Users\since\Blue Ocean\whiskey_blog"
CONTENT_DIR = os.path.join(BASE_DIR, "content")
OUTPUT_DIR = os.path.join(BASE_DIR, "docs")
IMAGES_DIR = os.path.join(BASE_DIR, "images")

# CSS Content — Modern dark design
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

/* ── Header ── */
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

/* ── Nav ── */
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

/* ── Container ── */
.container {
    max-width: 720px;
    margin: 0 auto;
    padding: 40px 20px 80px;
}

/* ── Article ── */
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
    border: none;
    padding: 0;
}
article h2 {
    color: var(--gold);
    font-size: 22px;
    margin-top: 48px;
    margin-bottom: 16px;
    padding: 0 0 8px 0;
    border-left: none;
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
    max-width: 100%;
    height: auto;
    border-radius: var(--radius);
}

/* ── Product Card (Amazon) ── */
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
    display: block;
}

/* ── CTA Button ── */
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

/* ── Index: Article Cards ── */
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

/* ── Hero (Index) ── */
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

/* ── Footer ── */
.footer {
    text-align: center;
    padding: 40px 20px;
    font-size: 12px;
    color: #555;
    border-top: 1px solid var(--border);
    margin-top: 60px;
}

/* ── Mobile ── */
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

# HTML Template
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

def md_to_html(md_text):
    html = md_text
    # Extract description
    desc_match = re.search(r'^Description: (.*?)$', html, re.MULTILINE)
    description = desc_match.group(1) if desc_match else ""
    html = re.sub(r'^Description: .*?$', '', html, flags=re.MULTILINE)

    # Horizontal rules
    html = re.sub(r'^---\s*$', '<hr>', html, flags=re.MULTILINE)

    # Headers
    html = re.sub(r'^### (.*?)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.*?)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^# (.*?)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)

    # Unordered list items
    html = re.sub(r'^\*   (.*?)$', r'<li>\1</li>', html, flags=re.MULTILINE)

    # Bold
    html = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html)

    # Images with alt
    html = re.sub(r'!\[(.*?)\]\((.*?)\)', r'<img src="\2" alt="\1">', html)

    # Links
    html = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', html)

    # Strip inline styles from img tags (let CSS handle layout)
    html = re.sub(r'<img ([^>]*)style="[^"]*"', r'<img \1', html)

    # Wrap Amazon product blocks in product-card divs
    html = re.sub(
        r'<div style="text-align: center; margin: 20px 0;">(.*?)</div>',
        r'<div class="product-card">\1</div>',
        html, flags=re.DOTALL
    )

    # Amazon Link styling — btn class
    html = re.sub(
        r'<a href="(.*?)"[^>]*class="btn">(.*?)</a>',
        r'<a href="\1" target="_blank" rel="nofollow" class="btn">\2</a>',
        html
    )

    # Remove stray <br> inside product-card
    html = re.sub(r'(<div class="product-card">.*?)</div>',
                  lambda m: m.group(1).replace('<br>', '') + '</div>',
                  html, flags=re.DOTALL)

    # Paragraphs — wrap loose text lines
    lines = html.split('\n')
    result = []
    for line in lines:
        stripped = line.strip()
        if not stripped:
            result.append('')
        elif stripped.startswith('<'):
            result.append(line)
        elif stripped.startswith('*'):
            result.append(line)
        else:
            result.append(f'<p>{stripped}</p>')
    html = '\n'.join(result)

    # Wrap consecutive <li> in <ul>
    html = re.sub(r'((?:<li>.*?</li>\n?)+)', r'<ul>\1</ul>', html)

    # Clean up empty lines
    html = re.sub(r'\n{3,}', '\n\n', html)

    return html.strip(), description

def build_site():
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
    os.makedirs(OUTPUT_DIR)

    # Write style.css
    with open(os.path.join(OUTPUT_DIR, "style.css"), "w", encoding="utf-8") as f:
        f.write(CSS_CONTENT)

    # Copy images
    images_dst = os.path.join(OUTPUT_DIR, "images")
    if os.path.exists(IMAGES_DIR):
        shutil.copytree(IMAGES_DIR, images_dst)

    articles = []
    # Process MD files
    for md_file in glob.glob(os.path.join(CONTENT_DIR, "*.md")):
        name = os.path.splitext(os.path.basename(md_file))[0]
        with open(md_file, "r", encoding="utf-8") as f:
            raw_content = f.read()

        title_match = re.search(r'^# (.*?)$', raw_content, re.MULTILINE)
        title = title_match.group(1) if title_match else "Untitled"

        # Extract description for card
        desc_match = re.search(r'^Description: (.*?)$', raw_content, re.MULTILINE)
        card_desc = desc_match.group(1)[:80] + "..." if desc_match and len(desc_match.group(1)) > 80 else (desc_match.group(1) if desc_match else "")

        html_body, description = md_to_html(raw_content)
        if not description:
            description = f"{title} - ウイスキーの選び方・楽しみ方を解説"

        final_html = TEMPLATE.format(title=title, description=description, content=html_body)

        output_path = os.path.join(OUTPUT_DIR, f"{name}.html")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(final_html)

        if name != "product":
            articles.append({"title": title, "url": f"{name}.html", "order": name, "desc": card_desc})

    # Sort articles
    articles.sort(key=lambda x: x["order"])

    # Index Page
    index_body = """
    <div class="hero">
        <h1>Whiskey Guide</h1>
        <p>初心者から通まで。<br>あなたにぴったりの一杯が見つかるウイスキーメディア。</p>
    </div>

    <div class="article-grid">
    """
    for art in articles:
        index_body += f'''
        <a href="{art["url"]}" class="article-card">
            <h3>{art["title"]}</h3>
            <p>{art["desc"]}</p>
        </a>'''
    index_body += "\n    </div>"

    final_index = TEMPLATE.format(
        title="HOME",
        description="初心者から通まで。あなたにぴったりの一杯が見つかるウイスキーメディア。",
        content=index_body
    )
    with open(os.path.join(OUTPUT_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(final_index)

    print(f"Success! Built {len(articles)} articles in: {OUTPUT_DIR}")

if __name__ == "__main__":
    build_site()
