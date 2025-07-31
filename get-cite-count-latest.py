from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import time
import dotenv
from dotenv import dotenv_values

dotenv.load_dotenv()
config = dotenv_values(".env")


# 配置Selenium选项
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument(config["User_Agent"])

chromedriver_path = config["chrome_driver_path"]  # 替换为你的chromedriver路径

service = Service(executable_path=chromedriver_path)

# 启动浏览器
driver = webdriver.Chrome(service=service, options=chrome_options)

def get_citation_count(keyword: str) -> int:
    """
    通过学术网站查询关键词相关内容的引用次数
    
    参数:
        keyword: 搜索关键词
        chromedriver_path: Chrome驱动路径，如果已在PATH中可省略
    
    返回:
        引用次数，如果未找到则返回0
    """
    # 替换空格为加号以适应URL格式
    formatted_keyword = keyword.replace(" ", "+")
    url = f"https://www.gupiaoq.com/scholar?q={formatted_keyword}#google_vignette"
    
    
    try:
        # 打开网页
        driver.get(url)
        print(f"正在查询关键词: '{keyword}'")
        print(f"访问URL: {url}")

        # 等待页面加载
        try:
            # 等待引用次数元素出现（显式等待）
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'a:contains("被引用次数")'))
            )
        except:
            # 如果显式等待失败，使用隐式等待
            time.sleep(3)
        
        # 获取页面源代码
        html_content = driver.page_source
        
        # 使用正则表达式提取引用次数
        match = re.search(r'被引用次数：(\d+)</a>', html_content)
        arxiv = re.search(r'arxiv.org/abs/(\d+.\d+)', html_content)
        
        if match:
            citation_count = int(match.group(1))
            print(f"找到引用次数: {citation_count}")
            # return citation_count
        if arxiv:
            arxiv_id = arxiv.group(1)
            print(f"找到arXiv ID: http://arxiv.org/abs/{arxiv_id}")
            # return 0

            
    except Exception as e:
        print(f"发生错误: {e}")
        return 0
    finally:
        # 确保浏览器关闭
        driver.quit()

# 使用示例
if __name__ == "__main__":
    keyword = input("请输入要查询的关键词: ")
    print(get_citation_count(keyword))
    # print(f"'{keyword}' 的引用次数: {count}\n")    