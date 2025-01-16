from flask import Flask, render_template, request
import matplotlib.pyplot as plt
import io
import base64
import pandas as pd
import os  # 確保 os 模組被導入

app = Flask(__name__)

# 儲存數據的 CSV 檔案
DATA_FILE = 'health_data.csv'

# 生成健康數據圖表的函數
def generate_chart():
    try:
        # 讀取 CSV 檔案
        if os.path.exists(DATA_FILE):
            data = pd.read_csv(DATA_FILE)
        else:
            data = pd.DataFrame(columns=["date", "weight", "systolic", "diastolic", "heart_rate"])
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return None

    if data.empty:
        return None

    # 確保 'date' 欄位是 datetime 格式
    data['date'] = pd.to_datetime(data['date'])

    # 排序日期，確保數據是按照時間順序顯示
    data = data.sort_values('date')

    # 繪製圖表
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(data['date'], data['weight'], label="體重 (kg)", color='blue', linestyle='-', marker='o')
    ax.plot(data['date'], data['systolic'], label="收縮壓 (mmHg)", color='red', linestyle='-', marker='x')
    ax.plot(data['date'], data['diastolic'], label="舒張壓 (mmHg)", color='green', linestyle='-', marker='s')
    ax.plot(data['date'], data['heart_rate'], label="心率 (bpm)", color='purple', linestyle='-', marker='^')

    ax.set_xlabel('日期')
    ax.set_ylabel('數值')
    ax.set_title('健康數據走勢圖')
    ax.legend()

    plt.xticks(rotation=45)
    plt.tight_layout()

    # 儲存圖表為圖片並轉換為 base64 編碼
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    chart_url = base64.b64encode(img.getvalue()).decode('utf-8')

    return chart_url

@app.route('/', methods=['GET', 'POST'])
def index():
    chart_url = None
    error_message = None
    if request.method == 'POST':
        try:
            date = request.form['date']
            weight = request.form['weight']
            systolic = request.form['systolic']
            diastolic = request.form['diastolic']
            heart_rate = request.form['heart_rate']

            if not date or not weight or not systolic or not diastolic or not heart_rate:
                raise ValueError("所有欄位都必須填寫！")

            # 讀取現有資料並儲存新資料
            if os.path.exists(DATA_FILE):
                data = pd.read_csv(DATA_FILE)
            else:
                data = pd.DataFrame(columns=["date", "weight", "systolic", "diastolic", "heart_rate"])

            new_data = pd.DataFrame({
                "date": [date],
                "weight": [weight],
                "systolic": [systolic],
                "diastolic": [diastolic],
                "heart_rate": [heart_rate]
            })
            data = pd.concat([data, new_data], ignore_index=True)
            data.to_csv(DATA_FILE, index=False)

            # 生成更新後的圖表
            chart_url = generate_chart()
        except Exception as e:
            error_message = f"發生錯誤: {e}"

    return render_template('health_analysis.html', chart_url=chart_url, error_message=error_message)


@app.route('/health_analysis')
def health_analysis():
    chart_url = generate_chart()
    error_message = None if chart_url else "沒有足夠的數據生成圖表。"
    return render_template('health_analysis.html', chart_url=chart_url, error_message=error_message)



if __name__ == '__main__':
    app.run(debug=True)
