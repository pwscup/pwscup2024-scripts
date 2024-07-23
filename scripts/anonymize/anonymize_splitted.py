import sys
import csv
import os
import random

import pandas as pd
import numpy as np


# 匿名化処理を書いた関数
# ここを変更すると匿名化の方法を変えられる
# pandasのデータフレームを入力することを想定
def anonymize(df):
    anonymized_df = df.copy()

    # 加工処理の適用
    print("1. Name列の削除")
    if 'Name' in df.columns:
        # 'Name'列は使わないので、(もしあれば)削除する
        anonymized_df.drop('Name', axis=1, inplace=True)

    print("2. 最初の2属性が一致しているユーザの中で、映画の評価をシャッフル")
    anonymized_df = group_shuffle(anonymized_df,
        df.columns.tolist()[0:2], df.columns.tolist()[2:])
    print("3. ランダムな列でシャッフル")
    anonymized_df = random_shuffle(anonymized_df)

    return anonymized_df

def random_shuffle(df, rep=1000):
    # ランダムに選んだ列の中でセルの入れ替え　x 1000回
    anonymized_df = df.copy()
    for _ in range(rep):
        col_name = random.choice(df.columns.tolist())
        users = np.random.choice(np.arange(len(df)), 2, replace=False)
        tmp = anonymized_df.loc[users[0], col_name]
        anonymized_df.loc[users[0], col_name] = anonymized_df.loc[users[1], col_name]
        anonymized_df.loc[users[1], col_name] = tmp

    return anonymized_df

def group_shuffle(df, groups, targets):
    # group列で指定した列の値が同じ行内で、targets列の値をシャッフルする
    # Resulting DataFrame
    result = df.copy()

    # Iterate over each group
    for name, group_data in df.groupby(groups):
        for target in targets:
            # Shuffle the target column within the current group
            shuffled_values = np.random.permutation(group_data[target].values)
            result.loc[group_data.index, target] = shuffled_values

    return result


# メインの実行部分
if __name__ == "__main__":
    # 引数の数が間違っていたら強制終了
    if len(sys.argv) != 3:
            print(f"Usage: python {os.path.basename(__file__)} <filename>")
            sys.exit(1)

    # CSVファイルパスの読み込み
    input_file_path = sys.argv[1]
    output_file_path = sys.argv[2]

    # CSVファイルをpandasのデータフレームとして読み込む
    # 不正なファイルパスを指定するとここで強制終了
    Bi = pd.read_csv(input_file_path)

    # 匿名化処理
    Ci = anonymize(Bi)

    # 結果の出力
    Ci.to_csv(output_file_path, index=False)
