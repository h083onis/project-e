import mysql.connector
import datetime
import pytz
import json
import pandas as pd

def get_ble_data():
    connection = mysql.connector.connect(
        host="mysql",
        user="project-e",
        password="project-e",
        database="ble_db",
        port=3306
    )
    try:
        with connection.cursor(dictionary=True) as cursor:
            # dbから現在時刻の1分前台のデータを取得
            # query = """
            # SELECT * FROM ble_data
            # WHERE timestamp >= DATE_SUB(DATE_FORMAT(CONVERT_TZ(NOW(), 'UTC', 'Asia/Tokyo'), '%Y-%m-%d %H:%i:00'), INTERVAL 1 MINUTE)
            # AND timestamp < DATE_FORMAT(CONVERT_TZ(NOW(), 'UTC', 'Asia/Tokyo'), '%Y-%m-%d %H:%i:00');
            # """

            #仮sql 
            query = """
            SELECT * FROM ble_data
            WHERE timestamp >= '2024-12-04 12:05:00'
            AND timestamp < '2024-12-04 12:06:00';
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

        # 1分間のデータをまとめる(現状、1分間のデータ1つしかないからコメントアウトしてます)
        # all_data = pd.concat(new_data)

        return df

    finally:
        cursor.close()
        connection.close()