from flask import Flask, jsonify
import os
import json

app = Flask(__name__)

# ファイルパス
BUFFER_FILE = "/app/shared/Buffer.json"

# バッファの内容を返すAPIエンドポイント
# http://127.0.0.1:5001/prediction
@app.route('/prediction', methods=['GET'])
def get_prediction():
    if not os.path.exists(BUFFER_FILE):
        return jsonify({"error": "Buffer file not found"}), 404
    
    with open(BUFFER_FILE, 'r') as f:
        data = json.load(f)
    
    if not data:
        return jsonify({"error": "No data available"}), 404
    
    # 最新のデータを返す
    latest_data = data[-1]
    return jsonify(latest_data)

if __name__ == '__main__':
    app.run(debug=True)
