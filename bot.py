from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from flask import Flask, request, abort
import requests
import os

app = Flask(__name__)

# LINE Channel Access Token 和 Channel Secret
LINE_CHANNEL_ACCESS_TOKEN = 'uoiAEyTtX6TC0mHqQRvv7wEDJy5EZjMA7pZXN4ScLvCQZjwkXZ8X+n69UmMg0yzPS6X36bTXSou5SWGopYYx9106Ilzf+Toj/HwRz8Gu5WAcKfVBFzFy87+nGjOEsx85BfsY/PXTpmJm0AfH0ioksAdB04t89/1O/w1cDnyilFU='
LINE_CHANNEL_SECRET = '4a9c66a0204e7f38ae1c204376c7da2d'

# NewsAPI 金鑰
NEWS_API_KEY = 'e8343cd73c3b45559133d0f08a55fa65'

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# 設置Webhook的路由
@app.route("/callback", methods=['POST'])
def callback():
    # 確保是LINE的Webhook
    signature = request.headers['X-Line-Signature']
    
    # 取得LINE傳送的事件
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except Exception as e:
        print("Error:", e)
        abort(400)
    return 'OK'

# 根據用戶的關鍵詞查詢最新的新聞
def get_news(query):
    url = f'https://newsapi.org/v2/everything?q={query}&apiKey={NEWS_API_KEY}&language=zh'
    response = requests.get(url)
    news_data = response.json()

    if news_data.get('status') == 'ok' and news_data.get('articles'):
        articles = news_data['articles'][:5]  # 取前五篇新聞
        news_list = []
        for article in articles:
            title = article['title']
            url = article['url']
            news_list.append(f'{title}\n{url}')
        return '\n\n'.join(news_list)
    else:
        return "抱歉，無法找到相關的新聞。請稍後再試。"

# 設置當接收到訊息時的回應邏輯
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text.lower()

    # 假設用戶的訊息是查詢某個領域的新聞
    response = get_news(user_message)

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=response)
    )

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
