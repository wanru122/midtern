from flask import Flask, render_template, jsonify,request,abort
from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage, TextSendMessage, PostbackEvent, TemplateSendMessage, ButtonsTemplate, MessageTemplateAction
import datetime
import requests


app = Flask(__name__)

# LINE Channel Access Token 和 Channel Secret
LINE_CHANNEL_ACCESS_TOKEN = 'uoiAEyTtX6TC0mHqQRvv7wEDJy5EZjMA7pZXN4ScLvCQZjwkXZ8X+n69UmMg0yzPS6X36bTXSou5SWGopYYx9106Ilzf+Toj/HwRz8Gu5WAcKfVBFzFy87+nGjOEsx85BfsY/PXTpmJm0AfH0ioksAdB04t89/1O/w1cDnyilFU='
LINE_CHANNEL_SECRET = '4a9c66a0204e7f38ae1c204376c7da2d'

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# 健康小知識資料
health_tips = [
    "每天喝足8杯水，保持身體水分。",
    "每天步行至少30分鐘，有助於心血管健康。",
    "減少攝入加工食品，選擇天然食材。",
    "良好的睡眠習慣可以提升免疫力。",
    "多吃富含纖維的食物，如水果、蔬菜和全穀物。",
    "定期進行體育運動，增強身體免疫力。",
    "避免長時間坐著，記得每隔一段時間站起來活動。",
    "每天保持足夠的睡眠，有助於提高工作效率。",
    "減少壓力，練習深呼吸、冥想等放鬆技巧。",
    "每天攝取足夠的維生素D，對骨骼健康非常重要。",
    "保持心理健康，與朋友和家人保持聯繫，互相支持。",
    "每週進行至少150分鐘的中等強度運動。",
    "適量飲酒，避免過量，對健康更有益。",
    "定期體檢，及早發現健康問題，做到早預防、早治療。",
    "少吃鹽，多食用富含鉀的食物，幫助控制血壓。",
    "合理搭配膳食，三餐均衡，營養充足。",
    "戒煙，遠離香煙和二手煙，對身體有顯著的健康益處。",
    "適當增加Omega-3脂肪酸的攝入，有助於大腦和心臟健康。",
    "保持良好的姿勢，避免長時間低頭或駝背。",
    "盡量避免過度使用電子產品，給眼睛適當休息，預防視力疲勞。",
    "多吃含有抗氧化劑的食物，如莓果、綠茶和深色蔬菜，有助於延緩衰老。"
]

# 設置Webhook的路由
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except Exception as e:
        print("Error:", e)
        abort(400)
    return 'OK'

# 當接收到訊息時的回應邏輯
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text.lower()

    # 假設用戶的訊息是查詢每日健康小知識
    if "每日健康小知識" in user_message:
        today = datetime.date.today()
        tip = health_tips[today.toordinal() % len(health_tips)]
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=tip)
        )
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="請輸入 '每日健康小知識' 來查看今天的健康小知識。")
        )

# 生成包含按鈕的消息
@app.route('/send_health_tip_button', methods=['GET'])
def send_health_tip_button():
    buttons_template = ButtonsTemplate(
        title="健康小知識",
        text="按下按鈕查看每日健康小知識",
        actions=[
            MessageTemplateAction(
                label="每日健康小知識",
                text="每日健康小知識"
            )
        ]
    )
    template_message = TemplateSendMessage(
        alt_text="健康小知識按鈕",
        template=buttons_template
    )
    # 在這裡發送包含按鈕的消息
    user_id = 'user_line_id'  # 替換成目標用戶的LINE ID
    line_bot_api.push_message(user_id, template_message)
    return "已發送"

if __name__ == '__main__':
    app.run(debug=True)
