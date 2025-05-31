import time
import random
import requests  # 导入 requests 库
import os  # 导入 os 库
import platform  # 导入 platform 用于检测操作系统
from urllib.parse import quote  # 导入 quote 用于 URL 编码
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException, SessionNotCreatedException, NoSuchElementException
import argparse  # 导入 argparse 用于命令行参数处理
import multiprocessing  # 导入 multiprocessing 用于并行处理

# 默认搜索词列表
DEFAULT_SEARCH_WORDS = [
    "盛年不重来，一日难再晨", "千里之行，始于足下", "少年易学老难成，一寸光阴不可轻",
    "敏而好学，不耻下问", "海内存知已，天涯若比邻", "三人行，必有我师焉",
    "莫愁前路无知已，天下谁人不识君", "人生贵相知，何用金与钱", "天生我材必有用",
    "路漫漫其修远兮，吾将上下而求索", "温故而知新，可以为师矣", "学而不思则罔，思而不学则殆",
    "读书破万卷，下笔如有神", "锲而不舍，金石可镂", "业精于勤，荒于嬉",
]


# 获取热词函数
def get_hot_words(instance_num_for_log=""):
    # 为日志添加实例编号前缀
    log_prefix = f"[实例 {instance_num_for_log}] " if instance_num_for_log else ""
    keywords_sources = ['BaiduHot', 'TouTiaoHot', 'DouYinHot', 'WeiBoHot']
    api_base = "https://api.gmya.net/Api/"
    appkey = ""  # 如果您有 AppKey，请填写在这里

    for source in keywords_sources:
        try:
            url = f"{api_base}{source}"
            if appkey:
                url += f"?appkey={appkey}"

            print(f"{log_prefix}尝试从 {source} 获取热词...")
            response = requests.get(url, timeout=15)
            response.raise_for_status()
            data = response.json()

            if data.get('code') == 200 and data.get('data'):
                titles = [item['title'] for item in data['data'] if item.get('title')]
                if titles:
                    print(f"{log_prefix}成功从 {source} 获取到 {len(titles)} 个热词。")
                    return titles
            else:
                print(f"{log_prefix}从 {source} 获取热词失败: {data.get('msg', '未知错误')}")

        except requests.exceptions.RequestException as e:
            print(f"{log_prefix}请求 {source} 失败: {str(e)}")
        except Exception as e:
            print(f"{log_prefix}处理 {source} 数据失败: {str(e)}")

    print(f"{log_prefix}未能从任何 API 获取热词，将使用默认搜索词。")
    return DEFAULT_SEARCH_WORDS


# 生成随机字符串函数
def generate_random_str(length):
    chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    return ''.join(random.choice(chars) for _ in range(length))


# 查找系统 ChromeDriver
def find_system_chromedriver():
    """查找系统中已安装的 ChromeDriver，支持多平台"""
    import shutil
    
    # 首先尝试在 PATH 中查找（适用于所有平台）
    chromedriver_path = shutil.which('chromedriver')
    if chromedriver_path:
        return chromedriver_path
    
    # 根据操作系统检查常见路径
    system = platform.system().lower()
    
    if system == 'linux':
        # Linux 常见路径
        linux_paths = [
            '/usr/bin/chromedriver',
            '/usr/local/bin/chromedriver',
            '/snap/bin/chromium.chromedriver',
            '/usr/lib/chromium-browser/chromedriver',
            '/opt/google/chrome/chromedriver',
        ]
        for path in linux_paths:
            if os.path.exists(path) and os.access(path, os.X_OK):
                return path
                
    elif system == 'darwin':  # macOS
        # macOS 常见路径
        macos_paths = [
            '/usr/local/bin/chromedriver',
            '/opt/homebrew/bin/chromedriver',
            '/Applications/Google Chrome.app/Contents/MacOS/chromedriver',
        ]
        for path in macos_paths:
            if os.path.exists(path) and os.access(path, os.X_OK):
                return path
                
    elif system == 'windows':
        # Windows 常见路径
        windows_paths = [
            r'C:\Program Files\Google\Chrome\Application\chromedriver.exe',
            r'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe',
            r'C:\Windows\System32\chromedriver.exe',
            r'C:\chromedriver.exe',
        ]
        for path in windows_paths:
            if os.path.exists(path):
                return path
        
        # Windows 下也尝试查找 .exe 版本
        chromedriver_exe = shutil.which('chromedriver.exe')
        if chromedriver_exe:
            return chromedriver_exe
    
    return None


