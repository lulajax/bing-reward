#!/bin/bash

# 简化的 ChromeDriver 安装脚本
# 专门处理新版本Chrome兼容性问题

echo "============================================"
echo "简化 ChromeDriver 安装..."
echo "============================================"

# 使用系统包管理器安装（推荐方法）
echo "方法1: 尝试使用系统包管理器安装..."

if command -v apt &> /dev/null; then
    # Ubuntu/Debian
    if sudo apt update && sudo apt install -y chromium-chromedriver; then
        echo "通过 apt 安装 chromium-chromedriver 成功"
        exit 0
    fi
elif command -v yum &> /dev/null; then
    # CentOS/RHEL
    if sudo yum install -y chromedriver; then
        echo "通过 yum 安装 chromedriver 成功"
        exit 0
    fi
elif command -v dnf &> /dev/null; then
    # Fedora
    if sudo dnf install -y chromedriver; then
        echo "通过 dnf 安装 chromedriver 成功"
        exit 0
    fi
fi

echo "系统包管理器安装失败，尝试方法2..."

# 方法2: 下载兼容的稳定版本
echo "方法2: 下载兼容的稳定版本..."

# 使用一个经过测试的稳定版本
STABLE_VERSION="119.0.6045.105"
DOWNLOAD_URL="https://chromedriver.storage.googleapis.com/$STABLE_VERSION/chromedriver_linux64.zip"

echo "下载 ChromeDriver 稳定版本: $STABLE_VERSION"

# 创建临时目录
TMP_DIR="/tmp/chromedriver_stable"
mkdir -p "$TMP_DIR"
cd "$TMP_DIR" || exit 1

# 下载
if wget -O chromedriver_linux64.zip "$DOWNLOAD_URL" >/dev/null 2>&1; then
    echo "下载成功"
elif curl -o chromedriver_linux64.zip "$DOWNLOAD_URL" >/dev/null 2>&1; then
    echo "下载成功"
else
    echo "下载失败，尝试镜像源..."
    MIRROR_URL="https://npm.taobao.org/mirrors/chromedriver/$STABLE_VERSION/chromedriver_linux64.zip"
    if wget -O chromedriver_linux64.zip "$MIRROR_URL" >/dev/null 2>&1; then
        echo "从镜像下载成功"
    else
        echo "所有下载方法都失败了"
        echo "请手动下载 ChromeDriver"
        exit 1
    fi
fi

# 解压并安装
if command -v unzip &> /dev/null; then
    unzip -q chromedriver_linux64.zip
    
    # 尝试安装到系统目录
    if sudo mv chromedriver /usr/local/bin/ 2>/dev/null; then
        sudo chmod +x /usr/local/bin/chromedriver
        echo "安装到 /usr/local/bin/chromedriver 成功"
    else
        # 安装到用户目录
        mkdir -p "$HOME/.local/bin"
        mv chromedriver "$HOME/.local/bin/"
        chmod +x "$HOME/.local/bin/chromedriver"
        echo "安装到 $HOME/.local/bin/chromedriver 成功"
        
        # 添加到PATH
        if ! echo "$PATH" | grep -q "$HOME/.local/bin"; then
            echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.bashrc"
            echo "已将 $HOME/.local/bin 添加到 PATH"
            echo "请运行: source ~/.bashrc 或重新打开终端"
        fi
    fi
else
    echo "错误: 需要安装 unzip: sudo apt install unzip"
    exit 1
fi

# 清理
cd /
rm -rf "$TMP_DIR"

# 验证
echo "验证安装..."
if command -v chromedriver &> /dev/null; then
    echo "ChromeDriver 安装成功！"
    chromedriver --version
else
    echo "安装完成，但可能需要重新加载环境变量"
    echo "请运行: source ~/.bashrc"
fi

echo ""
echo "安装完成！现在可以运行脚本了。" 