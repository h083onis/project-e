import pandas as pd

# 特徴量を抽出する関数
def extract_features(df):
    thresholds = [-60, -70, -80, -90, -100]

    # ユニークアドレス数と総数を計算
    unique_address_counts = df.groupby(df.index)['address'].nunique()
    total_counts = df.groupby(df.index)['address'].count()
    unique_ratio = unique_address_counts / total_counts

    # 結果を格納する辞書
    features = {
        'unique_address_count': unique_address_counts,
        'total_count': total_counts,
        'unique_ratio_Tsec': unique_ratio
    }

    # RSSI閾値ごとの計算
    for threshold in thresholds:
        df_threshold = df[df['rssi'] > threshold]
        unique_address_counts_thr = df_threshold.groupby(df_threshold.index)['address'].nunique()
        total_counts_thr = df_threshold.groupby(df_threshold.index)['address'].count()
        unique_ratio_thr = unique_address_counts_thr / total_counts_thr

        # 特徴量に追加
        features[f'unique_address_count_over{threshold}'] = unique_address_counts_thr
        features[f'total_count_over{threshold}'] = total_counts_thr
        features[f'unique_ratio_Tsec_over{threshold}'] = unique_ratio_thr

    # データフレームに変換し、欠損値を0で補完
    feature_df = pd.DataFrame(features)
    feature_df.fillna(0.0, inplace=True)

    # display(feature_df)
    return feature_df
