@echo off
chcp 65001 > nul
echo ========================================================
echo  【重要】GitHubへの強制アップロード
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
git commit -m "Force update site content"

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
echo  ※エラーが出る場合は、この画面を閉じて再度実行してみてください。
echo.
pause

:: Force Push to overwrite remote changes
echo [INFO] アップロード中...
git push -f -u origin main

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] アップロードに失敗しました！
    echo GitHubにログインできなかったか、通信エラーの可能性があります。
    echo.
) else (
    echo.
    echo [SUCCESS] アップロード完了です！🎉
    echo.
    echo  https://keny0823.github.io/whiskey_blog/
    echo  ↑
    echo  このURLにアクセスして、更新されたか確認してください。
    echo  （反映まで数分かかることがあります）
    echo.
)

pause
