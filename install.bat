@echo off
echo 正在安装pvfUtility MCP服务器依赖...

REM 检查uv是否安装
uv --version >nul 2>&1
if %errorlevel% neq 0 (
    echo 警告: 未找到uv，尝试使用pip安装...
    
    REM 检查Python是否安装
    python --version >nul 2>&1
    if %errorlevel% neq 0 (
        echo 错误: 未找到Python，请先安装Python 3.8+
        pause
        exit /b 1
    )
    
    REM 使用pip安装依赖
    echo 使用pip安装Python依赖包...
    pip install -r requirements.txt
    
    if %errorlevel% equ 0 (
        echo.
        echo 使用pip安装完成！
    ) else (
        echo pip安装失败，请检查网络连接和Python环境
        pause
        exit /b 1
    )
) else (
    echo 使用uv安装依赖包...
    uv sync
    
    if %errorlevel% equ 0 (
        echo.
        echo 使用uv安装完成！
    ) else (
        echo uv安装失败，尝试使用pip...
        pip install -r requirements.txt
        
        if %errorlevel% equ 0 (
            echo 使用pip安装完成！
        ) else (
            echo 安装失败，请检查网络连接
            pause
            exit /b 1
        )
    )
)

echo.
echo 安装完成！
echo.
echo 使用说明:
echo 1. 确保pvfUtility软件已启动并开启WebApi服务（默认端口27000）
echo 2. 您的MCP配置已设置为使用uv运行
echo 3. 配置路径: C:\Users\sen\AppData\Roaming\Trae\User\mcp.json
echo 4. 重启您的MCP客户端即可使用
echo.
echo 测试命令:
echo    uv run test_mcp_server.py
echo.

pause