# 🌐 Webサイトを全世界に公開する手順（GitHub Pages編）

完成したウイスキーブログを、無料で公開する手順書です。
**「GitHub Pages」** を使うのが最も安定的で、プロっぽく見えます。

---

## 手順A：GitHub Pagesで公開する（推奨）

GitHubのアカウントをお持ちの場合、これが一番おすすめです。

1.  **GitHubに新しいリポジトリを作る**
    *   リポジトリ名は `whiskey-blog` など、適当でOKです。
    *   「Public」を選んで作成してください。

2.  **ファイルをアップロードする**
    *   このフォルダの中身をすべてアップロードします：
    *   `c:\Users\since\新しいフォルダー\trend_arbitrage_project\whiskey_blog`
    *   （特に `docs` フォルダが重要です）

3.  **公開設定をする**
    *   リポジトリの **[Settings]** タブを開く。
    *   左メニューの **[Pages]** をクリック。
    *   **Build and deployment** の **Source** で「Deploy from a branch」を選択。
    *   **Branch** のところを「main」にし、フォルダを **「/docs」** に変更して Save ボタンを押す。

4.  **完了！**
    *   数分待つと、画面上に「Your site is live at...」とURLが表示されます。
    *   それがあなたのサイトのURLです。

---

## 手順B：Netlify Drop（もっと簡単な方法）

GitHubが難しい場合は、こちらを使ってください。登録不要です。

1.  ブラウザで [https://app.netlify.com/drop](https://app.netlify.com/drop) を開く。
2.  `trend_arbitrage_project/whiskey_blog/docs` フォルダを、画面にドラッグ＆ドロップする。
3.  これだけで即公開されます。

---

**💰 収益化の準備**
サイトが公開できたら、AmazonアソシエイトにそのURLを申請しましょう。
審査に通ったら、記事内のリンクを書き換えて、再度とアップロード（更新）してください。
