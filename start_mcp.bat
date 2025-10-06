@echo off
echo 启动pvfUtility MCP服务器...
echo.

REM 检查uv是否安装
uv --version >nul 2>&1
if %errorlevel% neq 0 (
    echo 未找到uv，请先安装uv
    echo 下载地址: https://github.com/astral-sh/uv
    pause
    exit /b 1
)

echo 检查依赖...
if not exist ".venv" (
    echo 首次运行，正在安装依赖...
    uv sync
    if %errorlevel% neq 0 (
        echo 依赖安装失败
        pause
        exit /b 1
    )
)

echo.
echo 启动MCP服务器...
echo 基础URL: http://localhost:27000
echo.
echo 注意: 请确保pvfUtility软件已启动并开启WebApi服务
echo.

uv run mcp_server.py --base-url http://localhost:27000

pause