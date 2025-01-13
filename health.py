from flask import Flask, request, jsonify
from flask_mail import Mail, Message
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # 解決跨域請求問題

# 設定郵件伺服器
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'c112156121@nkust.edu.tw'
app.config['MAIL_PASSWORD'] = 'tnhi mepz ghjf awnh'

mail = Mail(app)

@app.route('/send_reminder', methods=['POST'])
def send_reminder():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    checkup_date = data.get('checkupDate')
    recommended_checkup = data.get('recommendedCheckup')

    # 傳送提醒郵件
    try:
        msg = Message(f"健康檢查提醒 - {name}",
                      sender=app.config['MAIL_USERNAME'],
                      recipients=[email])
        msg.body = f"您好 {name}，\n您的健康檢查提醒已設定為 {checkup_date}。\n建議檢查項目：{recommended_checkup}。\n請保持健康！"
        mail.send(msg)
        return jsonify({"message": f"提醒信件已成功寄送至 {email}！"})
    except Exception as e:
        return jsonify({"message": f"提醒信件發送失敗：{str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
