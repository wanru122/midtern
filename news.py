import requests
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta
import re


load_dotenv()
apikey = os.getenv("API_KEY")


today = datetime.today()
three_months_ago = today - timedelta(days=90)
default_from_date = three_months_ago.strftime('%Y-%m-%d')
default_to_date = today.strftime('%Y-%m-%d')


relevant_keywords = ["健康", "疾病", "醫療", "醫生", "醫院", "保健", "免疫", "疫苗", "藥物", "治療", "養生", "疫情", "心理"]


query_file = "last_query.txt"
default_query = "健康 OR 疾病 OR 醫療 OR 醫生 OR 醫院 OR 保健 OR 免疫 OR 疫苗"


if os.path.exists(query_file):
    with open(query_file, "r", encoding="utf-8") as file:
        saved_query = file.read().strip()
else:
    saved_query = default_query


user_query = input(f"請輸入關鍵字（按 Enter 使用上次輸入或預設值：'{saved_query}'）：") or saved_query

with open(query_file, "w", encoding="utf-8") as file:
    file.write(user_query)

params = {
    'q': user_query,
    'language': 'zh',
    'from': default_from_date,
    'to': default_to_date,
    'apiKey': apikey,
    'pageSize': 18,  
}

try:
    web = requests.get('https://newsapi.org/v2/everything', params=params)
    web.raise_for_status()
except requests.exceptions.RequestException as e:
    print(f"請求失敗: {e}")
    web = None 


current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

with open('news.html', 'w+', encoding='utf-8') as f:
    f.write(f'''
    <html>
    <head>
        <title>新聞即時搜尋</title>
        <link rel="stylesheet" href="liang.css">
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

    if web and web.status_code == 200:
        articles = web.json().get('articles', [])
        filtered_articles = []

        for article in articles:
            title = article.get('title', '').lower()
            description = article.get('description', '').lower()

            if any(keyword in title or keyword in description for keyword in relevant_keywords):
                filtered_articles.append(article)

        if filtered_articles:
            for article in filtered_articles:
                title = article.get('title', '無標題')
                author = article.get('author', '無作者')
                description = article.get('description', '無描述')
                url = article.get('url', '#')
                image_url = article.get('urlToImage', 'default_image.jpg') 

      
                for keyword in relevant_keywords:
                    description = re.sub(rf'({re.escape(keyword)})', r'<strong>\1</strong>', description, flags=re.IGNORECASE)

                f.write(f'''
                    <div class="news-card">
                        <img src="{image_url}" alt="新聞圖片" style="width: 100%; max-width: 300px;">
                        <h2><a href="{url}" target="_blank">{title}</a></h2>
                        <p>作者: {author}</p> 
                        <p>{description}</p>
                    </div>
                ''')
        else:
            f.write('<h2>未找到符合條件的新聞。</h2>')
    else:
        error_message = f"無法獲取新聞數據，錯誤碼: {web.status_code}" if web else "請檢查您的 API 密鑰或網絡連接。"
        f.write(f'<div class="error"><h2>新聞加載失敗</h2><p>{error_message}</p></div>')


    f.write(f'''
        <div class="back-to-top">
            <a href="#top">回到頂部</a>
        </div>
        <div class="footer2">
            <p>保健巴拉拉. 為您服務</p>
            <p id="current-time"></p>
        </div>

        <script>
            function updateTimeOnLoad() {{
            const now = new Date();
            const formattedTime = now.getFullYear() + '-' +
            String(now.getMonth() + 1).padStart(2, '0') + '-' +
            String(now.getDate()).padStart(2, '0') + ' ' +
            String(now.getHours()).padStart(2, '0') + ':' +
            String(now.getMinutes()).padStart(2, '0') + ':' +
            String(now.getSeconds()).padStart(2, '0');
            document.getElementById('current-time').innerText = '最新更新時間: ' + formattedTime;
    }}
    updateTimeOnLoad();
</script>

    </body>
    </html>
    ''')
