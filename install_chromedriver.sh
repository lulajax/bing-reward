#!/bin/bash

# 手动安装 ChromeDriver 脚本
# 解决网络连接问题导致的 webdriver-manager 失败

echo "============================================"
echo "手动安装 ChromeDriver..."
echo "============================================"

# 检查 Chrome 版本
if command -v google-chrome &> /dev/null; then
    CHROME_VERSION=$(google-chrome --version | grep -oE '[0-9]+\.[0-9]+\.[0-9]+')
    echo "检测到 Chrome 版本: $CHROME_VERSION"
else
    echo "警告: 未找到 Google Chrome，请先安装 Chrome"
    exit 1
fi

# 获取主版本号
CHROME_MAJOR_VERSION=$(echo $CHROME_VERSION | cut -d. -f1)
echo "Chrome 主版本号: $CHROME_MAJOR_VERSION"

# 根据Chrome版本选择ChromeDriver版本
get_chromedriver_version() {
    local chrome_major=$1
    
    # 对于较新的Chrome版本，使用映射表
    case $chrome_major in
        "137"|"136"|"135"|"134"|"133")
            echo "119.0.6045.105"  # 使用稳定版本
            ;;
        "132"|"131"|"130"|"129"|"128")
            echo "119.0.6045.105"
            ;;
        "127"|"126"|"125"|"124"|"123")
            echo "123.0.6312.86"
            ;;
        "122"|"121"|"120"|"119")
            echo "119.0.6045.105"
            ;;
        "118"|"117"|"116"|"115")
            echo "115.0.5790.102"
            ;;
        *)
            echo "114.0.5735.90"  # 默认稳定版本
            ;;
    esac
}

# 首先尝试从官方API获取版本
CHROMEDRIVER_URL="https://chromedriver.storage.googleapis.com/LATEST_RELEASE_$CHROME_MAJOR_VERSION"
echo "正在获取 ChromeDriver 版本信息..."

# 尝试获取对应版本的 ChromeDriver
CHROMEDRIVER_VERSION=$(curl -s "$CHROMEDRIVER_URL" 2>/dev/null)

# 检查返回值是否包含错误信息（XML格式的错误）
if [[ -z "$CHROMEDRIVER_VERSION" ]] || [[ "$CHROMEDRIVER_VERSION" == *"Error"* ]] || [[ "$CHROMEDRIVER_VERSION" == *"xml"* ]]; then
    echo "官方API无法获取 Chrome $CHROME_MAJOR_VERSION 对应的 ChromeDriver 版本"
    echo "使用兼容版本映射表..."
    CHROMEDRIVER_VERSION=$(get_chromedriver_version "$CHROME_MAJOR_VERSION")
    echo "选择兼容的 ChromeDriver 版本: $CHROMEDRIVER_VERSION"
else
    echo "找到对应的 ChromeDriver 版本: $CHROMEDRIVER_VERSION"
fi

# 下载 ChromeDriver
DOWNLOAD_URL="https://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip"
echo "下载地址: $DOWNLOAD_URL"

# 创建临时目录
TMP_DIR="/tmp/chromedriver_install"
mkdir -p "$TMP_DIR"
cd "$TMP_DIR" || exit 1

echo "正在下载 ChromeDriver..."

download_success=false

# 尝试下载
if wget -O chromedriver_linux64.zip "$DOWNLOAD_URL" >/dev/null 2>&1; then
    echo "下载成功 (使用 wget)"
    download_success=true
elif curl -o chromedriver_linux64.zip "$DOWNLOAD_URL" >/dev/null 2>&1; then
    echo "下载成功 (使用 curl)"
    download_success=true
else
    echo "官方下载失败，尝试备用方案..."
    
    # 备用下载方案：使用镜像站点
    MIRROR_URLS=(
        "https://npm.taobao.org/mirrors/chromedriver/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip"
        "https://registry.npmmirror.com/-/binary/chromedriver/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip"
    )
    
    for mirror_url in "${MIRROR_URLS[@]}"; do
        echo "尝试镜像: $mirror_url"
        if wget -O chromedriver_linux64.zip "$mirror_url" >/dev/null 2>&1; then
            echo "从镜像下载成功 (wget)"
            download_success=true
            break
        elif curl -o chromedriver_linux64.zip "$mirror_url" >/dev/null 2>&1; then
            echo "从镜像下载成功 (curl)"
            download_success=true
            break
        fi
    done
fi

if [ "$download_success" = false ]; then
    echo "所有下载尝试都失败了"
    echo "请手动下载 ChromeDriver 并放置到 /usr/local/bin/chromedriver"
    echo "建议下载地址: https://chromedriver.chromium.org/downloads"
    exit 1
fi

# 检查下载的文件是否存在
if [ ! -f "chromedriver_linux64.zip" ]; then
    echo "错误: 下载的文件不存在"
    exit 1
fi

# 解压
echo "正在解压..."
if command -v unzip &> /dev/null; then
    if unzip -q chromedriver_linux64.zip; then
        echo "解压成功"
    else
        echo "解压失败"
        exit 1
    fi
else
    echo "错误: 未找到 unzip 命令，请安装: sudo apt install unzip"
    exit 1
fi

# 检查解压后的文件
if [ ! -f "chromedriver" ]; then
    echo "错误: 解压后未找到 chromedriver 文件"
    exit 1
fi

# 安装到系统路径
echo "正在安装 ChromeDriver..."
if sudo mv chromedriver /usr/local/bin/; then
    sudo chmod +x /usr/local/bin/chromedriver
    echo "ChromeDriver 已安装到 /usr/local/bin/chromedriver"
else
    echo "安装失败，尝试备用路径..."
    # 如果没有sudo权限，尝试安装到用户目录
    mkdir -p "$HOME/.local/bin"
    mv chromedriver "$HOME/.local/bin/"
    chmod +x "$HOME/.local/bin/chromedriver"
    echo "ChromeDriver 已安装到 $HOME/.local/bin/chromedriver"
    echo "请确保 $HOME/.local/bin 在您的 PATH 中"
fi

# 验证安装
echo "验证安装..."
if command -v chromedriver &> /dev/null; then
    echo "ChromeDriver 安装成功！"
    chromedriver --version
elif [ -f "/usr/local/bin/chromedriver" ]; then
    echo "ChromeDriver 安装成功！"
    /usr/local/bin/chromedriver --version
elif [ -f "$HOME/.local/bin/chromedriver" ]; then
    echo "ChromeDriver 安装成功！"
    "$HOME/.local/bin/chromedriver" --version
else
    echo "ChromeDriver 安装可能失败，请检查"
    exit 1
fi

# 清理临时文件
cd / || exit 1
rm -rf "$TMP_DIR"

echo ""
echo "============================================"
echo "ChromeDriver 安装完成！"
echo "============================================"
echo ""
echo "现在可以运行脚本了："
echo "./start_bing_reward.sh"
echo "" 