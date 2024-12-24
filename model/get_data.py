import mysql.connector
from datetime import datetime, timedelta
import pytz
import json
import pandas as pd

def get_ble_data(current_time):
    connection = mysql.connector.connect(
        host="mysql",
        user="project-e",
        password="project-e",
        database="ble_db",
        port=3306
    )
    try:
        with connection.cursor(dictionary=True) as cursor:
            # 秒以下を0にする
            current_time = datetime.strptime(current_time, '%Y-%m-%d %H:%M:%S.%f')
            modified_time = current_time.replace(second=0, microsecond=0)
            minus_one_minute = modified_time - timedelta(minutes=1)
            # print(modified_time)
            # print(minus_one_minute)
            # dbから現在時刻の1分前台のデータを取得
            # query = f"""
            # SELECT * FROM ble_data
            # WHERE timestamp >= '{minus_one_minute}'
            # AND timestamp < '{modified_time}';
            # """

            #仮sql 
            query = """
            SELECT * FROM ble_data
            WHERE timestamp >= '2024-11-01 11:57:00'
            AND timestamp < '2024-11-01 11:58:00';
            """
            cursor.execute(query)  # 1分前台のデータを取得
            rows = cursor.fetchall()

        # 取得したデータを整形
        if not rows:
            return pd.DataFrame()  # データがない場合は空のDataFrameを返す

        # 各行を展開してDataFrameに変換
        expanded_rows = []
        for row in rows:
            # JSON文字列をリストにパース
            devices = json.loads(row["other_data"])
            for device in devices:
                expanded_rows.append({
                    "timestamp": row["timestamp"], 
                    "address": device["address"], 
                    "rssi": device["rssi"]
                })

        # DataFrameに変換
        df = pd.DataFrame(expanded_rows)
        # タイムスタンプをdatetime型に変換
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        # インデックスをタイムスタンプに設定
        df.set_index('timestamp', inplace=True)

        return df

    finally:
        cursor.close()
        connection.close()