# 设置 WebDriver 函数
def setup_driver(user_data_dir, instance_num, headless=False):
    log_prefix = f"[实例 {instance_num}] "
    print(f"{log_prefix}正在设置 WebDriver...")
    chrome_options = ChromeOptions()
    
    # 根据操作系统设置 User-Agent
    system = platform.system().lower()
    if system == 'linux':
        user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
    elif system == 'darwin':  # macOS
        user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
    elif system == 'windows':
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
    else:
        user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
    
    # 基本设置
    chrome_options.add_argument(f"user-agent={user_agent}")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-plugins")
    chrome_options.add_argument("--disable-images")  # 禁用图片加载以提高性能
    chrome_options.add_argument("--disable-javascript")  # 可选：禁用JavaScript以提高性能
    
    # 只有在明确指定 headless 参数时才使用无头模式
    if headless:
        print(f"{log_prefix}使用无头模式运行")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
    else:
        print(f"{log_prefix}使用GUI模式运行")
        chrome_options.add_argument("--start-maximized")

    if user_data_dir:
        if not os.path.exists(user_data_dir):
            print(f"{log_prefix}Chrome 用户数据目录不存在，正在创建: {user_data_dir}")
            try:
                os.makedirs(user_data_dir, exist_ok=True)
            except OSError as e:
                print(f"{log_prefix}创建用户数据目录失败: {e}。将使用临时配置文件。")
                user_data_dir = None

        if user_data_dir:
            print(f"{log_prefix}使用 Chrome 用户数据目录: {user_data_dir}")
            chrome_options.add_argument(f"user-data-dir={user_data_dir}")
    else:
        print(f"{log_prefix}未提供有效的 Chrome 用户数据目录。将使用临时配置文件。")

    try:
        print(f"{log_prefix}正在设置 ChromeDriver...")
        print(f"{log_prefix}检测到操作系统: {platform.system()}")
        
        # 优先使用 webdriver-manager 自动下载最新版本的 ChromeDriver
        print(f"{log_prefix}使用 webdriver-manager 自动下载 ChromeDriver...")
        try:
            from webdriver_manager.chrome import ChromeDriverManager
            service = ChromeService(ChromeDriverManager().install())
            print(f"{log_prefix}webdriver-manager 下载成功")
        except Exception as e:
            print(f"{log_prefix}webdriver-manager 失败: {e}")
            # 如果 webdriver-manager 失败，才尝试查找系统已安装的 ChromeDriver
            print(f"{log_prefix}尝试查找系统已安装的 ChromeDriver...")
            system_chromedriver = find_system_chromedriver()
            if system_chromedriver:
                print(f"{log_prefix}使用系统 ChromeDriver: {system_chromedriver}")
                service = ChromeService(system_chromedriver)
            else:
                print(f"{log_prefix}未找到系统 ChromeDriver，请手动安装 ChromeDriver 或检查网络连接")
                return None
        
        driver = webdriver.Chrome(service=service, options=chrome_options)
        print(f"{log_prefix}ChromeDriver 启动成功。")
        return driver
        
    except SessionNotCreatedException as e:
        print(f"{log_prefix}创建会话失败: {e}")
        print(f"{log_prefix}可能是由于用户数据目录冲突或 ChromeDriver/Chrome 版本问题。")
        return None
    except Exception as e:
        print(f"{log_prefix}设置 WebDriver 时发生未知错误: {e}")
        return None


# 运行搜索函数 (这是每个进程将执行的函数)
def run_search(user_data_dir, instance_num, headless=False):
    log_prefix = f"[实例 {instance_num}] "
    print(f"{log_prefix}--- 开始运行 (用户目录: {user_data_dir or '临时配置'}) ---")
    max_searches = 40  # 可以考虑将此值也作为参数传入，如果希望每个实例搜索次数不同
    long_pause = 10

    # 传递实例编号给 get_hot_words 以便日志区分
    search_terms = get_hot_words(instance_num_for_log=str(instance_num))
    if not search_terms:
        print(f"{log_prefix}无法获取搜索词，程序退出。")
        return

    driver = setup_driver(user_data_dir, instance_num, headless)

    if not driver:
        print(f"{log_prefix}WebDriver 启动失败，程序退出。")
        return

    try:
        for count in range(max_searches):
            # 确保 search_terms 不为空
            if not search_terms:
                print(f"{log_prefix}搜索词列表为空，跳过此轮搜索。")
                break

            domain = "www.bing.com" if count < max_searches // 2 else "cn.bing.com"
            term = search_terms[count % len(search_terms)]
            encoded_term = quote(term)

            params = {
                "q": encoded_term,
                "form": generate_random_str(4),
                "cvid": generate_random_str(32)
            }
            search_url = f"https://{domain}/search?{'&'.join(f'{k}={v}' for k, v in params.items())}"

            try:
                print(f"{log_prefix}正在搜索 ({count + 1}/{max_searches}): {term} @ {domain}")
                driver.get(search_url)

                print(f"{log_prefix}  模拟滚动...")
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
                time.sleep(random.uniform(1, 3))
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(random.uniform(2, 5))

                delay = random.randint(5, 10)
                print(f"{log_prefix}  等待 {delay} 秒...")
                time.sleep(delay)

                if (count + 1) % 4 == 0 and (count + 1) < max_searches:
                    print(f"{log_prefix}  第 {count + 1} 次搜索后，长暂停 {long_pause} 秒...")
                    time.sleep(long_pause)

            except WebDriverException as e:
                print(f"{log_prefix}搜索失败: {str(e)}")
                print(f"{log_prefix}可能是浏览器已关闭或连接中断。")
                # 在并行模式下，一个实例失败不应停止其他实例，因此这里只跳出当前实例的循环
                break
            except Exception as e:  # 捕获更广泛的异常
                print(f"{log_prefix}在搜索循环中发生意外错误: {str(e)}")
                break

    except KeyboardInterrupt:
        # KeyboardInterrupt 通常由主进程捕获，子进程可能以不同方式响应
        print(f"{log_prefix}用户中断了进程 (或主进程已终止)。")
    except Exception as e:
        print(f"{log_prefix}在 run_search 外部循环发生未知错误: {e}")
    finally:
        if driver:
            print(f"{log_prefix}正在关闭浏览器...")
            try:
                driver.quit()
                print(f"{log_prefix}浏览器已关闭。")
            except Exception as e:
                print(f"{log_prefix}关闭浏览器时出错: {e}")
    print(f"{log_prefix}--- 运行结束 ---")


