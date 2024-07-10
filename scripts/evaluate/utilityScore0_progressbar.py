import pandas as pd
import numpy as np
import sys
from sklearn.metrics import mean_absolute_error
from tqdm import tqdm

def load_data(file1, file2):
    # CSVファイルをDataFrameとして読み込む
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)
    return df1, df2

def calculate_mae(cross_tab1, cross_tab2):
    # カテゴリごとの頻度をnumpyの配列に変換
    table1 = cross_tab1.to_numpy()
    table2 = cross_tab2.to_numpy()
    
    # MAEを計算
    mae = mean_absolute_error(table1.flatten(), table2.flatten())
    
    # MAEを0から1の範囲に正規化
    normalized_mae = mae / (np.max(table1) - np.min(table1))
    
    return normalized_mae

def find_max_mae_and_columns(file1, file2):
    # データを読み込む
    df1, df2 = load_data(file1, file2)
    
    # カラム名のリストを取得
    columns1 = df1.columns
    columns2 = df2.columns
    
    max_mae = -1
    max_mae_columns = None
    
    # すべての組み合わせに対してクロス集計とMAEの計算を行う
    total_combinations = len(columns1) * len(columns2)
    progress_bar = tqdm(total=total_combinations, desc="Processing")

    for col1 in columns1:
        for col2 in columns2:
            try:
                cross_tab1 = pd.crosstab(df1[col1], df1[col2])
                cross_tab2 = pd.crosstab(df2[col1], df2[col2])
                
                # MAEを計算
                mae = calculate_mae(cross_tab1, cross_tab2)
                
                # 最大のMAEを更新する場合、それとカラム名を記録
                if mae > max_mae:
                    max_mae = mae
                    max_mae_columns = (col1, col2)
            except KeyError as e:
                print(f"Skipping columns {col1} and {col2} due to error: {e}")
            finally:
                progress_bar.update(1)
    
    progress_bar.close()
    return max_mae, max_mae_columns

# メインの実行部分
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: python utilityScore0.py <filename1> <filename2>")
        sys.exit(1)

    # 2つのCSVファイルの読み込み
    file1 = sys.argv[1]
    file2 = sys.argv[2]
    
    # 最大のMAEとそのときのカラム名を取得
    max_mae, max_mae_columns = find_max_mae_and_columns(file1, file2)
    
    us = "{:.3f}".format((1-max_mae)*100)
    # 結果の出力
    print(f"Max Mean Absolute Error: {max_mae}")
    print(f"Columns with max MAE: {max_mae_columns}")
    print(f"Utility Score: {us}")
