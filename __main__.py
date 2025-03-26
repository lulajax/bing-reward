import time
import random
import requests
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
from urllib.parse import quote

DEFAULT_SEARCH_WORDS = [
    "盛年不重来，一日难再晨", "千里之行，始于足下", "少年易学老难成，一寸光阴不可轻",
    "敏而好学，不耻下问", "海内存知已，天涯若比邻", "三人行，必有我师焉",
    "莫愁前路无知已，天下谁人不识君", "人生贵相知，何用金与钱", "天生我材必有用",
    # ...（其他默认搜索词）
]


def get_hot_words():
    keywords_sources = ['BaiduHot', 'TouTiaoHot', 'DouYinHot', 'WeiBoHot']
    api_base = "https://api.gmya.net/Api/"
    appkey = ""

    for source in keywords_sources:
        try:
            url = f"{api_base}{source}"
            if appkey:
                url += f"?appkey={appkey}"

            response = requests.get(url, timeout=15)
            response.raise_for_status()
            data = response.json()

            if data.get('data'):
                titles = [item['title'] for item in data['data'] if item.get('title')]
                if titles:
                    return titles
        except Exception as e:
            print(f"Failed to get {source}: {str(e)}")

    print("Using default search words")
    return DEFAULT_SEARCH_WORDS


def generate_random_str(length):
    chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    return ''.join(random.choice(chars) for _ in range(length))


def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"
    )
    chrome_options.add_argument("--no-sandbox")

    chrome_user_data_dir = find_chrome_user_data_dir()
    if chrome_user_data_dir and os.path.exists(chrome_user_data_dir):
        print(f"Chrome 用户数据目录: {chrome_user_data_dir}")
        chrome_options.add_argument(f"user-data-dir={chrome_user_data_dir}")
    else:
        print("未找到有效的 Chrome 用户数据目录。")

    # edge_options.add_argument("--headless")  # 取消注释启用无头模式
    return webdriver.Edge(options=chrome_options)

def find_edge_user_data_dir():
    user_profile = os.environ['USERPROFILE']
    edge_user_data_dir = os.path.join(user_profile, 'AppData', 'Local', 'Microsoft', 'Edge', 'User Data')

    if os.path.exists(edge_user_data_dir):
        return edge_user_data_dir
    else:
        return None

def find_chrome_user_data_dir():
    user_profile = os.environ['USERPROFILE']
    chrom_user_data_dir = os.path.join(user_profile, 'AppData', 'Local', 'Google', 'Chrome', 'User Data')
    if os.path.exists(chrom_user_data_dir):
        return chrom_user_data_dir
    else:
        return None

def run_search():
    max_searches = 40
    long_pause = 10
    search_terms = get_hot_words()
    driver = setup_driver()

    try:
        for count in range(max_searches):
            # 切换搜索域名
            domain = "www.bing.com" if count < max_searches // 2 else "cn.bing.com"

            # 获取搜索词
            term = search_terms[count % len(search_terms)]
            encoded_term = quote(term)

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
                print(f"Searching ({count + 1}/{max_searches}): {term}")
                driver.get(search_url)

                # 模拟滚动
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
                time.sleep(random.uniform(2, 5))

                # 随机等待
                delay = random.randint(5, 10)
                time.sleep(delay)

                # 每4次搜索后长暂停
                if (count + 1) % 4 == 0:
                    print(f"Long pause after {count + 1} searches")
                    time.sleep(long_pause)

            except WebDriverException as e:
                print(f"Search failed: {str(e)}")
                break

    except KeyboardInterrupt:
        print("Process interrupted")
    finally:
        driver.quit()
        print("Browser closed")


if __name__ == "__main__":
    run_search()