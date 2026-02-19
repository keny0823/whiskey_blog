@echo off
chcp 65001 > nul
echo ========================================================
echo  【重要】GitHubへのアップロード（更新）処理
echo ========================================================
echo.

:: Change directory safely
cd /d "c:\Users\since\新しいフォルダー\trend_arbitrage_project\whiskey_blog"

:: Check if git is initialized
if not exist .git (
    echo [INFO] Gitリポジトリを初期化しています...
    git init
    git branch -M main
)

:: Configure local git identity (Dummy identity for this repo only)
git config user.email "whiskey_bot@example.com"
git config user.name "Whiskey Bot"

:: Add all files
echo [INFO] 変更ファイルを準備しています...
git add .

:: Commit
echo [INFO] 変更を記録（コミット）しています...
git commit -m "Update content and affiliate links"

:: Add Remote (if not exists)
git remote get-url origin > nul 2>&1
if %errorlevel% neq 0 (
    echo [INFO] 送信先のリポジトリを設定しています...
    git remote add origin https://github.com/keny0823/whiskey_blog.git
)

echo.
echo ========================================================
echo  🚀 いよいよGitHubへ送信します！
echo ========================================================
echo.
echo  この後、ブラウザで「GitHubのログイン画面」が表示される場合があります。
echo  その場合は、あなたのGitHubアカウントでログインし、
echo  「Authorize（許可）」ボタンを押してください。
echo.
echo  ※すでにログイン済みの場合は、そのまま完了します。
echo.
pause

:: Push
echo [INFO] アップロード中...
git push -u origin main

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] アップロードに失敗しました！
    echo 以下の原因が考えられます：
    echo 1. インターネットに繋がっていない
    echo 2. GitHubへのログインに失敗した
    echo 3. リポジトリURL（keny0823/whiskey_blog）が存在しない、または権限がない
    echo.
) else (
    echo.
    echo [SUCCESS] アップロード完了です！🎉
    echo 数分後にWebサイト（https://keny0823.github.io/whiskey_blog/）が更新されます。
)

echo.
pause
