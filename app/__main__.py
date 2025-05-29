import time
import random
import requests  # 导入 requests 库
import os      # 导入 os 库
from urllib.parse import quote # 导入 quote 用于 URL 编码
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions # 确保导入的是 ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException, SessionNotCreatedException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager # 导入 ChromeDriverManager

# 默认搜索词列表
DEFAULT_SEARCH_WORDS = [
    "盛年不重来，一日难再晨", "千里之行，始于足下", "少年易学老难成，一寸光阴不可轻",
    "敏而好学，不耻下问", "海内存知已，天涯若比邻", "三人行，必有我师焉",
    "莫愁前路无知已，天下谁人不识君", "人生贵相知，何用金与钱", "天生我材必有用",
    "路漫漫其修远兮，吾将上下而求索", "温故而知新，可以为师矣", "学而不思则罔，思而不学则殆",
    "读书破万卷，下笔如有神", "锲而不舍，金石可镂", "业精于勤，荒于嬉",
]

# 获取热词函数
def get_hot_words():
    keywords_sources = ['BaiduHot', 'TouTiaoHot', 'DouYinHot', 'WeiBoHot']
    api_base = "https://api.gmya.net/Api/"
    appkey = "" # 如果您有 AppKey，请填写在这里

    for source in keywords_sources:
        try:
            url = f"{api_base}{source}"
            if appkey:
                url += f"?appkey={appkey}"

            print(f"尝试从 {source} 获取热词...")
            response = requests.get(url, timeout=15)
            response.raise_for_status() # 如果请求失败 (状态码非 2xx)，则抛出异常
            data = response.json()

            if data.get('code') == 200 and data.get('data'): # 检查 API 返回是否成功且包含数据
                titles = [item['title'] for item in data['data'] if item.get('title')]
                if titles:
                    print(f"成功从 {source} 获取到 {len(titles)} 个热词。")
                    return titles
            else:
                print(f"从 {source} 获取热词失败: {data.get('msg', '未知错误')}")

        except requests.exceptions.RequestException as e:
            print(f"请求 {source} 失败: {str(e)}")
        except Exception as e:
            print(f"处理 {source} 数据失败: {str(e)}")

    print("未能从任何 API 获取热词，将使用默认搜索词。")
    return DEFAULT_SEARCH_WORDS

# 生成随机字符串函数
def generate_random_str(length):
    chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    return ''.join(random.choice(chars) for _ in range(length))

# 查找 Chrome 用户数据目录函数
def find_chrome_user_data_dir():
    # user_profile = os.environ.get('USERPROFILE') # 使用 .get 避免 KeyError
    user_profile = "C:\\Users\\DevToolsUser"# 使用 .get 避免 KeyError
    if not user_profile:
        return None

    chrome_user_data_dir = os.path.join(user_profile, 'AppData', 'Local', 'Google', 'Chrome', 'User Data')

    if not os.path.exists(chrome_user_data_dir):
        print(f"Chrome 用户数据目录不存在，正在创建: {chrome_user_data_dir}")
        os.makedirs(chrome_user_data_dir)  # 创建缺失的目录

    return chrome_user_data_dir

# 设置 WebDriver 函数 (主要修改点)
def setup_driver():
    chrome_options = ChromeOptions() # 使用 ChromeOptions
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36" # 更新为更现代的 User-Agent
    )
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage") # 推荐添加，防止在某些环境下因 /dev/shm 空间不足导致崩溃
    chrome_options.add_argument("--start-maximized")      # 启动时最大化窗口
    # chrome_options.add_argument("--headless")  # 如果需要无头模式，取消此行注释
    # chrome_options.add_argument("--disable-gpu") # 在无头模式或某些环境下可能需要

    chrome_user_data_dir = find_chrome_user_data_dir()
    if chrome_user_data_dir:
        print(f"Chrome 用户数据目录: {chrome_user_data_dir}")
        print("警告: 使用默认用户数据目录可能会与正在运行的 Chrome 实例冲突。如果启动失败，请尝试关闭所有 Chrome 窗口后再试。")
        chrome_options.add_argument(f"user-data-dir={chrome_user_data_dir}")
        # 如果您想使用特定的配置文件（例如 'Profile 1'），可以添加：
        # chrome_options.add_argument("--profile-directory=Default") # 或 'Profile 1', 'Profile 2' 等
    else:
        print("未找到有效的 Chrome 用户数据目录。将使用临时配置文件。")

    try:
        print("正在设置 ChromeDriver...")
        # 使用 ChromeDriverManager().install() 自动下载并设置 ChromeDriver 路径
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        print("ChromeDriver 启动成功。")
        return driver
    except SessionNotCreatedException as e:
        print(f"创建会话失败: {e}")
        print("可能是由于用户数据目录冲突或 ChromeDriver/Chrome 版本问题。")
        print("请确保没有其他 Chrome 实例正在使用该用户数据目录，或尝试不使用用户数据目录运行。")
        # 可以选择在这里添加不带 user-data-dir 的备用启动方案
        return None # 返回 None 表示失败
    except Exception as e:
        print(f"设置 WebDriver 时发生未知错误: {e}")
        return None

# 运行搜索函数
def run_search():
    max_searches = 40
    long_pause = 10
    search_terms = get_hot_words()
    if not search_terms: # 确保 search_terms 不是空的
        print("无法获取搜索词，程序退出。")
        return

    driver = setup_driver()

    if not driver: # 检查 WebDriver 是否成功启动
        print("WebDriver 启动失败，程序退出。")
        return

    try:
        for count in range(max_searches):
            # 切换搜索域名 (确保至少有一个搜索词)
            domain = "www.bing.com" if count < max_searches // 2 else "cn.bing.com"

            # 获取搜索词
            term = search_terms[count % len(search_terms)]
            encoded_term = quote(term) # 使用 quote 进行 URL 编码

            # 生成随机参数
            params = {
                "q": encoded_term,
                "form": generate_random_str(4),
                "cvid": generate_random_str(32)
            }

            # 构建搜索URL
            search_url = f"https://{domain}/search?{'&'.join(f'{k}={v}' for k, v in params.items())}"

            # 执行搜索
            try:
                print(f"正在搜索 ({count + 1}/{max_searches}): {term} @ {domain}")
                driver.get(search_url)

                # 模拟滚动
                print("  模拟滚动...")
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);") # 滚到一半
                time.sleep(random.uniform(1, 3))
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") # 滚到底部
                time.sleep(random.uniform(2, 5))

                # 随机等待
                delay = random.randint(5, 10)
                print(f"  等待 {delay} 秒...")
                time.sleep(delay)

                # 每4次搜索后长暂停
                if (count + 1) % 4 == 0 and (count + 1) < max_searches:
                    print(f"  第 {count + 1} 次搜索后，长暂停 {long_pause} 秒...")
                    time.sleep(long_pause)

            except WebDriverException as e:
                print(f"搜索失败: {str(e)}")
                print("可能是浏览器已关闭或连接中断，尝试继续...")
                # 可以选择在这里添加重新启动 WebDriver 的逻辑，或者直接中断
                # 为了简单起见，我们这里选择中断
                break

    except KeyboardInterrupt:
        print("用户中断了进程。")
    finally:
        if driver: # 确保 driver 对象存在再关闭
            print("正在关闭浏览器...")
            driver.quit()
            print("浏览器已关闭。")

# 主程序入口
if __name__ == "__main__":
    run_search()