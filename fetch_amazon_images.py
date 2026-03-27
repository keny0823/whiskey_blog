"""
Amazon商品画像を自動ダウンロードしてdocs/images/products/に保存するスクリプト。
使い方: py -3.12 fetch_amazon_images.py
"""
import os
import re
import glob
import time
import urllib.request

BASE_DIR = r"c:\Users\since\Blue Ocean\whiskey_blog"
CONTENT_DIR = os.path.join(BASE_DIR, "content")
OUTPUT_DIR = os.path.join(BASE_DIR, "images", "products")

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept-Language': 'ja-JP,ja;q=0.9',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
}

def get_amazon_image_url(asin):
    """AmazonページからOG画像またはメイン商品画像URLを取得"""
    url = f'https://www.amazon.co.jp/dp/{asin}'
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=15) as res:
            html = res.read().decode('utf-8', errors='replace')

        # og:image を優先
        og = re.search(r'<meta[^>]+property="og:image"[^>]+content="([^"]+)"', html)
        if og:
            return og.group(1)

        # landingImage の large URL
        landing = re.search(r'"large":"(https://m\.media-amazon\.com/images/I/[^"]+)"', html)
        if landing:
            return landing.group(1)

        # hiRes
        hires = re.search(r'"hiRes":"(https://m\.media-amazon\.com/images/I/[^"]+)"', html)
        if hires:
            return hires.group(1)

    except Exception as e:
        print(f"  [ERROR] {asin}: {e}")
    return None

def download_image(img_url, save_path):
    """画像をダウンロードして保存"""
    req = urllib.request.Request(img_url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=15) as res:
            data = res.read()
        with open(save_path, 'wb') as f:
            f.write(data)
        return True
    except Exception as e:
        print(f"  [ERROR] download failed: {e}")
        return False

def extract_asins_from_md(md_file):
    """マークダウンファイルからASINを抽出"""
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()

    asins = set()
    # AMAZON: ASIN 形式
    for m in re.finditer(r'^AMAZON:\s*(\w+)', content, re.MULTILINE):
        asins.add(m.group(1))
    # <div style> 内の /dp/ASIN 形式
    for m in re.finditer(r'/dp/([A-Z0-9]{10})', content):
        asins.add(m.group(1))
    return asins

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # 全MDファイルからASINを収集
    all_asins = set()
    for md_file in glob.glob(os.path.join(CONTENT_DIR, "*.md")):
        asins = extract_asins_from_md(md_file)
        all_asins.update(asins)

    print(f"対象ASIN数: {len(all_asins)}")
    print(f"保存先: {OUTPUT_DIR}")
    print()

    success = 0
    skip = 0
    fail = 0

    for asin in sorted(all_asins):
        save_path = os.path.join(OUTPUT_DIR, f"{asin}.jpg")

        # 既存ファイルがあればスキップ
        if os.path.exists(save_path) and os.path.getsize(save_path) > 1000:
            print(f"  [SKIP] {asin} (既存)")
            skip += 1
            continue

        print(f"  [GET]  {asin} ...", end=" ", flush=True)
        img_url = get_amazon_image_url(asin)
        if not img_url:
            print("画像URL取得失敗")
            fail += 1
            time.sleep(2)
            continue

        ok = download_image(img_url, save_path)
        if ok:
            size = os.path.getsize(save_path)
            print(f"OK ({size:,} bytes)")
            success += 1
        else:
            fail += 1

        time.sleep(2)  # Amazon負荷対策

    print()
    print(f"完了: 成功={success}, スキップ={skip}, 失敗={fail}")

if __name__ == "__main__":
    main()
