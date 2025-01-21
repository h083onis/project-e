import time
import os
import json
import mysql.connector
import congestion_model
import pytz
from datetime import datetime, timedelta

def save_prediction_to_db():
    """
    予測結果を保存するプログラム
    :param prediction: 予測値 (float)
    :param timestamp: 任意の時刻 (datetime形式), Noneの場合は現在時刻が使われる
    """
    while True:
         # 次の実行時刻を計算
        next_run_time = datetime.now()
        # 日本時間取得
        JP_time = datetime.now(pytz.timezone('Asia/Tokyo'))
        # タイムゾーンを削除
        JP_time_without_tz = JP_time.replace(tzinfo=None)
        # オフセットなしで表示
        timestamp = JP_time_without_tz.strftime('%Y-%m-%d %H:%M:%S.%f')
        # CatBoostモデルのファイルパス
        model_path = "./best_catb_model.cbm"
        # リアルタイム推定を開始
        prediction = congestion_model.real_time_estimation(model_path, timestamp)

        try:
            connection = mysql.connector.connect(
                host="mysql",
                user="project-e",
                password="project-e",
                database="ble_db",
                port=3306
            )
            cursor = connection.cursor()

            # データ挿入
            sql = "INSERT INTO prediction_table (timestamp, prediction) VALUES (%s, %s)"
            cursor.execute(sql, (timestamp, prediction))

            connection.commit()
            print("予測結果を保存しました。")

        except mysql.connector.Error as err:
            print(f"エラー: {err}")
        finally:
            if connection:
                cursor.close()
                connection.close()

        # 次の実行時刻を計算
        next_run_time += timedelta(minutes=1)

        # 次の実行時刻まで待機
        now = datetime.now()
        sleep_duration = (next_run_time - now).total_seconds()
        if sleep_duration > 0:
            time.sleep(sleep_duration)


if __name__ == '__main__':
    save_prediction_to_db()
