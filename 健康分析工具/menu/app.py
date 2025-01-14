from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv
import redis
from datetime import datetime

# 初始化應用與環境變數
load_dotenv()
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# 初始化 Redis 快取
cache = redis.StrictRedis(host='localhost', port=6379, decode_responses=True)

# 環境變數設定
AZURE_API_KEY = os.getenv('AZURE_API_KEY')
AZURE_ENDPOINT_URL = os.getenv('AZURE_ENDPOINT_URL')

# 天氣API設定（以OpenWeatherMap為例）
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')  # 需要註冊獲取API密鑰
WEATHER_API_URL = 'http://api.openweathermap.org/data/2.5/weather'

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
        cache_key = f"advice:{bmi}:{bmr}:{diet}:{exercise}:{goal}:{datetime.now().strftime('%Y-%m-%d')}"
        cached_response = cache.get(cache_key)
        if cached_response:
            print("從快取返回結果")
            return jsonify({"advice": cached_response})

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
        cache.set(cache_key, advice, ex=3600)  # 快取 1 小時

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

@app.route('/get_weather_advice', methods=['GET'])
def get_weather_advice():
    city = request.args.get('city', 'Kaohsiung') 
    url = f"{WEATHER_API_URL}?q={city}&appid={WEATHER_API_KEY}&units=metric" 

    try:
        response = requests.get(url)
        response.raise_for_status()  # 確保沒有錯誤
        data = response.json()

        # 提取所需的天氣數據
        temperature = data['main']['temp']
        weather = data['weather'][0]['description']
        humidity = data['main']['humidity']

        # 根據溫度提供運動建議
        if temperature > 30:
            advice = "天氣炎熱，建議避免戶外運動，改為室內運動。"
        elif 20 <= temperature <= 30:
            advice = "天氣適宜，可以進行中等強度的戶外運動。"
        else:
            advice = "天氣較冷，建議穿暖和衣物並進行低強度運動。"

        return jsonify({
            "city": city,
            "temperature": temperature,
            "weather": weather,
            "humidity": humidity,
            "advice": advice
        })
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"無法獲取天氣資料: {str(e)}"}), 500

@app.route('/get_advice_history', methods=['GET'])
def get_advice_history():
    try:
        # 從日誌文件中讀取建議記錄
        if not os.path.exists("advice_log.txt"):
            return jsonify({"history": []})

        with open("advice_log.txt", "r", encoding="utf-8") as log_file:
            logs = log_file.readlines()

        # 將記錄分塊化返回
        history = []
        current_record = {}
        for line in logs:
            if line.startswith("202"):
                if current_record:
                    history.append(current_record)
                current_record = {"timestamp": line.split(" - ")[0], "prompt": line.split("Prompt: ")[1].strip()}
            elif line.startswith("Advice: "):
                current_record["advice"] = line.replace("Advice: ", "").strip()
        if current_record:
            history.append(current_record)

        return jsonify({"history": history})
    except Exception as e:
        print(f"錯誤: {e}")
        return jsonify({"error": "無法讀取歷史記錄。"}), 500

if __name__ == '__main__':
    app.run(debug=True)
