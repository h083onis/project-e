from flask import Flask, jsonify
import json

app = Flask(__name__)

# バッファファイルから予測結果を取得
def load_from_buffer():
    try:
        with open('buffer.json', 'r') as f:
            data = json.load(f)
        return data.get("prediction")
    except FileNotFoundError:
        return None

# バッファの内容を返すAPIエンドポイント
# http://127.0.0.1:5001/prediction
@app.route('/prediction', methods=['GET'])
def get__prediction():
    prediction = load_from_buffer()
    if prediction is not None:
        return jsonify({'prediction': prediction})
    else:
        return jsonify({'error': 'Prediction not available'}), 503

if __name__ == '__main__':
    app.run(debug=True)
