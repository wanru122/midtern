import os
import logging
from dotenv import load_dotenv
from flask import Flask, request, jsonify
import openai
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
# 允許來自 http://127.0.0.1:3000 的所有請求
CORS(app, resources={r"/send_message": {"origins": "http://127.0.0.1:3000"}})

# 配置日誌
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# 加載環境變數
load_dotenv()

# 配置 Azure OpenAI API
OPENAI_ENDPOINT = os.getenv("endpointUrl")
OPENAI_API_KEY = os.getenv("apiKey")


# 初始化 OpenAI 設定
openai.api_base = OPENAI_ENDPOINT
openai.api_key = OPENAI_API_KEY

@app.route("/send_message", methods=["POST", "OPTIONS"])
def send_message():
    if request.method == "OPTIONS":
        # 預檢請求，返回 CORS 標頭
        return jsonify(), 200

    try:
        data = request.get_json()
        user_message = data.get("message", "").strip()

        logger.debug(f"Received user message: {user_message}")

        if not user_message:
            return jsonify({"error": "請輸入有效的訊息"}), 400

        reply = generate_response(user_message)
        return jsonify({"reply": reply})

    except openai.error.OpenAIError as api_error:
        return jsonify({"error": f"OpenAI API 錯誤: {str(api_error)}"}), 500
    except Exception as e:
        return jsonify({"error": f"伺服器錯誤: {str(e)}"}), 500


def generate_response(user_message):
    """
    調用 OpenAI API 並返回回應
    """
    try:
        response = openai.ChatCompletion.create(
            engine="gpt-35-turbo",  # 替換為您的部署名稱
            messages=[{
                "role": "system", 
                "content": "你是一個用繁體中文回答問題的智慧助手，請確保你的回應最多為 50 個字。"
            }, {
                "role": "user", 
                "content": user_message
            }],
            max_tokens=150,
            temperature=0.7,
        )

        # 提取回應內容並限制字數
        reply = response.choices[0].message["content"]
        max_words = 50
        return " ".join(reply.split()[:max_words])
    
    except Exception as e:
        logger.error(f"調用 OpenAI API 錯誤: {str(e)}")
        raise

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)