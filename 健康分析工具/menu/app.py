from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)

# 設置 CORS，允許來自特定來源的請求
CORS(app, resources={r"/*": {"origins": ["http://127.0.0.1:3000", "http://127.0.0.1:3002"]}})

# 設定 Azure OpenAI API 密鑰和端點
azure_api_key = '' 
endpoint_url = ""

@app.route('/get_advice', methods=['POST'])
def get_advice():
    try:
        # 獲取前端發送的用戶資料
        data = request.json
        print(f"收到資料: {data}")  # 日誌打印收到的資料

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

        # 構建用於請求的提示語
        prompt = (
        f"根據以下資訊：BMI={bmi}, BMR={bmr}, 飲食習慣={diet}, 運動習慣={exercise}, 健康目標={goal}，"
        f"請設計一份個性化的一日三餐建議，需包含每餐的食材、份量與建議的卡路里攝取量，並提供一餐與餐之間的加餐建議。"
        f"同時，根據當天的餐飲計劃（{meal_plan}）設計一日的運動建議，包括運動種類、時間安排、強度要求及目標，"
        f"確保餐飲與運動計劃相互配合，幫助達成健康目標。限950字內。"
    )


        # 向 Azure OpenAI API 發送請求
        headers = {
            'Content-Type': 'application/json',
            'api-key': azure_api_key
        }
        body = {
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 950,  # 增加最大 tokens
            "temperature": 0.7
        }

        response = requests.post(endpoint_url, headers=headers, json=body)
        response.raise_for_status()  # 檢查請求是否成功
        response_data = response.json()

        # 取得 AI 返回的建議
        advice = response_data['choices'][0]['message']['content'].strip()

        # 返回給前端顯示
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