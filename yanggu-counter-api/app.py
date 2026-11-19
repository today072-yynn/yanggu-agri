import os
import json
from datetime import datetime, timezone, timedelta
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # GitHub Pages 도메인에서의 접속 허용

DATA_FILE = 'visitor_log.json'

def get_kst_today():
    kst = timezone(timedelta(hours=9))
    return datetime.now(kst).strftime('%Y-%m-%d')

def load_data():
    if not os.path.exists(DATA_FILE):
        return {"total": 0, "daily": {}}
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

@app.route('/hit', methods=['GET'])
def hit_counter():
    today = get_kst_today()
    data = load_data()
    
    # 무조건 1씩 증가 (중복 체크 없음)
    data["total"] += 1
    data["daily"][today] = data["daily"].get(today, 0) + 1
    
    save_data(data)
    
    return jsonify({
        "today": data["daily"][today],
        "total": data["total"]
    })

@app.route('/logs', methods=['GET'])
def view_logs():
    # 날짜별 누적 기록 전체를 확인하고 싶을 때 접속하는 주소
    return jsonify(load_data())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)