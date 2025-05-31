#!/bin/bash

# 手动安装 ChromeDriver 脚本
# 解决网络连接问题导致的 webdriver-manager 失败

echo "============================================"
echo "手动安装 ChromeDriver..."
echo "============================================"

# 检查 Chrome 版本
if command -v google-chrome &> /dev/null; then
    CHROME_VERSION=$(google-chrome --version | grep -oP '\d+\.\d+\.\d+')
    echo "检测到 Chrome 版本: $CHROME_VERSION"
else
    echo "警告: 未找到 Google Chrome，请先安装 Chrome"
    exit 1
fi

# 获取主版本号
CHROME_MAJOR_VERSION=$(echo $CHROME_VERSION | cut -d. -f1)
echo "Chrome 主版本号: $CHROME_MAJOR_VERSION"

# ChromeDriver 下载地址
CHROMEDRIVER_URL="https://chromedriver.storage.googleapis.com/LATEST_RELEASE_$CHROME_MAJOR_VERSION"
echo "正在获取 ChromeDriver 版本信息..."

# 尝试获取对应版本的 ChromeDriver
if CHROMEDRIVER_VERSION=$(curl -s $CHROMEDRIVER_URL 2>/dev/null); then
    echo "找到对应的 ChromeDriver 版本: $CHROMEDRIVER_VERSION"
else
    echo "无法获取 ChromeDriver 版本信息，尝试使用通用版本..."
    # 使用一些常见的稳定版本
    case $CHROME_MAJOR_VERSION in
        "120"|"121"|"122"|"123"|"124"|"125")
            CHROMEDRIVER_VERSION="120.0.6099.109"
            ;;
        *)
            CHROMEDRIVER_VERSION="119.0.6045.105"
            ;;
    esac
    echo "使用 ChromeDriver 版本: $CHROMEDRIVER_VERSION"
fi

# 下载 ChromeDriver
DOWNLOAD_URL="https://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip"
echo "下载地址: $DOWNLOAD_URL"

# 创建临时目录
TMP_DIR="/tmp/chromedriver_install"
mkdir -p $TMP_DIR
cd $TMP_DIR

echo "正在下载 ChromeDriver..."
if wget -O chromedriver_linux64.zip "$DOWNLOAD_URL" 2>/dev/null; then
    echo "下载成功"
elif curl -o chromedriver_linux64.zip "$DOWNLOAD_URL" 2>/dev/null; then
    echo "下载成功 (使用 curl)"
else
    echo "下载失败，尝试备用方案..."
    
    # 备用下载方案：使用镜像站点
    MIRROR_URLS=(
        "https://npm.taobao.org/mirrors/chromedriver/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip"
        "https://registry.npmmirror.com/-/binary/chromedriver/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip"
    )
    
    downloaded=false
    for mirror_url in "${MIRROR_URLS[@]}"; do
        echo "尝试镜像: $mirror_url"
        if wget -O chromedriver_linux64.zip "$mirror_url" 2>/dev/null || curl -o chromedriver_linux64.zip "$mirror_url" 2>/dev/null; then
            echo "从镜像下载成功"
            downloaded=true
            break
        fi
    done
    
    if [ "$downloaded" = false ]; then
        echo "所有下载尝试都失败了"
        echo "请手动下载 ChromeDriver 并放置到 /usr/local/bin/chromedriver"
        echo "下载地址: $DOWNLOAD_URL"
        exit 1
    fi
fi

# 解压
echo "正在解压..."
if command -v unzip &> /dev/null; then
    unzip -q chromedriver_linux64.zip
else
    echo "错误: 未找到 unzip 命令，请安装: sudo apt install unzip"
    exit 1
fi

# 安装到系统路径
echo "正在安装 ChromeDriver..."
sudo mv chromedriver /usr/local/bin/
sudo chmod +x /usr/local/bin/chromedriver

# 验证安装
if /usr/local/bin/chromedriver --version &>/dev/null; then
    echo "ChromeDriver 安装成功！"
    /usr/local/bin/chromedriver --version
else
    echo "ChromeDriver 安装可能失败，请检查"
    exit 1
fi

# 清理临时文件
cd /
rm -rf $TMP_DIR

echo ""
echo "============================================"
echo "ChromeDriver 安装完成！"
echo "============================================"
echo ""
echo "现在可以运行脚本了："
echo "./start_bing_reward.sh"
echo "" 