#!/usr/bin/env python3
"""
generate_articles.py
Generates 5 new whiskey blog articles with luxury design and Amazon affiliate links.
Outputs to: public/article4.html ~ public/article8.html
Then pushes to GitHub.
"""

import re
import subprocess
from pathlib import Path
from urllib.parse import quote

PROJECT_ROOT = Path(__file__).parent
PUBLIC_DIR = PROJECT_ROOT / "public"
AFFILIATE_TAG = "keny0823-22"


def amazon_search_url(keyword: str) -> str:
    return f"https://www.amazon.co.jp/s?k={quote(keyword)}&tag={AFFILIATE_TAG}"


def strip_tags(html: str) -> str:
    return re.sub(r"<[^>]+>", "", html).replace("\n", " ").strip()


# ─── Article Data ─────────────────────────────────────────────────────────────

ARTICLES = [
    {
        "filename": "article4.html",
        "badge": "Beginner's Guide",
        "category": "入門ガイド",
        "title_html": (
            "「ウイスキー、何から飲めばいい？」迷える初心者に贈る<br>"
            '<span class="accent">はじめての5本</span>'
        ),
        "lead": [
            "「ウイスキーって種類が多すぎて、何を選べばいいかわからない」——そんな声をよく聞きます。",
            "実は、ウイスキー選びにはコツがあります。最初の一本さえ間違えなければ、あとは自然に好みが広がっていくものです。",
        ],
        "intro": (
            "この記事では、初心者が最初に手を伸ばすべき「飲みやすさ×コスパ」に優れた5本を厳選しました。"
            "どれもコンビニや酒屋で手に入りやすい銘柄です。"
        ),
        "whiskies": [
            {
                "name": "バランタイン 12年（スコッチ）",
                "search_key": "バランタイン 12年 ウイスキー",
                "description": (
                    "スコットランドの老舗ブレンデッドウイスキー。"
                    "<strong>ハチミツと花のような優しい甘さ</strong>で、口当たりが非常にマイルド。"
                    "「最初に飲んで良かった」と思えるレベルの完成度です。"
                    "世界でもっとも売れているウイスキーの一つで、初心者の登竜門的存在。"
                ),
                "details": [
                    ("おすすめの飲み方", "ハイボール、またはロック"),
                    ("価格帯", "2,500円〜3,500円"),
                    ("原産国", "スコットランド"),
                ],
            },
            {
                "name": "ジャック ダニエル（テネシー）",
                "search_key": "ジャックダニエル ウイスキー",
                "description": (
                    "アメリカを代表するテネシーウイスキー。"
                    "<strong>バニラとメープルシロップのような甘さ</strong>があり、"
                    "独特の「チャコール・メローイング製法」で驚くほど飲みやすく仕上げています。"
                    "コーラや炭酸水で割ると、さらにぐっと飲みやすくなります。"
                ),
                "details": [
                    ("おすすめの飲み方", "コークハイ、またはハイボール"),
                    ("価格帯", "1,800円〜2,200円"),
                    ("原産国", "アメリカ"),
                ],
            },
            {
                "name": "サントリー 白州（ジャパニーズ）",
                "search_key": "サントリー 白州 ウイスキー",
                "description": (
                    "南アルプスの森に抱かれた蒸溜所で生まれた、<strong>「森香る」ジャパニーズウイスキー</strong>。"
                    "爽やかでスモーキーな香りと、ハーブのような清涼感が特徴。"
                    "ハイボールにすると驚くほど軽快で、食事との相性も抜群です。"
                ),
                "details": [
                    ("おすすめの飲み方", "白州ハイボール（レモンスライスを添えて）"),
                    ("価格帯", "5,000円前後（定価）"),
                    ("原産国", "日本"),
                ],
            },
            {
                "name": "ザ・グレンリベット 12年（スコッチ）",
                "search_key": "グレンリベット 12年 シングルモルト",
                "description": (
                    "「シングルモルトのスタンダード」として世界中で愛される一本。"
                    "<strong>洋梨や桃のようなフルーティな香り</strong>と、クリームのようなまろやかさが特徴。"
                    "「スコッチは苦手」という方でも、これなら飲めたという声が多い銘柄です。"
                ),
                "details": [
                    ("おすすめの飲み方", "ストレート、またはトゥワイスアップ"),
                    ("価格帯", "3,500円〜4,500円"),
                    ("原産国", "スコットランド"),
                ],
            },
            {
                "name": "カバラン クラシック（台湾）",
                "search_key": "カバラン クラシック シングルモルト",
                "description": (
                    "台湾で生まれた、世界が注目するシングルモルト。"
                    "<strong>トロピカルフルーツと蜂蜜</strong>が混ざり合った甘くリッチな風味は、"
                    "スコッチとは全く異なる魅力があります。"
                    "「ウイスキーってこんなに多様なの？」と驚く一本です。"
                ),
                "details": [
                    ("おすすめの飲み方", "ストレート"),
                    ("価格帯", "4,000円〜5,500円"),
                    ("原産国", "台湾"),
                ],
            },
        ],
        "summary_title": "まとめ：「飲みやすさ」を基準に選ぼう",
        "summary_body": (
            "初心者のうちは、難しいことを考える必要はありません。"
            "「甘い」「フルーティ」「飲みやすい」という感覚だけを頼りに選べば十分。"
            "この5本がその入口になれば幸いです。"
        ),
    },
    {
        "filename": "article5.html",
        "badge": "Cocktail Guide",
        "category": "飲み方ガイド",
        "title_html": (
            "ハイボールが10倍美味しくなる<br>"
            '<span class="accent">「割って映える」銘柄3選</span>'
        ),
        "lead": [
            "居酒屋でも定番になったハイボール。でも、どのウイスキーで作るかで、その美味しさは天と地ほど変わります。",
            "「なんとなくハイボールを飲んでいる」という人に、ぜひ試してほしい銘柄を3つ紹介します。",
        ],
        "intro": (
            "今回は「ハイボールに使うと特に輝く」ウイスキーを厳選しました。"
            "市販の安いウイスキーで作るのとは、比べ物にならない仕上がりになります。"
        ),
        "whiskies": [
            {
                "name": "サントリー 角瓶（ジャパニーズ）",
                "search_key": "サントリー 角瓶 ウイスキー",
                "description": (
                    "居酒屋ハイボールの代名詞。<strong>甘みと苦味のバランスが絶妙</strong>で、"
                    "炭酸と合わせたときに最も力を発揮するウイスキーと言っても過言ではありません。"
                    "グラスに氷をたっぷり入れてよく冷やし、炭酸を静かに注ぐ「角ハイボール」は、プロの技法です。"
                ),
                "details": [
                    ("おすすめの飲み方", "角ハイボール（ウイスキー1：炭酸4の比率）"),
                    ("価格帯", "1,500円〜1,800円"),
                    ("ポイント", "強炭酸を使うとさらに美味しい"),
                ],
            },
            {
                "name": "ジムビーム ホワイト（バーボン）",
                "search_key": "ジムビーム ホワイト バーボン",
                "description": (
                    "世界ナンバーワン売上のバーボン。"
                    "<strong>バニラとオーク樽の香り</strong>が炭酸と合わさると、甘くスムーズなハイボールになります。"
                    "コスパが非常に高く、「毎日飲む家ハイボール用ウイスキー」として愛用者が多い一本です。"
                ),
                "details": [
                    ("おすすめの飲み方", "ハイボール（レモン果汁を少し絞っても◎）"),
                    ("価格帯", "1,200円〜1,600円"),
                    ("ポイント", "冷凍庫で冷やしてから使うのも人気"),
                ],
            },
            {
                "name": "フォアローゼズ（バーボン）",
                "search_key": "フォアローゼズ バーボン",
                "description": (
                    "バラのラベルが美しい、花のような香りのバーボン。"
                    "<strong>フローラルでフルーティな甘み</strong>が特徴で、"
                    "ハイボールにすると女性にも人気の爽やかな味わいになります。"
                    "「バーボンって甘いんだ」と再発見できる一本です。"
                ),
                "details": [
                    ("おすすめの飲み方", "ハイボール、またはコークハイ"),
                    ("価格帯", "1,800円〜2,500円"),
                    ("ポイント", "グラスのふちにオレンジピールを添えて"),
                ],
            },
        ],
        "summary_title": "まとめ：ウイスキーを変えるだけで世界が変わる",
        "summary_body": (
            "ハイボールは「割るだけ」ではありません。使うウイスキーで表情が全く変わります。"
            "今回の3本を試して、お気に入りの「マイハイボール」を見つけてみてください。"
        ),
    },
    {
        "filename": "article6.html",
        "badge": "Gift Guide",
        "category": "ギフトガイド",
        "title_html": (
            "上司・友人・大切な人へ。<br>"
            '<span class="accent">「もらって必ず喜ばれる」ウイスキーギフト3選</span>'
        ),
        "lead": [
            "誕生日、父の日、クリスマス——大切な人へのプレゼントにウイスキーを選ぶ人が増えています。",
            "でも、どれを選べば喜ばれるのか、迷いますよね。今回は「ウイスキー通を唸らせる」贈り物を3つ厳選しました。",
        ],
        "intro": (
            "価格帯・シーン別に使い分けられる3本を用意しました。"
            "贈る相手が「ウイスキー初心者」でも「熟練のウイスキーラバー」でも、"
            "喜ばれること間違いなしのラインナップです。"
        ),
        "whiskies": [
            {
                "name": "シングルモルト山崎（ジャパニーズ）",
                "search_key": "サントリー 山崎 シングルモルト",
                "description": (
                    "日本が誇る、世界最高峰のウイスキーのひとつ。"
                    "<strong>ミズナラ樽由来の伽羅（きゃら）のような香り</strong>と、"
                    "熟成した果実のような甘さが融合した複雑な味わいは、一度飲んだら忘れられません。"
                    "化粧箱付きで見た目も申し分なく、どんなシーンでも主役になれるギフトです。"
                ),
                "details": [
                    ("おすすめシーン", "父の日、特別な記念日、ビジネスギフト"),
                    ("価格帯", "8,000円〜15,000円（定価）"),
                    ("おすすめの飲み方", "ストレート"),
                ],
            },
            {
                "name": "マッカラン 15年 ファインオーク（スコッチ）",
                "search_key": "マッカラン 15年 ファインオーク",
                "description": (
                    "「シングルモルトのロールスロイス」と呼ばれるマッカランの15年熟成。"
                    "<strong>シェリー樽とバーボン樽の2種類で熟成</strong>され、"
                    "チョコレートとドライフルーツが複雑に絡み合う深みのある味。"
                    "ウイスキー好きへの贈り物として「これを持ってくるとは只者じゃない」と思われること確実です。"
                ),
                "details": [
                    ("おすすめシーン", "ウイスキー通へのプレゼント"),
                    ("価格帯", "12,000円〜18,000円"),
                    ("おすすめの飲み方", "ストレート（加水厳禁）"),
                ],
            },
            {
                "name": "グレンフィディック 18年（スコッチ）",
                "search_key": "グレンフィディック 18年 ウイスキー",
                "description": (
                    "世界で最も売れているシングルモルト、グレンフィディックの18年熟成版。"
                    "<strong>オーク樽のスパイシーさと、洋梨・リンゴのフルーティさ</strong>が見事に調和した、"
                    "「贈り物の定番中の定番」。"
                    "価格と品質のバランスが取れた、贈る側も安心感のある一本です。"
                ),
                "details": [
                    ("おすすめシーン", "父の日、誕生日、ウイスキー入門者へ"),
                    ("価格帯", "8,000円〜12,000円"),
                    ("おすすめの飲み方", "ストレート、またはロック"),
                ],
            },
        ],
        "summary_title": "まとめ：ウイスキーは「物語を贈る」ギフト",
        "summary_body": (
            "ウイスキーには、作られた土地の気候や文化、蒸溜家の哲学が詰まっています。"
            "それを大切な人に贈ることは、単なるプレゼント以上の意味を持ちます。"
            "今回の3本がその「物語の扉」を開くきっかけになれば幸いです。"
        ),
    },
    {
        "filename": "article7.html",
        "badge": "Value Picks",
        "category": "コスパ重視",
        "title_html": (
            '「安くてうまい」は本当にある。<br>'
            '<span class="accent">1万円以下の神コスパウイスキー4選</span>'
        ),
        "lead": [
            "「ウイスキーは高い」——そう思っている人も多いのでは？確かに高い銘柄はありますが、"
            "実は1万円以下でも信じられないほど美味しいウイスキーが存在します。",
            "今回は「コスパ最高」と断言できる4本を厳選して紹介します。",
        ],
        "intro": (
            "ソムリエや蒸溜家が愛用するものも含まれています。"
            "「高いワインより安いウイスキーのほうが美味い」——そう感じる日が来るかもしれません。"
        ),
        "whiskies": [
            {
                "name": "グレンモーレンジィ オリジナル（スコッチ）",
                "search_key": "グレンモーレンジィ オリジナル",
                "description": (
                    "4,000円前後でこの品質は反則的なコスパ。"
                    "<strong>オレンジ・蜂蜜・バニラの三重奏</strong>が口の中で広がり、"
                    "アルコールのピリピリ感がほとんどない。"
                    "「初めて飲むシングルモルトにこれを選んで正解だった」という声が後を絶たない名品です。"
                ),
                "details": [
                    ("価格帯", "4,000円〜5,000円"),
                    ("コスパ評価", "★★★★★"),
                    ("おすすめの飲み方", "ストレート、またはトゥワイスアップ"),
                ],
            },
            {
                "name": "ラフロイグ 10年（スコッチ・アイラ）",
                "search_key": "ラフロイグ 10年 シングルモルト",
                "description": (
                    "「スモーキーなウイスキーの最高峰」と言われながら、5,000円以下で購入できる驚きのコスパ。"
                    "<strong>海藻・ピート・独特のスモークが絡み合うクセのある香り</strong>は好き嫌いが分かれますが、"
                    "一度ハマったら抜け出せないと言われる中毒性があります。"
                    "「個性派ウイスキー」の入門として最適な一本。"
                ),
                "details": [
                    ("価格帯", "4,500円〜5,500円"),
                    ("コスパ評価", "★★★★☆（個性派部門1位）"),
                    ("おすすめの飲み方", "ストレート、または少量の加水"),
                ],
            },
            {
                "name": "デュワーズ 12年（スコッチ）",
                "search_key": "デュワーズ 12年 ウイスキー",
                "description": (
                    "「ダブル熟成（ダブルエイジド）」製法で作られたブレンデッドウイスキー。"
                    "<strong>なめらかな口当たりと、甘くクリーミーな余韻</strong>が特徴で、"
                    "3,500円前後という価格が信じられないほど完成度が高い。"
                    "「コスパ最高のスコッチ」として専門家にも高評価です。"
                ),
                "details": [
                    ("価格帯", "3,000円〜4,000円"),
                    ("コスパ評価", "★★★★★（コスパ部門No.1）"),
                    ("おすすめの飲み方", "ハイボール、またはロック"),
                ],
            },
            {
                "name": "アードモア トラディショナル カスク（スコッチ）",
                "search_key": "アードモア トラディショナル ウイスキー",
                "description": (
                    "ハイランド産の<strong>ライトスモーキー&amp;ハニー系シングルモルト</strong>。"
                    "「ピートが効いているけど重くない」という絶妙なバランスで、"
                    "スモーキー系ウイスキー入門に最適。"
                    "4,000円前後でこの複雑さが楽しめるのは、知る人ぞ知るコスパの秘密です。"
                ),
                "details": [
                    ("価格帯", "3,500円〜5,000円"),
                    ("コスパ評価", "★★★★☆（隠れた名品）"),
                    ("おすすめの飲み方", "ロック、またはハイボール"),
                ],
            },
        ],
        "summary_title": "まとめ：コスパとは「価格以上の感動」があること",
        "summary_body": (
            "今回紹介した4本は、いずれも「値段を忘れて楽しめる」ウイスキーです。"
            "高価なボトルに手が出ない時期でも、こういう銘柄を知っているだけで、"
            "ウイスキーライフがぐっと豊かになります。"
        ),
    },
    {
        "filename": "article8.html",
        "badge": "Ladies' Pick",
        "category": "甘口・フルーティ",
        "title_html": (
            "「甘い、軽い、美しい」<br>"
            '<span class="accent">女性ウイスキー初心者におすすめの3選</span>'
        ),
        "lead": [
            "「ウイスキーって男性の飲み物でしょ？」——それは大きな誤解です。"
            "近年、女性ウイスキー愛好家は急増しており、女性の感性に響く銘柄が世界中で注目されています。",
            "「甘くて飲みやすい」「香りが美しい」「ボトルがおしゃれ」——そんな視点で3本を選びました。",
        ],
        "intro": (
            "ウイスキー初心者の女性でも「これなら飲める！」「もう一杯欲しい」と感じてもらえるような銘柄ばかりです。"
            "プレゼントにも最適です。"
        ),
        "whiskies": [
            {
                "name": "ザ・グレンリベット 12年（スコッチ）",
                "search_key": "グレンリベット 12年 シングルモルト",
                "description": (
                    "洋梨・桃・ジャスミンのような<strong>花と果実の香りが際立つ</strong>シングルモルト。"
                    "アルコールのえぐみが少なく、白ワインが好きな女性に特に喜ばれます。"
                    "「ウイスキーって香水みたいに香るんだ」と驚かれること必至の一本です。"
                ),
                "details": [
                    ("おすすめの飲み方", "ストレート、または少量の加水"),
                    ("価格帯", "3,500円〜4,500円"),
                    ("香りのタイプ", "フローラル・フルーティ"),
                ],
            },
            {
                "name": "アラン 10年（スコッチ・アイランド）",
                "search_key": "アラン 10年 シングルモルト",
                "description": (
                    "スコットランドのアラン島で生まれた、"
                    "<strong>トロピカルフルーツと蜂蜜を思わせる甘さ</strong>が特徴のシングルモルト。"
                    "ピートを使用していないため、「スモーキーが苦手」という方でも安心して楽しめます。"
                    "ラベルのデザインも清潔感があり、女性へのプレゼントに人気です。"
                ),
                "details": [
                    ("おすすめの飲み方", "ロック、またはトゥワイスアップ"),
                    ("価格帯", "4,000円〜5,500円"),
                    ("香りのタイプ", "トロピカル・ハニー"),
                ],
            },
            {
                "name": "メーカーズマーク（バーボン）",
                "search_key": "メーカーズマーク バーボン",
                "description": (
                    "赤い封蝋が印象的な、<strong>バニラとキャラメルの甘さが前面に出た</strong>バーボンウイスキー。"
                    "通常のバーボンより辛みが少ない「冬小麦製法」で作られており、スイーツ感覚で楽しめます。"
                    "「ウイスキーを飲んでいるのにデザートみたい」と言われるほどの甘さです。"
                ),
                "details": [
                    ("おすすめの飲み方", "ロック（氷が溶けるほど甘くなる）"),
                    ("価格帯", "2,500円〜3,000円"),
                    ("香りのタイプ", "バニラ・キャラメル"),
                ],
            },
        ],
        "summary_title": "まとめ：ウイスキーに「性別」は関係ない",
        "summary_body": (
            "世界の一流バーでは、女性のウイスキーラバーが増え続けています。"
            "「甘さ」「軽さ」「香りの美しさ」——そんな基準で選んだウイスキーを、ぜひ試してみてください。"
            "新しい世界の扉が開くはずです。"
        ),
    },
]

