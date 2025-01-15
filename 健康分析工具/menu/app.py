from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
import time

# 初始化應用與環境變數
load_dotenv()
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# 環境變數設定
AZURE_API_KEY = os.getenv('AZURE_API_KEY')
AZURE_ENDPOINT_URL = os.getenv('AZURE_ENDPOINT_URL')

WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')  # 需要註冊獲取API密鑰
WEATHER_API_URL = 'http://api.openweathermap.org/data/2.5/weather'

# 使用字典作為簡單的記憶體快取
cache = {}

# 重試機制函數
def fetch_advice_with_retry(headers, body, max_retries=5):
    retries = 0
    while retries < max_retries:
        try:
            response = requests.post(AZURE_ENDPOINT_URL, headers=headers, json=body)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            retries += 1
            print(f"請求失敗，重試第 {retries} 次...")
            if retries == max_retries:
                raise e
            time.sleep(2 ** retries)  # 指數退避機制

# 天氣查詢函數
def get_weather(city):
    try:
        response = requests.get(WEATHER_API_URL, params={
            'q': city,
            'appid': WEATHER_API_KEY,
            'units': 'metric'
        })
        response.raise_for_status()
        weather_data = response.json()
        return weather_data['weather'][0]['description'], weather_data['main']['temp']
    except Exception as e:
        print(f"天氣查詢錯誤: {e}")
        return "未知", 25  # 默認為晴天和25°C

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
        city = data.get('city', 'Taipei')  # 默認城市為台北

        # 天氣查詢
        weather_description, temperature = get_weather(city)

        # 建立快取金鑰
        cache_key = f"{bmi}:{bmr}:{diet}:{exercise}:{goal}:{meal_plan}:{exercise_plan}:{city}"
        if cache_key in cache:
            cached_data = cache[cache_key]
            if (datetime.now() - cached_data['time']).seconds < 60:  # 限制1分鐘內的頻繁請求
                print("從快取返回結果")
                return jsonify({"advice": cached_data['advice']})

        # 組建提示語
        prompt = (
            f"根據以下資訊：\n"
            f"BMI: {bmi}\n"
            f"BMR: {bmr}\n"
            f"飲食習慣: {diet}\n"
            f"運動習慣: {exercise}\n"
            f"健康目標: {goal}\n\n"
            f"請設計一份個性化的一日三餐建議，需包含以下內容：\n"
            f"  - 每餐的食材\n"
            f"  - 每餐的份量\n"
            f"  - 每餐建議的卡路里攝取量\n"


            f"同時，根據當天的餐飲計劃（{meal_plan}）以及天氣：{weather_description}、溫度：{temperature}°C設計一日的運動建議，需包含以下內容：\n"
            f"  - 運動種類\n"
            f"  - 時間安排\n"
            f"  - 強度要求\n"
            f"並確保餐飲與運動計劃相互配合，幫助達成健康目標。"
            f"900字左右"
        )

        # 向 Azure OpenAI API 發送請求
        headers = {
            'Content-Type': 'application/json',
            'api-key': AZURE_API_KEY
        }
        body = {
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 900,
            "temperature": 0.7
        }

        # 調用重試機制
        response_data = fetch_advice_with_retry(headers, body)

        # 取得 AI 返回的建議
        advice = response_data['choices'][0]['message']['content'].strip()

        # 儲存至快取
        cache[cache_key] = {
            "advice": advice,
            "time": datetime.now()
        }

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