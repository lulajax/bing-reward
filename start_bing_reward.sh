#!/bin/bash

# Bing 奖励脚本启动器
# 自动激活虚拟环境并运行脚本

set -e  # 遇到错误时停止执行

echo "============================================"
echo "启动 Bing 奖励脚本"
echo "============================================"

# 检查虚拟环境是否存在
if [ ! -d "venv" ]; then
    echo "错误: 虚拟环境不存在。请先运行 ./setup_ubuntu.sh 安装依赖"
    exit 1
fi

# 创建用户数据目录（如果不存在）
echo "创建用户配置目录..."
mkdir -p /app/bing-reward/chrome_profiles/user1
mkdir -p /app/bing-reward/chrome_profiles/user2
mkdir -p /app/bing-reward/chrome_profiles/user3

# 激活虚拟环境
echo "激活虚拟环境..."
source venv/bin/activate

# 运行脚本
echo "启动 Bing 奖励脚本 (3个实例，最大并行数3)..."
python app/bing_reward_parallel.py 3 /app/bing-reward/chrome_profiles/user1 /app/bing-reward/chrome_profiles/user2 /app/bing-reward/chrome_profiles/user3 --max_parallel 3

echo "脚本运行完成" 