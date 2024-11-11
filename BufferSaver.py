import joblib
import numpy as np
import time
import json
from datetime import datetime, timedelta

# モデルの読み込み
model = joblib.load('model.pkl')

# バッファファイル名
BUFFER_FILE = 'buffer.json'

# 保存する最大データ数と古いデータの削除時間
EXPIRE_DURATION = timedelta(hours=1)  # 古いデータの削除時間（例：1時間）

# バッファにデータを追加
def save_to_buffer(prediction):
    timestamp = datetime.now().isoformat()
    new_data = {"timestamp": timestamp, "prediction": prediction}
    
    try:
        with open(BUFFER_FILE, 'r') as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = []
    
    # 新しいデータを追加し、古いデータを削除（現状過去１時間のデータを保持）
    data.append(new_data)
    data = [entry for entry in data if datetime.fromisoformat(entry["timestamp"]) >= datetime.now() - EXPIRE_DURATION]
    
    with open(BUFFER_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def update_buffer():
    while True:
        ble_data = np.random.rand(1, 256)  # ダミーの256次元データ
        prediction = model.predict(ble_data)  # 予測を実行
        save_to_buffer(prediction.tolist())  # JSONファイルに保存
        time.sleep(60)  # 1分ごとに更新

if __name__ == '__main__':
    update_buffer()
