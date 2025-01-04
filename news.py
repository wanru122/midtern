import requests
from dotenv import load_dotenv
import os

load_dotenv()

apikey = os.getenv("API_KEY")

params = {
    'q': '疾病',
    'language': 'zh',
    'from': '2024-12-15',
    'apiKey': apikey
}

web = requests.get('https://newsapi.org/v2/everything', params=params)

if web.status_code == 200:
    #json格式轉字典，提取articles的列表，沒有傳回空列表
    articles = web.json().get('articles', [])


    with open('news.html', 'w+', encoding='utf-8') as f:
        f.write('''
        <html>
        <head>
            <title>疾病新聞</title>
            <link rel="stylesheet" href="liang.css">
        </head>
        <body>
            <header>
                <img src="image/logo.jpg" class="logo">
                <nav>
                <a href="index.html" ><h3>首頁</h3></a>
                <a href="健康分析工具/bmi/submit.html"><h3>健康分析工具</h3></a>
                <a href="cb.html"><h3>Chat Bot</h3></a>
                <a href="test.html"><h3>百萬小學堂</h3></a>
                <a href="index.html#email"><h3>聯絡我們</h3></a>
                </nav>
                </header>
            <div class="news-container">
        ''')

        for article in articles:
            title = article.get('title', '無標題')
            author = article.get('author', '無作者')
            description = article.get('description', '無描述')
            url = article.get('url', '#')
            
            #點標題跳到原網址，target="_blank"新分頁
            f.write(f'''
                <div class="news-card">
                    <h2><a href="{url}" target="_blank">{title}</a></h2>
                    <p>作者: {author}
                    <p>{description}
                </div>
            ''')

        # 結束 HTML
        f.write('''
            </div>
                <div class="footer2">
                <p>保健巴拉拉. 為您服務</p>
                </div>
        </body>
        </html>
        ''')
else:
    print('無法獲取新聞數據:', web.status_code)
