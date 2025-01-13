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
import logging

# 設置日誌記錄
logging.basicConfig(filename='error.log', level=logging.ERROR, format='%(asctime)s - %(message)s')

# 載入環境變數
load_dotenv()
apikey = os.getenv("API_KEY")
if not apikey:
    raise ValueError("API_KEY 未正確設置，請檢查 .env 檔案。")

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

relevant_keywords = list(set(word for synonyms_list in synonyms.values() for word in synonyms_list))

# 查詢參數設置
query_params = {
    'q': " OR ".join(relevant_keywords),
    'from': default_from_date,
    'to': default_to_date,
}

# 使用者自定義關鍵字
user_query = input(f"請輸入關鍵字（預設: {query_params['q']}）：") or query_params['q']
query_params['q'] = user_query

# API 請求參數
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

# 用來儲存 API 抓取的文章
api_articles = []

# API 抓取函數
def fetch_api_articles():
    global api_articles
    for page in range(1, 2):  # 只請求第 1 頁，避免超過限制
        params['page'] = page
        try:
            response = requests.get('https://newsapi.org/v2/everything', params=params)
            response.raise_for_status()
            articles = response.json().get('articles', [])
            api_articles.extend(articles)
            if not articles:
                break
        except requests.exceptions.RequestException as e:
            logging.error(f"API 第 {page} 頁請求失敗: {e}")
            break

# 爬取健康醫療網
def scrape_healthnews():
    articles = []
    try:
        url = "https://www.healthnews.com.tw/"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        for article in soup.find_all('a'):
            title = article.text.strip()
            link = article.get('href', '')
            if not title or not link or "javascript:void(0)" in link:
                continue
            if not link.startswith("http"):
                link = url.rstrip("/") + link
            if any(keyword in title for keyword in relevant_keywords):
                articles.append({
                    'title': title,
                    'url': link,
                    'source': "健康醫療網",
                    'image': "https://via.placeholder.com/300"
                })
    except requests.exceptions.RequestException as e:
        logging.error(f"爬取健康醫療網失敗: {e}")
    return articles

# 爬取 Yahoo 健康專區
def scrape_yahoo_health():
    articles = []
    try:
        url = "https://tw.news.yahoo.com/health"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, allow_redirects=True)

        if "consent.yahoo.com" in response.url:
            logging.warning("被重定向至同意頁面，跳過此頁面。")
            return articles

        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        for article in soup.find_all('a'):
            title = article.text.strip()
            link = article.get('href', '')
            if not title or not link:
                continue
            if not link.startswith("http"):
                link = "https://tw.news.yahoo.com" + link
            if any(keyword in title for keyword in relevant_keywords):
                articles.append({
                    'title': title,
                    'url': link,
                    'source': "Yahoo 健康專區",
                    'image': "https://via.placeholder.com/300"
                })
    except requests.exceptions.RequestException as e:
        logging.error(f"爬取 Yahoo 健康專區失敗: {e}")
    return articles

# 整合文章
def integrate_articles(api_articles, scraped_articles):
    all_articles = []

    for article in api_articles:
        title = article.get('title', '無標題')
        description = article.get('description', '無描述')
        content = article.get('content', '')
        url = article.get('url', '#')
        image = article.get('urlToImage', 'https://via.placeholder.com/300')

        if any(keyword in title or keyword in description or keyword in content for keyword in relevant_keywords):
            all_articles.append({
                'title': title,
                'description': description,
                'url': url,
                'source': "NewsAPI",
                'image': image
            })

    seen_titles = set(article['title'] for article in all_articles)
    for article in scraped_articles:
        if article['title'] not in seen_titles:
            all_articles.append({
                'title': article['title'],
                'description': '此新聞來自爬蟲，無詳細描述。',
                'url': article['url'],
                'source': article['source'],
                'image': article['image']
            })

    return all_articles

# 情感分析
def analyze_sentiments(articles):
    for article in articles:
        if re.search(r'[\u4e00-\u9fa5]', article['title']):
            s = SnowNLP(article['title'])
            sentiment_score = s.sentiments
        else:
            sentiment_score = 0.5

        if sentiment_score > 0.6:
            article['sentiment'] = '😊'
        elif sentiment_score < 0.4:
            article['sentiment'] = '😢'
        else:
            article['sentiment'] = '😐'
    return articles

# 儲存為 HTML
def save_to_html(articles, file_name):
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    html_template = f"""
    <!DOCTYPE html>
    <html lang="zh-Hant">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>新聞整理</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            .news-card img {{ max-height: 150px; object-fit: cover; }}
            .news-card {{ margin-bottom: 20px; }}
        </style>
    </head>
    <body>
        <header class="text-white p-3 mb-4" style="background-color: rgb(26, 120, 106);">
            <div class="container">
                <h1>保健相關即時新聞</h1>
            </div>
        </header>
        <div class="container">
            <div class="row">
    """

    for article in articles:
        html_template += f"""
            <div class="col-md-4 news-card">
                <div class="card">
                    <img src="{article['image']}" class="card-img-top" alt="新聞圖片">
                    <div class="card-body">
                        <h5 class="card-title"><a href="{article['url']}" target="_blank">{article['title']}</a></h5>
                        <p class="card-text">{article['description']}</p>
                        <p class="text-muted">來源: {article['source']}</p>
                        <p class="text-muted">情感分析: {article['sentiment']}</p>
                    </div>
                </div>
            </div>
        """

    html_template += f"""
            </div>
        </div>
        <footer class="bg-light text-center py-3">
            <p>更新時間: {current_time}</p>
        </footer>
    </body>
    </html>
    """

    with open(file_name, 'w', encoding='utf-8') as f:
        f.write(html_template)

# 儲存為 JSON
def save_to_json(articles, file_name):
    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump(articles, f, ensure_ascii=False, indent=4)

# 主程序
fetch_api_articles()
healthnews_articles = scrape_healthnews()
yahoo_articles = scrape_yahoo_health()
all_articles = integrate_articles(api_articles, healthnews_articles + yahoo_articles)
analyzed_articles = analyze_sentiments(all_articles)

save_to_html(analyzed_articles, 'news.html')
save_to_json(analyzed_articles, 'news.json')

print(f"已匯出 {len(analyzed_articles)} 篇新聞至 news.html 和 news.json")