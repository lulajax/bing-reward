#!/bin/bash

# 修复 pip 安装超时问题的脚本

echo "============================================"
echo "修复 pip 安装超时问题..."
echo "============================================"

# 激活虚拟环境
if [ -d "venv" ]; then
    source venv/bin/activate
    echo "虚拟环境已激活"
else
    echo "错误: 虚拟环境不存在"
    exit 1
fi

# 清理 pip 缓存
echo "清理 pip 缓存..."
pip cache purge

# 使用国内镜像源安装依赖
echo "使用清华大学镜像源安装依赖..."

install_with_mirror() {
    local package=$1
    echo "安装 $package..."
    
    # 尝试多个镜像源
    mirrors=(
        "https://pypi.tuna.tsinghua.edu.cn/simple/"
        "https://mirrors.aliyun.com/pypi/simple/"
        "https://pypi.douban.com/simple/"
    )
    
    for mirror in "${mirrors[@]}"; do
        echo "尝试镜像: $mirror"
        if pip install "$package" -i "$mirror" --timeout 30 --retries 2 --trusted-host $(echo $mirror | cut -d'/' -f3); then
            echo "$package 安装成功"
            return 0
        else
            echo "镜像 $mirror 失败，尝试下一个..."
        fi
    done
    
    echo "所有镜像都失败，尝试官方源..."
    pip install "$package" --timeout 120 --retries 1
}

# 安装依赖包
install_with_mirror "requests>=2.31.0"
install_with_mirror "selenium>=4.15.0" 
install_with_mirror "webdriver-manager>=4.0.1"

echo "============================================"
echo "依赖安装完成！"
echo "============================================"

# 验证安装
echo "验证安装结果..."
python -c "import requests; print('requests:', requests.__version__)" || echo "requests 未安装"
python -c "import selenium; print('selenium:', selenium.__version__)" || echo "selenium 未安装"
python -c "import webdriver_manager; print('webdriver-manager: OK')" || echo "webdriver-manager 未安装"

echo ""
echo "如果所有包都显示版本号，说明安装成功！"
echo "现在可以运行: ./start_bing_reward.sh" 