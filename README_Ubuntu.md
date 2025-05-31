# Bing 奖励脚本 - Ubuntu 部署包

这是一个自动化的 Bing 搜索脚本，已优化适配 Ubuntu 环境。

## 快速部署

### 1. 安装依赖
```bash
chmod +x setup_ubuntu.sh
./setup_ubuntu.sh
```

### 2. 运行脚本

**桌面环境（有GUI）：**
```bash
./start_bing_reward.sh
```

## 问题解决方案

### pip 安装超时问题

如果遇到 pip 安装超时错误：

**方法1：使用修复脚本**
```bash
chmod +x fix_pip_timeout.sh
./fix_pip_timeout.sh
```

**方法2：手动安装依赖**
```bash
# 激活虚拟环境
source venv/bin/activate

# 使用国内镜像源
pip install requests>=2.31.0 -i https://pypi.tuna.tsinghua.edu.cn/simple/ --trusted-host pypi.tuna.tsinghua.edu.cn
pip install selenium>=4.15.0 -i https://pypi.tuna.tsinghua.edu.cn/simple/ --trusted-host pypi.tuna.tsinghua.edu.cn
pip install webdriver-manager>=4.0.1 -i https://pypi.tuna.tsinghua.edu.cn/simple/ --trusted-host pypi.tuna.tsinghua.edu.cn
```

### ChromeDriver 网络问题

如果遇到 "Could not reach host. Are you offline?" 错误：

**方法1：简化安装（推荐）**
```bash
chmod +x install_chromedriver_simple.sh
./install_chromedriver_simple.sh
```

**方法2：手动安装 ChromeDriver**
```bash
chmod +x install_chromedriver.sh
./install_chromedriver.sh
```

**方法3：使用系统包管理器**
```bash
sudo apt update
sudo apt install chromium-chromedriver
```

### 新版本Chrome问题（如Chrome 137）

如果遇到Chrome版本过新，没有对应ChromeDriver的问题：

**解决方案1：使用系统ChromeDriver**
```bash
sudo apt install chromium-chromedriver
```

**解决方案2：使用兼容版本**
```bash
# 下载兼容的稳定版本
./install_chromedriver_simple.sh
```

**解决方案3：手动下载兼容版本**
```bash
# 下载ChromeDriver 119.x（兼容Chrome 120-137）
wget https://chromedriver.storage.googleapis.com/119.0.6045.105/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
sudo mv chromedriver /usr/local/bin/
sudo chmod +x /usr/local/bin/chromedriver
```

## 说明

- 脚本会自动运行2个浏览器实例
- 最大并行数设置为2，避免系统过载
- 用户配置文件存储在 `/app/bing-reward/chrome_profiles/`
- 首次运行会自动下载 ChromeDriver（如果未手动安装）
- 脚本已优化支持新版本Chrome浏览器

## 系统要求

- Ubuntu 20.04+ 
- 至少 4GB RAM
- Python 3.8+
- 网络连接

## 故障排除

### 网络超时问题
```bash
# 清理 pip 缓存
source venv/bin/activate
pip cache purge

# 使用修复脚本
./fix_pip_timeout.sh
```

### ChromeDriver 问题
```bash
# 检查 ChromeDriver 是否已安装
chromedriver --version

# 方法1: 简化安装
./install_chromedriver_simple.sh

# 方法2: 完整安装
./install_chromedriver.sh

# 方法3: 系统包管理器
sudo apt install chromium-chromedriver

# 检查 Chrome 版本
google-chrome --version
```

### Chrome版本兼容性
| Chrome版本 | 推荐ChromeDriver版本 | 安装方法 |
|-----------|-------------------|---------|
| 137-133   | 119.0.6045.105    | 使用简化脚本 |
| 132-128   | 119.0.6045.105    | 使用简化脚本 |
| 127-123   | 123.0.6312.86     | 手动指定版本 |
| 122-119   | 119.0.6045.105    | 官方下载 |
| 更早版本   | 系统包管理器        | apt install |

### 权限问题
```bash
sudo chown -R $USER:$USER /app/bing-reward/
chmod +x *.sh
```

### Chrome 启动失败
```bash
google-chrome --version
sudo apt install -y google-chrome-stable
```

### 依赖验证
```bash
source venv/bin/activate
python -c "import requests, selenium, webdriver_manager; print('所有依赖已安装')"
```

## 可用脚本

- `setup_ubuntu.sh` - 完整安装（推荐）
- `fix_pip_timeout.sh` - 修复pip超时问题
- `install_chromedriver.sh` - 手动安装ChromeDriver
- `install_chromedriver_simple.sh` - 简化ChromeDriver安装（新）
- `start_bing_reward.sh` - 启动脚本

## 完全离线安装

如果网络环境很差，可以尝试：

1. 先运行基础安装：`sudo apt install python3 python3-pip python3-venv google-chrome-stable chromium-chromedriver`
2. 创建虚拟环境：`python3 -m venv venv`
3. 手动下载依赖包并离线安装
4. 使用系统的 chromium-chromedriver 而不是下载新的

## 最新更新

- ✅ 支持 Chrome 137 等新版本
- ✅ 添加简化安装脚本
- ✅ 改进ChromeDriver版本兼容性
- ✅ 增强网络问题处理
- ✅ 优化系统包管理器支持 