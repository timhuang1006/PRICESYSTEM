@echo off
setlocal

set GIT="C:\Program Files\Git\bin\git.exe"

echo [1/6] 初始化 Git 倉庫...
%GIT% init

echo [2/6] 設定使用者資訊...
%GIT% config user.name "Quote App Administrator"
%GIT% config user.email "rsps90432@gmail.com"

echo [3/6] 添加所有檔案...
%GIT% add .

echo [4/6] 提交到本地倉庫...
%GIT% commit -m "Add data persistence with GCS volume mount"

echo.
echo =========================================
echo Git 倉庫初始化完成！
echo =========================================
echo.
echo 接下來需要設定遠端倉庫。請選擇：
echo.
echo 1. GitHub: 請先在 https://github.com/new 建立新倉庫
echo    然後執行: setup_git_remote_github.bat
echo.
echo 2. Google Cloud: 暫時無法使用（權限不足）
echo.
pause
