# Bing 奖励脚本 - 跨平台版本

这是一个自动化的 Bing 搜索脚本，支持多实例并行运行，已优化适配 Windows、macOS 和 Linux 环境。

## 系统要求

- Python 3.8+
- Google Chrome 浏览器
- 至少 4GB RAM (推荐 8GB 以上)
- 网络连接

## 快速开始

### Windows 用户

1. **安装依赖**
   ```
   双击运行: setup_windows.bat
   ```

2. **运行脚本**
   ```
   双击运行: start_bing_reward.bat
   ```

### Linux/Ubuntu 用户

1. **安装依赖**
   ```bash
   chmod +x setup_ubuntu.sh
   ./setup_ubuntu.sh
   ```

2. **运行脚本**
   ```bash
   ./start_bing_reward.sh
   ```

### macOS 用户

1. **安装依赖**
   ```bash
   # 安装 Homebrew (如果未安装)
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   
   # 安装 Python 和 Chrome
   brew install python@3.11
   brew install --cask google-chrome
   
   # 运行安装脚本
   chmod +x setup_ubuntu.sh
   ./setup_ubuntu.sh
   ```

2. **运行脚本**
   ```bash
   ./start_bing_reward.sh
   ```

## 手动运行

如果需要更多控制，可以直接使用 Python 脚本：

```bash
# 激活虚拟环境
# Windows:
venv\Scripts\activate.bat

# Linux/macOS:
source venv/bin/activate

# 运行脚本
python app/bing_reward_parallel.py 2 ./chrome_profiles/user1 ./chrome_profiles/user2 --max_parallel 2 --headless
```

## 参数说明

- `num_instances`: 要运行的浏览器实例数量
- `user_dirs`: Chrome 用户数据目录路径列表
- `--headless`: 强制使用无头模式 (无GUI)
- `--max_parallel`: 最大并行运行的实例数

## 问题解决

### 网络连接问题

**pip 安装超时 (Linux/macOS):**
```bash
./fix_pip_timeout.sh
```

**ChromeDriver 下载失败:**
```bash
# Linux:
./install_chromedriver.sh

# Windows: 手动下载 ChromeDriver 并放到系统 PATH 中
```

### 跨平台路径问题

脚本已自动适配不同操作系统：
- **Windows**: 使用 `\` 路径分隔符
- **Linux/macOS**: 使用 `/` 路径分隔符
- **ChromeDriver**: 自动检测平台并查找对应路径

### Chrome 浏览器问题

**Windows:**
- 从 [Chrome官网](https://www.google.com/chrome/) 下载安装

**Linux:**
```bash
sudo apt install google-chrome-stable
```

**macOS:**
```bash
brew install --cask google-chrome
```

## 功能特性

- ✅ 跨平台支持 (Windows/Linux/macOS)
- ✅ 自动检测操作系统和环境
- ✅ 智能ChromeDriver查找和下载
- ✅ 多实例并行运行
- ✅ GUI和无头模式自动切换
- ✅ 网络超时和重试机制
- ✅ 详细的日志输出

## 文件结构

```
bing-reward/
├── app/
│   └── bing_reward_parallel.py    # 主程序
├── requirements.txt               # Python依赖
├── setup_windows.bat             # Windows安装脚本
├── setup_ubuntu.sh               # Linux安装脚本
├── start_bing_reward.bat         # Windows启动脚本
├── start_bing_reward.sh          # Linux启动脚本
├── fix_pip_timeout.sh            # 网络问题修复脚本
├── install_chromedriver.sh       # ChromeDriver安装脚本
└── README.md                     # 说明文档
```

## 常见问题

1. **多平台兼容性**: 脚本自动检测操作系统并适配
2. **ChromeDriver版本**: 自动匹配Chrome浏览器版本
3. **网络问题**: 提供多种备用方案和镜像源
4. **资源占用**: 可调整并行实例数量控制资源使用

## 注意事项

- 脚本仅用于自动化搜索，请遵守相关服务条款
- 建议在稳定的网络环境下运行
- 多实例运行会增加系统资源消耗
- 首次运行可能需要较长时间来下载依赖
