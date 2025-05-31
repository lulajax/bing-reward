#!/bin/bash

# Ubuntu 22 环境安装脚本
# 用于安装 Bing 奖励脚本的所有依赖

set -e  # 遇到错误时停止执行

echo "============================================"
echo "正在为 Ubuntu 设置 Bing 奖励脚本环境..."
echo "============================================"

# 更新系统包
echo "更新系统包..."
sudo apt update

# 安装 Python3 和 pip（如果未安装）
echo "安装 Python3 和相关工具..."
sudo apt install -y python3 python3-pip python3-venv

# 安装系统依赖
echo "安装系统依赖..."
sudo apt install -y wget curl unzip

# 安装 Google Chrome
echo "安装 Google Chrome..."
if ! command -v google-chrome &> /dev/null; then
    # 添加 Google Chrome 的官方 GPG 密钥
    wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
    
    # 添加 Google Chrome 仓库
    echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" | sudo tee /etc/apt/sources.list.d/google-chrome.list
    
    # 更新包列表并安装 Chrome
    sudo apt update
    sudo apt install -y google-chrome-stable
    
    echo "Google Chrome 安装完成"
else
    echo "Google Chrome 已安装"
fi

# 创建虚拟环境
echo "创建 Python 虚拟环境..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "虚拟环境创建完成"
else
    echo "虚拟环境已存在"
fi

# 激活虚拟环境并安装 Python 依赖
echo "安装 Python 依赖..."
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# 创建用户数据目录
echo "创建用户配置目录..."
mkdir -p /app/bing-reward/chrome_profiles/user1
mkdir -p /app/bing-reward/chrome_profiles/user2
mkdir -p /app/bing-reward/chrome_profiles/user3
mkdir -p /app/bing-reward/chrome_profiles/user4

# 安装 ChromeDriver
echo "安装 ChromeDriver..."
if ! command -v chromedriver &> /dev/null && ! [ -f "/usr/local/bin/chromedriver" ]; then
    echo "正在运行 ChromeDriver 安装脚本..."
    chmod +x install_chromedriver.sh
    ./install_chromedriver.sh || {
        echo "警告: ChromeDriver 安装失败，运行时将尝试自动下载"
        echo "如果运行时出现网络问题，请手动运行: ./install_chromedriver.sh"
    }
else
    echo "ChromeDriver 已安装"
fi

# 设置脚本权限
echo "设置脚本权限..."
chmod +x start_bing_reward.sh 2>/dev/null || echo "警告: start_bing_reward.sh 不存在"
chmod +x fix_pip_timeout.sh 2>/dev/null || echo "警告: fix_pip_timeout.sh 不存在"
chmod +x install_chromedriver.sh 2>/dev/null || echo "警告: install_chromedriver.sh 不存在"

echo ""
echo "============================================"
echo "安装完成！"
echo "============================================"
echo ""
echo "使用方法："
echo "1. 桌面环境（有GUI）："
echo "   ./start_bing_reward.sh"
echo ""
echo "注意："
echo "- 脚本会运行2个实例，最大并行数为2"
echo "- 多实例运行会消耗更多系统资源"
echo "- 用户配置目录: /app/bing-reward/chrome_profiles/"
echo ""
echo "如果遇到问题："
echo "- 网络超时: ./fix_pip_timeout.sh"
echo "- ChromeDriver问题: ./install_chromedriver.sh"
echo ""