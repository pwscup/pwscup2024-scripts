import pandas as pd
import numpy as np
import sys
from sklearn.metrics import mean_absolute_error
from tqdm import tqdm
from concurrent.futures import ProcessPoolExecutor, as_completed

def load_data(file1, file2):
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)
    return df1, df2


def find_max_mae_and_columns(file1, file2, parallel=1):
    df1, df2 = load_data(file1, file2)
    columns = list(set(df1.columns) & set(df2.columns))  # 共通カラムのみ考慮

    # 除外するカラム名のペアを定義
    excluded_columns = {'Name', 'Gender', 'Age', 'Occupation', 'ZIP-code'}

     # カラム名のペアを生成し、除外するペアをフィルタリング
    column_pairs = set()
    for col1 in columns:
        for col2 in columns:
            if col1 != col2 and not (col1 in excluded_columns and col2 in excluded_columns):
                pair = tuple(sorted((col1, col2)))
                column_pairs.add(pair)

    err_dic = {}
    for pair in column_pairs:
      c1,c2 = pair
      column_pair = [c1, c2]
      freq1 = df1.value_counts(column_pair)
      freq2 = df2.value_counts(column_pair)
      err_dic[",".join(column_pair)] = (freq1 - freq2).abs().mean() / (freq1.max() - freq1.min())
      ## 何かで規格化する必要がある

    return max(err_dic.items(), key=lambda x: x[1])


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python utilityScore0.py <filename1> <filename2> [--parallel N]")
        sys.exit(1)

    file1 = sys.argv[1]
    file2 = sys.argv[2]
    parallel = 1  # デフォルトはシングルスレッド
    if len(sys.argv) == 5 and sys.argv[3] == '--parallel':
        parallel = int(sys.argv[4])

    max_mae_columns, max_mae = find_max_mae_and_columns(file1, file2, parallel)
    us = "{:.3f}".format((1-max_mae)*100)
    print(f"Max Mean Absolute Error: {max_mae}")
    print(f"Columns with max MAE: {max_mae_columns}")
    print(f"Utility Score: {us}")

