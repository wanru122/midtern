import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta
import json
from snownlp import SnowNLP
import random
import time
import re

# 載入環境變數
load_dotenv()
apikey = os.getenv("API_KEY")

# 定義日期範圍
today = datetime.today()
month_ago = today - timedelta(days=30)
default_from_date = month_ago.strftime('%Y-%m-%d')
default_to_date = today.strftime('%Y-%m-%d')

# 定義相關關鍵字
synonyms = {
    "健康": ["健康", "健身", "健康生活"],
    "疾病": ["疾病", "病症", "病情"],
    "醫療": ["醫療", "醫學", "醫護"],
    "醫生": ["醫生", "醫師"],
    "醫院": ["醫院", "診所"],
    "保健": ["保健", "養生", "護理"],
    "免疫": ["免疫", "免疫系統"],
    "疫苗": ["疫苗", "接種", "免疫"],
    "藥物": ["藥物", "藥品", "藥效"],
    "治療": ["治療", "醫治", "療法"],
    "養生": ["養生", "保健"],
    "疫情": ["疫情", "傳染病", "疫病"],
    "心理": ["心理", "心理健康", "精神"],
}

# 整理相關的關鍵字
relevant_keywords = set()
for keyword, synonym_list in synonyms.items():
    relevant_keywords.update(synonym_list)
relevant_keywords = list(relevant_keywords)

# 查詢參數設定
query_params = {
    'q': " OR ".join(relevant_keywords),
    'from': default_from_date,
    'to': default_to_date,
}

# 使用者自定義關鍵字
user_query = input(f"請輸入關鍵字（預設: {query_params['q']}）：") or query_params['q']
query_params['q'] = user_query

# API請求參數
params = {
    'q': query_params['q'],
    'language': 'zh',
    'from': query_params['from'],
    'to': query_params['to'],
    'apiKey': apikey,
    'sortBy': 'popularity',
    'pageSize': 100,
    'page': 1
}

# 用來儲存API抓取的文章
api_articles = []

# 進行多頁抓取，這裡只請求第 1 頁，避免超過限制
for page in range(1, 2):  # 只請求第 1 頁
    params['page'] = page
    try:
        response = requests.get('https://newsapi.org/v2/everything', params=params)
        response.raise_for_status()
        articles = response.json().get('articles', [])
        api_articles.extend(articles)
        if not articles:
            break
    except requests.exceptions.RequestException as e:
        print(f"第 {page} 頁請求失敗: {e}")
        break

# 爬取文章資料
scraped_articles = []

def scrape_healthnews():
    try:
        url = "https://www.healthnews.com.tw/"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        articles = soup.find_all('a')
        for article in articles:
            title = article.text.strip()
            link = article.get('href', '')
            if not title or not link or "javascript:void(0)" in link:
                continue  # 過濾掉無效鏈接
            if not link.startswith("http"):
                link = "https://www.healthnews.com.tw" + link
            if any(keyword in title for keyword in relevant_keywords):
                scraped_articles.append({
                    'title': title,
                    'url': link,
                    'source': "健康醫療網"
                })
    except requests.exceptions.RequestException as e:
        print(f"爬取健康醫療網失敗: {e}")

def scrape_yahoo_health():
    try:
        url = "https://tw.news.yahoo.com/health"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, allow_redirects=True)
        
        # 檢查是否被重定向到同意頁面
        if "consent.yahoo.com" in response.url:
            print("被重定向至同意頁面，跳過此頁面。")
            return
        
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        articles = soup.find_all('a')
        for article in articles:
            title = article.text.strip()
            link = article.get('href', '')
            if not title or not link:
                continue
            if not link.startswith("http"):
                link = "https://tw.news.yahoo.com" + link
            if any(keyword in title for keyword in relevant_keywords):
                scraped_articles.append({
                    'title': title,
                    'url': link,
                    'source': "Yahoo 健康專區"
                })
    except requests.exceptions.RequestException as e:
        print(f"爬取 Yahoo 健康專區失敗: {e}")



scrape_healthnews()
scrape_yahoo_health()

# 整合API和爬蟲抓取的文章
all_articles = []

for article in api_articles:
    title = article.get('title', '無標題')
    description = article.get('description', '無描述')
    content = article.get('content', '')
    url = article.get('url', '#')

    if any(keyword in title or keyword in description or keyword in content for keyword in relevant_keywords):
        all_articles.append({
            'title': title,
            'description': description,
            'url': url,
            'source': "NewsAPI"
        })

seen_titles = set([article['title'] for article in all_articles])
for article in scraped_articles:
    if article['title'] not in seen_titles:
        all_articles.append({
            'title': article['title'],
            'description': '此新聞來自爬蟲，無詳細描述。',
            'url': article['url'],
            'source': article['source']
        })

# 使用 SnowNLP 進行情感分析
for article in all_articles:
    s = SnowNLP(article['title'])
    sentiment_score = s.sentiments

    if sentiment_score > 0.6:
        article['sentiment'] = '😊'  
    elif sentiment_score < 0.4:
        article['sentiment'] = '😢'  
    else:
        article['sentiment'] = '😐'  

time.sleep(random.uniform(1, 3))

# 定義函數來加粗關鍵字
def highlight_keywords(text, keywords):
    for keyword in keywords:
        text = re.sub(r'(?i)(' + re.escape(keyword) + r')', r'<b>\1</b>', text)
    return text

# 儲存到HTML檔案
html_file = 'news.html'
current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
with open(html_file, mode='w+', encoding='utf-8') as file:
    file.write(f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>新聞整理</title>
    <link rel="stylesheet" type="text/css" href="liang.css">
</head>
<body>
    <header>
        <a href="index.html"><h3><img src="image/logo.jpg" class="logo"></h3></a>
        <nav>
            <a href="news.html"><h3>相關新聞</h3></a>
            <a href="健康分析工具/bmi/submit.html"><h3>健康分析工具</h3></a>
            <a href="cb.html"><h3>Chat Bot</h3></a>
            <a href="test.html"><h3>百萬小學堂</h3></a>
            <a href="health.html"><h3>健康檢查提醒</h3></a>
        </nav>
    </header>
    <div class="news-container">
''')

    for article in all_articles:
        highlighted_title = highlight_keywords(article["title"], relevant_keywords)
        highlighted_description = highlight_keywords(article["description"], relevant_keywords)

        file.write(f'''
        <div class="news-card">
            <h2><a href="{article["url"]}" target="_blank">{highlighted_title}</a></h2>
            <p>{highlighted_description}</p>
            <p>情感分析: {article["sentiment"]}</p>
        </div>
        ''')

    file.write(f'''
    </div>
               <a href="#" class="back-to-top">回到最上面</a>
    <footer class='footer2'>
        <p>保健巴拉拉. 為您服務</p>
        <p>更新時間: {current_time}</p>
    </footer>
</body>
</html>
''')

print(f"\n已匯出 {len(all_articles)} 篇新聞至 {html_file}")


# 儲存為JSON
json_file = 'news.json'
with open(json_file, mode='w+', encoding='utf-8') as file:
    json.dump(all_articles, file, ensure_ascii=False, indent=4)

print(f"\n已匯出 {len(all_articles)} 篇新聞至 {json_file}")