# ─── CSS (shared luxury template) ────────────────────────────────────────────

CSS = """\
        /* ── Reset ── */
        *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

        /* ── Design Tokens ── */
        :root {
            --gold:        #c9a84c;
            --gold-light:  #e8cc7e;
            --gold-dim:    #8b6014;
            --bg-root:     #070604;
            --bg-deep:     #0f0d09;
            --bg-card:     #1a1712;
            --bg-inset:    #221f19;
            --text-bright: #f0e8d8;
            --text-main:   #d8ccb8;
            --text-sub:    #a09070;
            --text-muted:  #6a5e4a;
            --border:      #2c2820;
            --border-gold: #3a3020;
        }

        html { scroll-behavior: smooth; }

        body {
            font-family: 'Noto Serif JP', Georgia, 'Times New Roman', serif;
            background-color: var(--bg-root);
            color: var(--text-main);
            line-height: 1.95;
            font-size: 16px;
            font-weight: 300;
        }

        /* ── Header ── */
        header {
            background: linear-gradient(180deg, #0b0906 0%, #0f0d09 100%);
            border-bottom: 1px solid var(--border-gold);
            padding: 32px 20px 28px;
            text-align: center;
        }
        .header-rule {
            display: flex; align-items: center; justify-content: center;
            gap: 14px; margin-bottom: 18px;
        }
        .header-rule::before, .header-rule::after {
            content: ''; display: block; width: 48px; height: 1px;
            background: linear-gradient(90deg, transparent, var(--gold-dim));
        }
        .header-rule::after { background: linear-gradient(90deg, var(--gold-dim), transparent); }
        .header-diamond { color: var(--gold); font-size: 8px; letter-spacing: 6px; }
        .site-title {
            display: block; font-family: 'Playfair Display', Georgia, serif;
            color: var(--gold); font-size: clamp(18px, 3.8vw, 26px);
            letter-spacing: 0.22em; font-weight: 400; text-decoration: none;
            transition: color 0.2s;
        }
        .site-title:hover { color: var(--gold-light); }
        .site-tagline {
            font-size: 10px; color: var(--text-muted); letter-spacing: 0.28em;
            text-transform: uppercase; margin-top: 8px;
            font-family: 'Playfair Display', serif; font-style: italic;
        }
        .header-rule-bottom {
            display: flex; align-items: center; justify-content: center;
            gap: 14px; margin-top: 18px;
        }
        .header-rule-bottom::before, .header-rule-bottom::after {
            content: ''; display: block; width: 48px; height: 1px;
            background: linear-gradient(90deg, transparent, var(--border-gold));
        }
        .header-rule-bottom::after { background: linear-gradient(90deg, var(--border-gold), transparent); }
        .header-rule-bottom span { color: var(--text-muted); font-size: 7px; letter-spacing: 5px; }

        /* ── Nav ── */
        nav { background: var(--bg-deep); border-bottom: 1px solid var(--border); }
        nav ul { list-style: none; display: flex; justify-content: center; flex-wrap: wrap; }
        nav a {
            display: block; color: var(--text-sub); text-decoration: none;
            font-size: 11px; letter-spacing: 0.18em; text-transform: uppercase;
            padding: 14px 22px; border-bottom: 2px solid transparent;
            transition: color 0.2s, border-color 0.2s;
        }
        nav a:hover { color: var(--gold); border-bottom-color: var(--gold-dim); }

        /* ── Main Layout ── */
        .container { max-width: 760px; margin: 0 auto; padding: 52px 20px 88px; }

        /* ── Article Header ── */
        .article-label { display: flex; align-items: center; gap: 14px; margin-bottom: 22px; }
        .badge {
            font-family: 'Playfair Display', serif; font-style: italic;
            font-size: 10px; letter-spacing: 0.18em; color: var(--gold);
            border: 1px solid var(--border-gold); padding: 5px 14px;
        }
        .article-category { font-size: 11px; letter-spacing: 0.15em; color: var(--text-muted); text-transform: uppercase; }
        .article-title {
            font-family: 'Playfair Display', Georgia, serif;
            font-size: clamp(22px, 4.2vw, 32px); font-weight: 700;
            line-height: 1.5; color: var(--text-bright); margin-bottom: 8px;
        }
        .article-title .accent { color: var(--gold); }

        /* ── Lead ── */
        .lead {
            font-size: 15px; color: var(--text-sub);
            border-left: 2px solid var(--gold-dim);
            padding: 14px 18px; margin: 28px 0;
            background: var(--bg-inset); line-height: 1.9;
        }
        .lead p + p { margin-top: 10px; }

        /* ── Ornamental Divider ── */
        .ornament {
            display: flex; align-items: center; gap: 14px;
            margin: 44px 0; color: var(--text-muted);
        }
        .ornament::before, .ornament::after {
            content: ''; flex: 1; height: 1px;
            background: linear-gradient(90deg, transparent, var(--border-gold), transparent);
        }
        .ornament-inner { font-size: 10px; letter-spacing: 8px; padding: 0 4px; }

        /* ── Whiskey Card ── */
        .whiskey-card {
            background: var(--bg-card); border: 1px solid var(--border);
            border-top: 2px solid var(--gold-dim); padding: 36px 38px 32px; position: relative;
        }
        .card-number {
            position: absolute; top: -1px; right: 28px;
            font-family: 'Playfair Display', serif; font-style: italic;
            font-size: 11px; letter-spacing: 0.12em;
            color: var(--bg-card); background: var(--gold-dim); padding: 4px 14px 5px;
        }

        /* ── Section Heading ── */
        .section-heading {
            font-family: 'Playfair Display', Georgia, serif;
            font-size: clamp(17px, 3vw, 22px); font-weight: 600;
            color: var(--text-bright); padding-bottom: 14px;
            margin-bottom: 20px; position: relative;
        }
        .section-heading::after {
            content: ''; position: absolute; bottom: 0; left: 0;
            width: 100%; height: 1px;
            background: linear-gradient(90deg, var(--gold-dim) 0%, var(--gold-dim) 50px, var(--border) 50px);
        }

        /* ── Body Text ── */
        .whiskey-card p, .summary-box p { margin-bottom: 16px; color: var(--text-main); }
        .whiskey-card p:last-of-type { margin-bottom: 0; }
        strong { color: var(--gold-light); font-weight: 600; }

        /* ── Detail List ── */
        .detail-list {
            list-style: none; margin: 22px 0 26px;
            background: var(--bg-inset); padding: 0;
            border-left: 3px solid var(--gold-dim);
        }
        .detail-list li {
            font-size: 14px; color: var(--text-sub);
            padding: 11px 20px; display: flex; gap: 10px;
        }
        .detail-list li + li { border-top: 1px solid var(--border); }
        .detail-list li::before { content: '—'; color: var(--gold-dim); flex-shrink: 0; }

        /* ── Amazon Affiliate Button ── */
        .affiliate-box { margin-top: 28px; text-align: center; }
        .btn-amazon {
            display: inline-flex; align-items: center; justify-content: center;
            gap: 10px;
            background: linear-gradient(135deg, #c9a84c 0%, #a87e2e 100%);
            color: #080600; text-decoration: none;
            font-family: 'Noto Serif JP', serif; font-weight: 600;
            font-size: 13px; letter-spacing: 0.1em; padding: 15px 36px;
            border-radius: 1px;
            transition: filter 0.2s, transform 0.15s, box-shadow 0.2s;
            box-shadow: 0 2px 12px rgba(201,168,76,0.18), inset 0 1px 0 rgba(255,255,255,0.18);
            min-width: 260px;
        }
        .btn-amazon:hover {
            filter: brightness(1.1); transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(201,168,76,0.28), inset 0 1px 0 rgba(255,255,255,0.18);
        }
        .btn-amazon .btn-icon { font-size: 15px; opacity: 0.9; }
        .btn-amazon .btn-sub {
            font-size: 10px; letter-spacing: 0.06em;
            display: block; opacity: 0.75; font-weight: 400;
        }
        .btn-amazon-inner { text-align: left; }

        /* ── Summary Box ── */
        .summary-box {
            background: var(--bg-card); border: 1px solid var(--border);
            border-top: 2px solid var(--gold); padding: 38px 38px 34px; margin-top: 8px;
        }
        .cta-block {
            margin-top: 30px; padding-top: 26px;
            border-top: 1px solid var(--border); text-align: center;
        }
        .cta-lead { font-size: 14px; color: var(--text-sub); margin-bottom: 18px; line-height: 1.8; }
        .btn-cta {
            display: inline-block; background: transparent; color: var(--gold);
            text-decoration: none; font-family: 'Playfair Display', serif;
            font-size: 14px; letter-spacing: 0.1em; padding: 16px 36px;
            border: 1px solid var(--gold-dim);
            transition: background 0.25s, color 0.25s, border-color 0.25s; min-width: 300px;
        }
        .btn-cta:hover { background: var(--gold-dim); color: var(--text-bright); border-color: var(--gold-dim); }

        /* ── Footer ── */
        footer { text-align: center; padding: 44px 20px; border-top: 1px solid var(--border); }
        .footer-rule {
            display: flex; align-items: center; justify-content: center;
            gap: 12px; margin-bottom: 20px;
        }
        .footer-rule::before, .footer-rule::after {
            content: ''; display: block; width: 36px; height: 1px; background: var(--border-gold);
        }
        .footer-rule span { color: var(--text-muted); font-size: 8px; letter-spacing: 4px; }
        footer p { font-size: 11px; color: var(--text-muted); letter-spacing: 0.12em; }

        /* ── Responsive ── */
        @media (max-width: 600px) {
            .container { padding: 36px 16px 64px; }
            .whiskey-card { padding: 28px 20px 24px; }
            .summary-box { padding: 28px 20px 24px; }
            .btn-amazon { min-width: 0; width: 100%; }
            .btn-cta { min-width: 0; width: 100%; }
            .card-number { right: 16px; }
        }
"""

