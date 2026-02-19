@echo off
chcp 65001 > nul
echo ========================================================
echo  Deploying Whiskey Blog to GitHub Pages...
echo ========================================================

:: Change directory safely
cd /d "c:\Users\since\新しいフォルダー\trend_arbitrage_project\whiskey_blog"

:: Check if git is initialized
if not exist .git (
    echo [INFO] Initializing Git repository...
    git init
    git branch -M main
)

:: Configure local git identity to prevent commit errors
git config user.email "whiskey_bot@example.com"
git config user.name "Whiskey Bot"

:: Add all files
echo [INFO] Adding files...
git add .

:: Commit
echo [INFO] Committing changes...
git commit -m "Update affiliate links and content"

:: Add Remote (if not exists)
git remote get-url origin > nul 2>&1
if %errorlevel% neq 0 (
    echo [INFO] Setting up remote repository...
    git remote add origin https://github.com/keny0823/whiskey_blog.git
)

:: Push
echo [INFO] Pushing to GitHub...
git push -u origin main

echo.
echo ========================================================
echo  Deployment Process Finished
echo ========================================================
echo.
echo If you see an error above, please fix it manually in this window.
echo.
cmd /k
