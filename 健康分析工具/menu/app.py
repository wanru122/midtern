from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv
from datetime import datetime

# 初始化應用與環境變數
load_dotenv()
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# 環境變數設定
AZURE_API_KEY = os.getenv('AZURE_API_KEY')
AZURE_ENDPOINT_URL = os.getenv('AZURE_ENDPOINT_URL')

# 天氣API設定（以OpenWeatherMap為例）
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')  # 需要註冊獲取API密鑰
WEATHER_API_URL = 'http://api.openweathermap.org/data/2.5/weather'

# 使用字典作為簡單的記憶體快取
cache = {}

@app.route('/get_advice', methods=['POST'])
def get_advice():
    try:
        # 獲取前端發送的用戶資料
        data = request.json
        print(f"收到資料: {data}")

        # 確保所有必要的資料都已提供
        required_fields = ['bmi', 'bmr', 'diet', 'exercise', 'goal', 'meal_plan', 'exercise_plan']
        if not all(field in data for field in required_fields):
            return jsonify({"error": "請填寫所有欄位"}), 400

        # 提取用戶資料
        bmi = data['bmi']
        bmr = data['bmr']
        diet = data['diet']
        exercise = data['exercise']
        goal = data['goal']
        meal_plan = data['meal_plan']
        exercise_plan = data['exercise_plan']

        # 組建提示語
        prompt = (
            f"根據以下資訊：BMI={bmi}, BMR={bmr}, 飲食習慣={diet}, 運動習慣={exercise}, 健康目標={goal}，"
            f"請設計一份個性化的一日三餐建議，需包含每餐的食材、份量與建議的卡路里攝取量，並提供一餐與餐之間的加餐建議。"
            f"同時，根據當天的餐飲計劃（{meal_plan}）設計一日的運動建議，包括運動種類、時間安排、強度要求及目標，"
            f"確保餐飲與運動計劃相互配合，幫助達成健康目標。限950字內。"
        )

        # 快取檢查
        cache_key = f"{bmi}:{bmr}:{diet}:{exercise}:{goal}:{meal_plan}:{exercise_plan}:{datetime.now().strftime('%Y-%m-%d')}"
        if cache_key in cache:
            print("從快取返回結果")
            return jsonify({"advice": cache[cache_key]})

        # 向 Azure OpenAI API 發送請求
        headers = {
            'Content-Type': 'application/json',
            'api-key': AZURE_API_KEY
        }
        body = {
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 950,
            "temperature": 0.7
        }

        response = requests.post(AZURE_ENDPOINT_URL, headers=headers, json=body)
        response.raise_for_status()
        response_data = response.json()

        # 取得 AI 返回的建議
        advice = response_data['choices'][0]['message']['content'].strip()

        # 儲存至快取
        cache[cache_key] = advice

        # 儲存到日誌文件
        with open("advice_log.txt", "a", encoding="utf-8") as log_file:
            log_file.write(f"{datetime.now()} - Prompt: {prompt}\nAdvice: {advice}\n\n")

        # 返回結果
        return jsonify({"advice": advice})

    except requests.exceptions.RequestException as req_err:
        print(f"請求錯誤: {req_err}")
        return jsonify({"error": "無法連接到 AI 服務，請稍後再試。"}), 500
    except KeyError as key_err:
        print(f"鍵錯誤: {key_err}")
        return jsonify({"error": "伺服器返回的數據格式不正確。"}), 500
    except Exception as e:
        print(f"錯誤: {e}")
        return jsonify({"error": "伺服器發生錯誤，請稍後再試。"}), 500

if __name__ == '__main__':
    app.run(debug=True)
