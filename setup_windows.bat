@echo off
setlocal enabledelayedexpansion

REM Windows 环境安装脚本
REM 用于安装 Bing 奖励脚本的所有依赖

echo ============================================
echo 正在为 Windows 设置 Bing 奖励脚本环境...
echo ============================================

REM 检查 Python 是否已安装
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未找到 Python，请先安装 Python 3.8+
    echo 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
) else (
    echo Python 已安装
    python --version
)

REM 创建虚拟环境
echo 创建 Python 虚拟环境...
if not exist "venv" (
    python -m venv venv
    echo 虚拟环境创建完成
) else (
    echo 虚拟环境已存在
)

REM 激活虚拟环境并安装依赖
echo 安装 Python 依赖...
call venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt

REM 创建用户数据目录
echo 创建用户配置目录...
if not exist "chrome_profiles\user1" mkdir "chrome_profiles\user1"
if not exist "chrome_profiles\user2" mkdir "chrome_profiles\user2"
if not exist "chrome_profiles\user3" mkdir "chrome_profiles\user3"
if not exist "chrome_profiles\user4" mkdir "chrome_profiles\user4"

echo.
echo ============================================
echo 安装完成！
echo ============================================
echo.
echo 使用方法：
echo 1. 双击运行: start_bing_reward.bat
echo.
echo 注意：
echo - 请确保已安装 Google Chrome 浏览器
echo - 首次运行会自动下载 ChromeDriver
echo - 脚本会运行2个实例，最大并行数为2
echo - 多实例运行会消耗更多系统资源
echo.
pause 