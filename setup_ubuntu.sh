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