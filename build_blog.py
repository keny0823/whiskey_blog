import os
import re
import glob

# Configuration
CONTENT_DIR = r"c:\Users\since\新しいフォルダー\trend_arbitrage_project\whiskey_blog\content"
OUTPUT_DIR = r"c:\Users\since\新しいフォルダー\trend_arbitrage_project\whiskey_blog\docs"

# HTML Template (Dark/Gold Theme)
TEMPLATE = """
<!DOCTYPE html>
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
    <title>{title} | Gentleman's Whiskey</title>
    <style>
        body {{
            font-family: "Garamond", "Times New Roman", serif;
            background-color: #121212;
            color: #e0e0e0;
            margin: 0;
            padding: 0;
            line-height: 1.8;
        }}
        header {{
            background-color: #000;
            padding: 20px;
            text-align: center;
            border-bottom: 2px solid #d4af37; /* Gold */
        }}
        header h1 {{
            margin: 0;
            color: #d4af37;
            font-size: 24px;
            letter-spacing: 2px;
        }}
        nav {{
            text-align: center;
            padding: 10px;
            background: #1e1e1e;
        }}
        nav a {{
            color: #fff;
            text-decoration: none;
            margin: 0 15px;
            font-size: 14px;
        }}
        nav a:hover {{
            color: #d4af37;
        }}
        .container {{
            max-width: 800px;
            margin: 40px auto;
            padding: 0 20px;
        }}
        article {{
            background: #1e1e1e;
            padding: 40px;
            border-radius: 5px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        }}
        h1 {{
            color: #d4af37;
            font-size: 28px;
            border-bottom: 1px solid #333;
            padding-bottom: 15px;
        }}
        h2 {{
            color: #fff;
            border-left: 4px solid #d4af37;
            padding-left: 15px;
            margin-top: 40px;
        }}
        a {{
            color: #d4af37;
            text-decoration: underline;
        }}
        .btn {{
            display: inline-block;
            background: #d4af37;
            color: #000;
            padding: 15px 30px;
            text-decoration: none;
            border-radius: 30px;
            font-weight: bold;
            margin: 20px 0;
            text-align: center;
        }}
        .btn:hover {{
            background: #f1c40f;
        }}
        .footer {{
            text-align: center;
            padding: 40px;
            font-size: 12px;
            color: #666;
            border-top: 1px solid #333;
            margin-top: 60px;
        }}
        img {{
            max-width: 100%;
            border-radius: 5px;
        }}
        /* ... existing styles ... */
        
        /* Mobile Optimization */
        @media (max-width: 600px) {{
            body {{
                font-size: 16px; /* 読みやすいサイズに調整 */
            }}
            .container {{
                margin: 20px auto;
                padding: 0 15px;
            }}
            article {{
                padding: 20px; /* スマホでは余白を減らす */
            }}
            h1 {{
                font-size: 24px;
            }}
            h2 {{
                font-size: 20px;
                margin-top: 30px;
            }}
            nav {{
                padding: 15px 5px;
            }}
            nav a {{
                display: block; /* 縦並びにして押しやすく */
                margin: 10px 0;
                font-size: 16px;
                border: 1px solid #333;
                padding: 10px;
                border-radius: 5px;
            }}
            header h1 {{
                font-size: 20px;
            }}
            .affiliate-link {{
                font-size: 0.8em;
            }}
        }}

    </style>
</head>
<body>
    <header>
        <h1>Gentleman's Whiskey Guide</h1>
    </header>
    <nav>
        <a href="index.html">HOME</a>
        <a href="product.html">電子書籍（商品）</a>
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
    # Basic Markdown parsing
    html = md_text
    
    # Headers
    html = re.sub(r'^# (.*?)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.*?)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
    
    # Bold
    html = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html)
    
    # Paragraphs (simple)
    html = re.sub(r'\n\n', r'<br><br>', html)
    
    # Links
    html = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', html)
    
    # Auto-style Amazon links as buttons
    html = re.sub(r'<a href="(.*?)">(.*?Amazon.*?)</a>', r'<div class="affiliate-link"><a href="\1" target="_blank" class="btn">\2</a></div>', html)
    
    return html

def build_site():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    articles = []

    # Process all markdown files
    for md_file in glob.glob(os.path.join(CONTENT_DIR, "*.md")):
        filename = os.path.basename(md_file)
        name_no_ext = os.path.splitext(filename)[0]
        
        with open(md_file, "r", encoding="utf-8") as f:
            content = f.read()
            
        # Extract title (first line)
        title_match = re.search(r'^# (.*?)$', content, re.MULTILINE)
        title = title_match.group(1) if title_match else "Untitled"
        
        html_content = md_to_html(content)
        final_html = TEMPLATE.format(title=title, content=html_content)
        
        output_path = os.path.join(OUTPUT_DIR, f"{name_no_ext}.html")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(final_html)
            
        # Add to list for index (exclude product page from general list if desired, but including is fine)
        if name_no_ext != "product":
            articles.append({"title": title, "url": f"{name_no_ext}.html"})

    # Create Index Page
    index_content = "<h1>ようこそ、ウイスキーの迷宮へ</h1><p>Barでの振る舞い、おすすめの銘柄、失敗しないプレゼント選び。大人の男性のための情報を発信します。</p>"
    index_content += "<h2>新着記事</h2><ul>"
    for art in articles:
        index_content += f'<li><a href="{art["url"]}">{art["title"]}</a></li>'
    index_content += "</ul>"
    
    # Add Product Promo to Index
    index_content += """
    <hr>
    <h2>【電子書籍】30代からのウイスキー入門</h2>
    <p>「Barで恥をかきたくない」あなたへ。一生使える知識を凝縮しました。</p>
    <a href="product.html" class="btn">詳細を見る</a>
    """

    final_index = TEMPLATE.format(title="HOME", content=index_content)
    with open(os.path.join(OUTPUT_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(final_index)

    print(f"Site built successfully in: {OUTPUT_DIR}")

if __name__ == "__main__":
    build_site()
