@echo off
setlocal enabledelayedexpansion

REM Bing 奖励脚本启动器 (Windows)
REM 自动激活虚拟环境并运行脚本

echo ============================================
echo 启动 Bing 奖励脚本 (Windows)
echo ============================================

REM 检查虚拟环境是否存在
if not exist "venv" (
    echo 错误: 虚拟环境不存在。请先运行安装脚本
    pause
    exit /b 1
)

REM 创建用户数据目录（如果不存在）
echo 创建用户配置目录...
if not exist "chrome_profiles\user1" mkdir "chrome_profiles\user1"
if not exist "chrome_profiles\user2" mkdir "chrome_profiles\user2"

REM 激活虚拟环境
echo 激活虚拟环境...
call venv\Scripts\activate.bat

REM 运行脚本
echo 启动 Bing 奖励脚本 (2个实例，最大并行数2)...
python app\bing_reward_parallel.py 2 "%CD%\chrome_profiles\user1" "%CD%\chrome_profiles\user2" --max_parallel 2

echo 脚本运行完成
pause 