# 主程序入口
if __name__ == "__main__":
    multiprocessing.freeze_support()  # <--- 必须是这里的第一行！！！

    # 然后才是 argparse 的设置和解析
    parser = argparse.ArgumentParser(description="并行运行 Bing 搜索脚本的多个实例...")
    parser.add_argument("num_instances", type=int, help="要运行的浏览器实例数量。")
    parser.add_argument("user_dirs", type=str, nargs='+', metavar='USER_DIR_PATH',
                        help="Chrome 用户数据目录的路径列表。数量必须与 num_instances 匹配。")
    parser.add_argument("--max_parallel", type=int, default=None,
                        help="最大并行运行的实例数。默认为 num_instances（即全部并行）。")
    parser.add_argument("--headless", action="store_true",
                        help="强制使用无头模式运行浏览器（无GUI）。")

    args = parser.parse_args()

    if args.num_instances <= 0:
        print("错误: 实例数量必须大于 0。")
        exit(1)

    if len(args.user_dirs) != args.num_instances:
        print(f"错误: 提供了 {len(args.user_dirs)} 个用户目录路径，但指定的实例数量是 {args.num_instances}。")
        print("请确保用户目录路径的数量与实例数量一致。")
        exit(1)

    max_concurrent_processes = args.max_parallel if args.max_parallel and args.max_parallel > 0 else args.num_instances
    if args.max_parallel and args.max_parallel > args.num_instances:
        print(f"警告: 最大并行数 ({args.max_parallel}) 大于实例总数 ({args.num_instances})。将并行运行所有实例。")
        max_concurrent_processes = args.num_instances

    print(f"准备并行运行 {args.num_instances} 个浏览器实例 (最大同时运行 {max_concurrent_processes} 个)...")
    print("警告: 并行运行多个浏览器实例会消耗大量系统资源 (CPU 和内存)。请确保您的计算机配置充足。")
    
    if args.headless:
        print("使用无头模式运行所有实例。")

    processes = []
    running_processes = []  # 用于跟踪当前正在运行的进程

    try:
        for i in range(args.num_instances):
            instance_number = i + 1
            user_data_directory = args.user_dirs[i]

            # 如果当前运行的进程数达到最大并行数，则等待一个进程完成后再启动新的
            while len(running_processes) >= max_concurrent_processes:
                for p_idx, p in enumerate(running_processes):
                    if not p.is_alive():
                        p.join()  # 清理已完成的进程
                        running_processes.pop(p_idx)
                        break  # 跳出内层 for 循环，重新检查 while 条件
                time.sleep(1)  # 短暂等待，避免CPU空转

            print(f"主程序: 准备启动实例 {instance_number} 使用用户目录: '{user_data_directory}'")
            # 创建进程
            process = multiprocessing.Process(target=run_search, args=(user_data_directory, instance_number, args.headless))
            processes.append(process)
            running_processes.append(process)
            process.start()
            # 稍微错开启动时间，可能有助于避免初始资源竞争
            time.sleep(random.uniform(0.5, 2.0))

        # 等待所有启动的进程完成
        print("主程序: 所有实例已启动。等待它们完成...")
        for process in processes:
            process.join()  # 等待该进程结束

    except KeyboardInterrupt:
        print("\n主程序: 检测到用户中断 (Ctrl+C)。正在尝试终止所有子进程...")
        for process in processes:
            if process.is_alive():
                print(f"主程序: 终止进程 PID {process.pid}...")
                process.terminate()  # 尝试友好终止
                process.join(timeout=5)  # 等待一小段时间
                if process.is_alive():
                    print(f"主程序: 进程 PID {process.pid} 未能在5秒内终止，强制终止...")
                    process.kill()  # 如果 terminate 不行，则强制 kill
                    process.join()  # 等待 kill 完成
        print("主程序: 所有子进程已尝试终止。")
    except Exception as e:
        print(f"主程序: 发生未预料的错误: {e}")
    finally:
        print("\n主程序: 所有实例运行完毕或已终止。")