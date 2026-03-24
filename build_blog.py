import os
import re
import glob
import shutil

# Configuration
BASE_DIR = r"c:\Users\since\Blue Ocean\whiskey_blog"
CONTENT_DIR = os.path.join(BASE_DIR, "content")
OUTPUT_DIR = os.path.join(BASE_DIR, "docs")
IMAGES_DIR = os.path.join(BASE_DIR, "images")

# CSS Content (Externalized)
CSS_CONTENT = """
body {
    font-family: "Garamond", "Times New Roman", serif;
    background-color: #121212;
    color: #e0e0e0;
    margin: 0;
    padding: 0;
    line-height: 1.8;
}
header {
    background-color: #000;
    padding: 20px;
    text-align: center;
    border-bottom: 2px solid #d4af37; /* Gold */
}
header h1 {
    margin: 0;
    color: #d4af37;
    font-size: 24px;
    letter-spacing: 2px;
}
nav {
    text-align: center;
    padding: 10px;
    background: #1e1e1e;
    border-bottom: 1px solid #333;
}
nav a {
    color: #fff;
    text-decoration: none;
    margin: 0 15px;
    font-size: 14px;
    transition: color 0.3s;
}
nav a:hover {
    color: #d4af37;
}
.container {
    max-width: 800px;
    margin: 40px auto;
    padding: 0 20px;
}
article {
    background: #1e1e1e;
    padding: 40px;
    border-radius: 5px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.5);
}
h1 {
    color: #d4af37;
    font-size: 28px;
    border-bottom: 1px solid #333;
    padding-bottom: 15px;
}
h2 {
    color: #fff;
    border-left: 4px solid #d4af37;
    padding-left: 15px;
    margin-top: 40px;
}
a {
    color: #d4af37;
    text-decoration: underline;
}
.btn {
    display: inline-block;
    background: #d4af37;
    color: #000 !important;
    padding: 15px 30px;
    text-decoration: none;
    border-radius: 30px;
    font-weight: bold;
    margin: 20px 0;
    text-align: center;
    transition: background 0.3s;
}
.btn:hover {
    background: #f1c40f;
}
.footer {
    text-align: center;
    padding: 40px;
    font-size: 12px;
    color: #666;
    border-top: 1px solid #333;
    margin-top: 60px;
}
img {
    max-width: 100%;
    border-radius: 5px;
    height: auto;
}

/* Mobile Optimization */
@media (max-width: 600px) {
    body { font-size: 16px; }
    .container { margin: 20px auto; padding: 0 15px; }
    article { padding: 25px 15px; }
    h1 { font-size: 24px; }
    h2 { font-size: 20px; }
    nav { padding: 10px 5px; }
    nav a {
        display: inline-block;
        margin: 5px 8px;
        font-size: 12px;
    }
    header h1 { font-size: 20px; }
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
    <title>{title} | Gentleman's Whiskey Guide</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <header>
        <h1>Gentleman's Whiskey Guide</h1>
    </header>
    <nav>
        <a href="index.html">HOME</a>
        <a href="article1.html">甘口銘柄</a>
        <a href="article2.html">ハイボール</a>
        <a href="article3.html">プレゼント</a>
        <a href="article4.html">アイラ・モルト</a>
        <a href="product.html">公式ガイド</a>
    </nav>
    
    <div class="container">
        <article>
            {content}
        </article>
    </div>

    <div class="footer">
        <p>&copy; 2026 Gentleman's Whiskey Guide. All rights reserved.</p>
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
    
    # Headers
    html = re.sub(r'^# (.*?)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.*?)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
    # Bold
    html = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html)
    # Paragraphs
    html = re.sub(r'\n\n', r'<br><br>', html)
    # Images with alt
    html = re.sub(r'!\[(.*?)\]\((.*?)\)', r'<img src="\2" alt="\1">', html)
    # Links
    html = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', html)
    # Amazon Link styling
    html = re.sub(r'<a href="(.*?)">(.*?Amazon.*?)</a>', r'<div class="affiliate-link"><a href="\1" target="_blank" class="btn">\2</a></div>', html)
    
    return html.strip(), description

def build_site():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    # Write style.css
    with open(os.path.join(OUTPUT_DIR, "style.css"), "w", encoding="utf-8") as f:
        f.write(CSS_CONTENT)

    # Copy images
    images_dst = os.path.join(OUTPUT_DIR, "images")
    if os.path.exists(IMAGES_DIR):
        if os.path.exists(images_dst): shutil.rmtree(images_dst)
        shutil.copytree(IMAGES_DIR, images_dst)

    articles = []
    # Process MD files
    for md_file in glob.glob(os.path.join(CONTENT_DIR, "*.md")):
        name = os.path.splitext(os.path.basename(md_file))[0]
        with open(md_file, "r", encoding="utf-8") as f:
            raw_content = f.read()
        
        title_match = re.search(r'^# (.*?)$', raw_content, re.MULTILINE)
        title = title_match.group(1) if title_match else "Untitled"
        
        html_body, description = md_to_html(raw_content)
        if not description: description = f"{title}に関する大人のためのウイスキーガイド。"
        
        final_html = TEMPLATE.format(title=title, description=description, content=html_body)
        
        output_path = os.path.join(OUTPUT_DIR, f"{name}.html")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(final_html)
        
        if name != "product":
            articles.append({"title": title, "url": f"{name}.html", "order": name})

    # Sort articles
    articles.sort(key=lambda x: x["order"])

    # Index Page
    index_body = """
    <h1>ようこそ、ウイスキーの迷宮へ</h1>
    <p>Barでの振る舞い、おすすめの銘柄、失敗しないプレゼント選び。<br>30代から始める、大人の男性のためのウイスキー情報を発信します。</p>
    
    <h2>新着記事</h2>
    <ul>
    """
    for art in articles:
        index_body += f'<li><a href="{art["url"]}">{art["title"]}</a></li>'
    index_body += "</ul>"
    
    index_body += """
    <hr>
    <h2>【電子書籍】30代からのウイスキー入門</h2>
    <p>「Barで恥をかきたくない」あなたへ。一生使える知識を凝縮しました。</p>
    <a href="product.html" class="btn">詳細を見る</a>
    """
    
    final_index = TEMPLATE.format(title="HOME", description="大人の男性のためのウイスキーガイド。Barの嗜みから投資銘柄まで、本物の知識を届けます。", content=index_body)
    with open(os.path.join(OUTPUT_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(final_index)

    print(f"Success! Site refactored and built in: {OUTPUT_DIR}")

if __name__ == "__main__":
    build_site()
