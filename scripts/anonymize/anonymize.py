"""

匿名化プログラムのサンプルです。

"""

import sys
import csv
import os
import random
import argparse

import pandas as pd
import numpy as np


# 匿名化処理を書いた関数
# ここを変更すると匿名化の方法を変えられる
# pandasのデータフレームを入力することを想定
def anonymize(df):
    anonymized_df = df.copy()

    # 加工処理の適用
    print("1. Name列の削除")
    if 'Name' in anonymized_df.columns:
        # 'Name'列は使わないので、(もしあれば)削除する
        anonymized_df.drop('Name', axis=1, inplace=True)

    print("2. 最初の2属性:GenderとAgeが一致しているユーザの中で、映画の評価(5列目以降すべて)をシャッフル")
    anonymized_df = group_shuffle(anonymized_df,
        anonymized_df.columns.tolist()[0:2], anonymized_df.columns.tolist()[4:])
    print("3. ランダムに選んだ1列で、値を1000回入れ替え")
    anonymized_df = random_shuffle(anonymized_df, rep=1000)

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
    anonymized_df = df.copy()

    # Iterate over each group
    for name, group_data in anonymized_df.groupby(groups):
        for target in targets:
            # Shuffle the target column within the current group
            shuffled_values = np.random.permutation(group_data[target].values)
            anonymized_df.loc[group_data.index, target] = shuffled_values

    return anonymized_df


# メインの実行部分
if __name__ == "__main__":
    # コマンドライン引数を読みこむ
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('org_csv', help='匿名化したいcsvファイル(e.g., B32_3.csv)')
    parser.add_argument('ano_csv', help='匿名化ファイルにつけたい名前(e.g., C32_3.csv)')
    # 引数を増やしたい時は
    # parser.add_argument('arg3')
    args = parser.parse_args()

    # CSVファイルパスの読み込み
    input_file_path = args.org_csv
    output_file_path = args.ano_csv

    # CSVファイルをpandasのデータフレームとして読み込む
    # 不正なファイルパスを指定するとここで強制終了
    Bi = pd.read_csv(input_file_path)

    # 匿名化処理
    Ci = anonymize(Bi)

    # 結果の出力
    Ci.to_csv(output_file_path, index=False)
