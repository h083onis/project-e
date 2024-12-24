import time
import os
import json
import mysql.connector
import congestion_model
import pytz
from datetime import datetime, timedelta

# バッファファイルを初期化（新しい日付での利用時）
def initialize_buffer():
    with open(BUFFER_FILE, 'w') as f:
        json.dump([], f)  # 空リストで初期化

# バッファファイル名
BUFFER_FILE = '/app/shared/Buffer.json'

def update_buffer():
    # 初期値
    input_value = 1
    current_date = datetime.now().date()  # 今日の日付

    # 初回起動時にファイルを初期化
    if not os.path.exists(BUFFER_FILE):
        initialize_buffer()

    while True:
        # 現在の日付を取得
        new_date = datetime.now().date()

        # 日付が変わった場合はバッファファイルをリセット
        if new_date != current_date:
            current_date = new_date
            initialize_buffer()

        # 日本時間取得
        JP_time = datetime.now( pytz.timezone('Asia/Tokyo'))
        # タイムゾーンを削除
        JP_time_without_tz = JP_time.replace(tzinfo=None)
        # オフセットなしで表示
        timestamp = JP_time_without_tz.strftime('%Y-%m-%d %H:%M:%S.%f')
        # CatBoostモデルのファイルパス
        model_path = "./best_catb_model.cbm"
        # リアルタイム推定を開始
        prediction = congestion_model.real_time_estimation(model_path, timestamp)
        new_data = {"timestamp": timestamp, "prediction": prediction}

        print(new_data)
        # バッファファイルにデータを追記
        with open(BUFFER_FILE, 'r') as f:
            data = json.load(f)

        data.append(new_data)

        with open(BUFFER_FILE, 'w') as f:
            json.dump(data, f, indent=4, default=str)

        # 次の処理まで1分待機
        time.sleep(60)


if __name__ == '__main__':
    update_buffer()
