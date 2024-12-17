import pandas as pd
import time
import get_data
import feature_extract
from catboost import CatBoostRegressor

# リアルタイム人数推定
def real_time_people_estimation(model_path):
    # モデルのロード
    model = CatBoostRegressor()
    model.load_model(model_path)

    print("リアルタイム人数推定を開始します...")

    try:
        while True:
            # 新しいBLEデータをシミュレート
            new_data = get_data.get_ble_data()

            # new_dataが空の場合にエラーを返す
            if new_data.empty:
                raise ValueError("スキャンしたBLEのデータがありません")

            print(new_data)
            features = feature_extract.extract_features(new_data)
            # 推定を行う（最新の特徴量データをモデルに入力）
            if not features.empty:
                prediction = model.predict(features.iloc[-1:])
                predicted_people = int(round(prediction[0]))  # 予測人数を整数に丸める
                print(f"{pd.Timestamp.now()}: 推定人数 = {predicted_people}")
            
            # 10秒ごとに更新
            time.sleep(10)

    except KeyboardInterrupt:
        print("\nリアルタイム推定を終了します。")

# 実行
if __name__ == "__main__":
    # CatBoostモデルのファイルパス
    model_path = "./best_catb_model.cbm"
    # リアルタイム推定を開始
    real_time_people_estimation(model_path)