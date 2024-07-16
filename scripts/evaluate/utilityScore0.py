import pandas as pd
import numpy as np
import sys
from sklearn.metrics import mean_absolute_error
from tqdm import tqdm

def load_data(file1, file2):
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)
    return df1, df2

def calculate_mae(bincount1, bincount2):
    # MAEを計算
    mae = mean_absolute_error(bincount1, bincount2)
    # MAEを0から1の範囲に正規化
    normalized_mae = mae / (np.max(bincount1) - np.min(bincount1))
    return normalized_mae

def numpy_crosstab(index, columns, unique_index, unique_columns):
    index_map = {value: idx for idx, value in enumerate(unique_index)}
    columns_map = {value: idx for idx, value in enumerate(unique_columns)}
    crosstab_result = np.zeros((len(unique_index), len(unique_columns)), dtype=int)
    for idx, col in zip(index, columns):
        row_idx = index_map.get(idx, -1)
        col_idx = columns_map.get(col, -1)
        if row_idx != -1 and col_idx != -1:
            crosstab_result[row_idx, col_idx] += 1
    return crosstab_result

def find_max_mae_and_columns(file1, file2):
    df1, df2 = load_data(file1, file2)
    columns = list(set(df1.columns) & set(df2.columns))  # 共通カラムのみ考慮
    max_mae = -1
    max_mae_columns = None
    
    total_combinations = len(columns) * (len(columns) - 1)  # 自己ペアは除外
    progress_bar = tqdm(total=total_combinations, desc="Processing")

    for col1 in columns:
        for col2 in columns:
            if col1 != col2:
                unique_index = np.union1d(df1[col1].unique(), df2[col1].unique())
                unique_columns = np.union1d(df1[col2].unique(), df2[col2].unique())
                ct1 = numpy_crosstab(df1[col1], df1[col2], unique_index, unique_columns)
                ct2 = numpy_crosstab(df2[col1], df2[col2], unique_index, unique_columns)
                mae = calculate_mae(ct1.flatten(), ct2.flatten())
                progress_bar.update(1)  # プログレスバーを更新
                if mae > max_mae:
                    max_mae = mae
                    max_mae_columns = (col1, col2)

    progress_bar.close()
    return max_mae, max_mae_columns

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python utilityScore0.py <filename1> <filename2>")
        sys.exit(1)

    file1 = sys.argv[1]
    file2 = sys.argv[2]
    max_mae, max_mae_columns = find_max_mae_and_columns(file1, file2)
    us = "{:.3f}".format((1-max_mae)*100)
    print(f"Max Mean Absolute Error: {max_mae}")
    print(f"Columns with max MAE: {max_mae_columns}")
    print(f"Utility Score: {us}")
