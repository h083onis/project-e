import pandas as pd

# 特徴量を抽出する関数
def extract_features(df):

    thresholds = [-60, -70, -80, -90, -100]

    # データが空なら空の特徴量を返す
    if df.empty:
        return pd.DataFrame([{
            'unique_address_count': 0, 'total_count': 0, 'unique_ratio_Tsec': 0.0,  
            **{f'unique_address_count_over{t}': 0 for t in thresholds},
            **{f'total_count_over{t}': 0 for t in thresholds},
            **{f'unique_ratio_Tsec_over{t}': 0.0 for t in thresholds}  
        }])

    # 特徴量を格納する辞書
    features = {}

    # 全体のユニークアドレス数、総数、ユニーク率を計算
    unique_address_count = df['address'].nunique()
    total_count = len(df)
    unique_ratio = unique_address_count / total_count if total_count > 0 else 0.0

    features['unique_address_count'] = unique_address_count
    features['total_count'] = total_count
    features['unique_ratio_Tsec'] = unique_ratio  

    # RSSI閾値ごとの計算
    for threshold in thresholds:
        df_threshold = df[df['rssi'] > threshold]

        unique_address_count_thr = df_threshold['address'].nunique()
        total_count_thr = len(df_threshold)
        unique_ratio_thr = unique_address_count_thr / total_count_thr if total_count_thr > 0 else 0.0

        # 特徴量を辞書に追加
        features[f'unique_address_count_over{threshold}'] = unique_address_count_thr
        features[f'total_count_over{threshold}'] = total_count_thr
        features[f'unique_ratio_Tsec_over{threshold}'] = unique_ratio_thr  

    # 辞書を1行のデータフレームに変換
    feature_df = pd.DataFrame([features])

    return feature_df
