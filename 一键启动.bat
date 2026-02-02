@echo off
setlocal

REM 配置参数
set "VENV_DIR=venv"
set "REQUIREMENTS=requirements.txt"
set "APP_ENTRY=app.py"

REM 检查虚拟环境
if not exist "%VENV_DIR%\Scripts\python.exe" (
    echo 正在创建虚拟环境...
    python -m venv "%VENV_DIR%"
    if errorlevel 1 (
        echo 虚拟环境创建失败，请检查Python安装
        pause
        exit
    )
)

REM 激活虚拟环境
call "%VENV_DIR%\Scripts\activate.bat"
if errorlevel 1 (
    echo 虚拟环境激活失败
    pause
    exit
)

REM 安装依赖
if exist "%REQUIREMENTS%" (
    echo 正在安装依赖...
    pip install -r "%REQUIREMENTS%"
    if errorlevel 1 (
        echo 依赖安装失败
        pause
        exit
    )
) else (
    echo 未找到requirements.txt文件
    pause
    exit
)

REM 启动应用
echo 启动应用中...
python "%APP_ENTRY%"
pause