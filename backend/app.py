from flask import Flask, jsonify, request
import os
import json
import mysql.connector

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

# Raspiから送られてきたデータをDBに格納するエンドポイント
# http://127.0.0.1:5001/insert
@app.route('/insert', methods=['POST'])
def insert_scanned_data():
    connection = mysql.connector.connect(
        host="mysql",
        user="project-e",
        password="project-e",
        database="ble_db",
        port=3306
    )
    if request.method == "POST":
        recieve_json = str(request.get_data())

        # 受けとったpostデータを整形
        recieve_json = recieve_json.split("'")[1]

        #JSON形式の変数
        json_data = json.loads(recieve_json)
        time = json_data.get('time')
        ble_data = json_data.get('ble_data')
        
        query = "INSERT INTO ble_data (timestamp, other_data) VALUES (%s, %s)"
        values = (time, json.dumps(ble_data))  # JSON型に変換して挿入
        
        cursor = connection.cursor()
        try:
            cursor.execute(query, values)
            connection.commit()
            return jsonify({"message": "Data inserted successfully"}), 201

        except mysql.connector.Error as err:
            print(f"エラー：{err}")
            return jsonify({"error": f"MySQL Error: {err}"}), 500
        except Exception as e:
            print(f"General Error: {e}")
            return jsonify({"error": f"General Error: {e}"}), 500
        
        finally:
            cursor.close()
            connection.close()
            
if __name__ == '__main__':
    app.run(debug=True)