# ─── HTML Builder ─────────────────────────────────────────────────────────────

def build_detail_items(details):
    return "\n".join(
        f'                    <li><span><strong>{label}:</strong>&ensp;{value}</span></li>'
        for label, value in details
    )


def build_whiskey_cards(whiskies):
    parts = []
    for i, w in enumerate(whiskies, 1):
        url = amazon_search_url(w["search_key"])
        detail_items = build_detail_items(w["details"])
        parts.append(f"""\
            <div class="whiskey-card">
                <span class="card-number">No. {i}</span>
                <h2 class="section-heading">{w['name']}</h2>
                <p>{w['description']}</p>
                <ul class="detail-list">
{detail_items}
                </ul>
                <div class="affiliate-box">
                    <a href="{url}" class="btn-amazon" target="_blank" rel="noopener noreferrer sponsored">
                        <span class="btn-icon">&#x1F6D2;</span>
                        <span class="btn-amazon-inner">
                            Amazon&#x3067;&#x4FA1;&#x683C;&#x3092;&#x30C1;&#x30A7;&#x30C3;&#x30AF;
                            <span class="btn-sub">{w['search_key']}</span>
                        </span>
                    </a>
                </div>
            </div>

            <div class="ornament"><span class="ornament-inner">&#x2726; &#x2726; &#x2726;</span></div>""")
    return "\n\n".join(parts)


