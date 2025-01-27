import time
import mysql.connector
import congestion_model
import pytz
from datetime import datetime, timedelta


# 予測結果を保存するプログラム
def pred_and_save():
    # 予測とデータベース保存処理を実行
    JP_time = datetime.now(pytz.timezone('Asia/Tokyo')).replace(tzinfo=None)
    timestamp = JP_time.strftime('%Y-%m-%d %H:%M:%S.%f')
    prediction = congestion_model.realtime_pred("./best_catb_model.cbm", timestamp)

    print({"timestamp": timestamp, "prediction": prediction})

    try:
        connection = mysql.connector.connect(
            host="mysql",
            user="project-e",
            password="project-e",
            database="ble_db",
            port=3306
        )
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO prediction_table (timestamp, prediction) VALUES (%s, %s)",
            (timestamp, prediction)
        )
        connection.commit()
        print("予測結果を保存しました。")
    except mysql.connector.Error as err:
        print(f"エラー: {err}")
    finally:
        if connection:
            cursor.close()
            connection.close()

# 
def pred_minutely():

    now = datetime.now()
    next_run_time = now.replace(second=0, microsecond=0) + timedelta(minutes=1)

    # 最初の予測
    pred_and_save()

    # 次回以降の予測
    while True:
        if datetime.now() >= next_run_time:
            pred_and_save()
            next_run_time += timedelta(minutes=1)

if __name__ == '__main__':
    pred_minutely()
