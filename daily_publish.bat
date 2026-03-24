@echo off
:: ============================================================
:: daily_publish.bat
:: ウイスキーブログ 毎日自動記事生成 & GitHub push
:: Windowsタスクスケジューラーに登録して毎日実行する
:: ============================================================

cd /d "C:\Users\since\新しいフォルダー\trend_arbitrage_project\whiskey_blog"

:: ログディレクトリを作成
if not exist "logs" mkdir logs

:: 実行日時をログに記録
echo. >> logs\daily_article.log
echo ===================================== >> logs\daily_article.log
echo [%DATE% %TIME%] daily_publish.bat 開始 >> logs\daily_article.log
echo ===================================== >> logs\daily_article.log

:: daily_article.py を実行（stdout/stderr をログファイルに追記）
python daily_article.py >> logs\daily_article.log 2>&1

:: 終了コードを確認
if %ERRORLEVEL% == 0 (
    echo [%DATE% %TIME%] 正常終了 >> logs\daily_article.log
) else (
    echo [%DATE% %TIME%] エラー終了 (code=%ERRORLEVEL%) >> logs\daily_article.log
)

exit /b %ERRORLEVEL%