def build_lead(lead_paragraphs):
    return "\n".join(f"                <p>{p}</p>" for p in lead_paragraphs)


def build_html(article):
    page_title = strip_tags(article["title_html"])
    card_html = build_whiskey_cards(article["whiskies"])
    lead_html = build_lead(article["lead"])

    return f"""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{page_title} | Gentleman's Whiskey Guide</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;0,700;1,400&family=Noto+Serif+JP:wght@300;400;600&display=swap" rel="stylesheet">
    <style>
{CSS}
    </style>
</head>
<body>

    <header>
        <div class="header-rule">
            <span class="header-diamond">&#x25C6; &#x25C6; &#x25C6;</span>
        </div>
        <a href="index.html" class="site-title">Gentleman&#x2019;s Whiskey Guide</a>
        <p class="site-tagline">For the Discerning Palate</p>
        <div class="header-rule-bottom">
            <span>&#x25C6; &#x25C6; &#x25C6;</span>
        </div>
    </header>

    <nav>
        <ul>
            <li><a href="index.html">Home</a></li>
            <li><a href="product.html">&#x96FB;&#x5B50;&#x66F8;&#x7C4D;&#xFF08;&#x5546;&#x54C1;&#xFF09;</a></li>
        </ul>
    </nav>

    <div class="container">
        <article>

            <div class="article-label">
                <span class="badge">{article['badge']}</span>
                <span class="article-category">{article['category']}</span>
            </div>

            <h1 class="article-title">
                {article['title_html']}
            </h1>

            <div class="lead">
{lead_html}
            </div>

            <p>{article['intro']}</p>

            <div class="ornament"><span class="ornament-inner">&#x2726; &#x2726; &#x2726;</span></div>

{card_html}

            <!-- &#x307E;&#x3068;&#x3081; -->
            <div class="summary-box">
                <h2 class="section-heading">{article['summary_title']}</h2>
                <p>{article['summary_body']}</p>
                <div class="cta-block">
                    <p class="cta-lead"><strong>&#x3055;&#x3089;&#x306B;&#x8A73;&#x3057;&#x3044;&#x300C;&#x5927;&#x4EBA;&#x306E;&#x98F2;&#x307F;&#x65B9;&#x300D;&#x3084;&#x300C;Bar&#x3067;&#x306E;&#x632F;&#x308B;&#x821E;&#x3044;&#x300D;&#x3092;&#x77E5;&#x308A;&#x305F;&#x3044;&#x65B9;&#x306F;&#x3001;<br>&#x3053;&#x3061;&#x3089;&#x306E;&#x30AC;&#x30A4;&#x30C9;&#x3082;&#x304A;&#x3059;&#x3059;&#x3081;&#x3067;&#x3059;&#x3002;</strong></p>
                    <a href="./product.html" class="btn-cta">&#x5927;&#x4EBA;&#x306E;&#x30A6;&#x30A4;&#x30B9;&#x30AD;&#x30FC;&#x5165;&#x9580;&#x66F8;&#xFF08;&#x516C;&#x5F0F;&#x30AC;&#x30A4;&#x30C9;&#xFF09;&#x3092;&#x898B;&#x308B; &nbsp;&#x203A;</a>
                </div>
            </div>

        </article>
    </div>

    <footer>
        <div class="footer-rule"><span>&#x25C6;</span></div>
        <p>&copy; 2026 Gentleman&#x2019;s Whiskey Guide. All rights reserved.</p>
    </footer>

</body>
</html>
"""


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    PUBLIC_DIR.mkdir(exist_ok=True)
    generated = []

    for article in ARTICLES:
        html = build_html(article)
        out_path = PUBLIC_DIR / article["filename"]
        out_path.write_text(html, encoding="utf-8")
        print(f"[OK] {out_path.name}")
        generated.append(out_path.name)

    print(f"\n{len(generated)} articles generated: {', '.join(generated)}")

    # ─── Git push ──────────────────────────────────────────────────────────────
    print("\n--- Git ---")
    subprocess.run(["git", "add", "public/"], cwd=PROJECT_ROOT, check=True)
    result = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=PROJECT_ROOT, capture_output=True, text=True
    )
    if not result.stdout.strip():
        print("Nothing to commit (files already up to date).")
        return
    subprocess.run(
        ["git", "commit", "-m", "Add 5 whiskey articles with Amazon affiliate links"],
        cwd=PROJECT_ROOT, check=True,
    )
    subprocess.run(["git", "push"], cwd=PROJECT_ROOT, check=True)
    print("\nDone! All articles pushed to GitHub.")


if __name__ == "__main__":
    main()
