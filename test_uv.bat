@echo off
echo 使用uv运行pvfUtility MCP服务器测试...
echo.

REM 检查uv是否安装
uv --version >nul 2>&1
if %errorlevel% neq 0 (
    echo 未找到uv，请先安装uv或使用: python test_mcp_server.py
    pause
    exit /b 1
)

echo 测试前请确保:
echo 1. pvfUtility软件已启动
echo 2. WebApi服务已开启（默认端口27000）
echo.

echo 开始测试...
uv run test_mcp_server.py

if %errorlevel% equ 0 (
    echo.
    echo 测试完成！MCP服务器工作正常
) else (
    echo.
    echo 测试失败，请检查:
    echo 1. pvfUtility软件是否正在运行
    echo 2. WebApi端口是否为27000
    echo 3. 防火墙设置
)

echo.
pause