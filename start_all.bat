@echo off
REM 启动 Flask 后端
start "" python server.py

REM 切换到前端目录
cd blivedm\webapp

REM 启动 Vue 前端开发服务器
start "" npm run serve

REM 返回根目录
cd ..\..\..

echo 前后端已启动
pause
