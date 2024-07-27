"""

匿名化プログラムのサンプルです。配布データ(e.g., B32.csv and B32_3.csv)を匿名化します。

"""

import sys
import csv
import os
import random
import argparse
import warnings
import re

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

def generate_output_filename(input_file_path, output_dir=None):
    # 正規表現パターン：Bから始まり、2桁の数字が続き、_と1桁の数字、またはBから始まり2桁の数字が続く
    pattern1 = re.compile(r'B(\d{2}_\d)\.csv$')
    pattern2 = re.compile(r'B(\d{2})\.csv$')
    
    match1 = pattern1.search(input_file_path)
    match2 = pattern2.search(input_file_path)
    
    if match1:
        output_filename = re.sub(r'^B', 'C', match1.group(0))
    elif match2:
        output_filename = re.sub(r'^B', 'C', match2.group(0))
    else:
        warnings.warn("想定していないファイル名です")
        output_filename = "C.csv"
    
    if output_dir:
        return os.path.join(output_dir, output_filename)
    else:
        input_dir = os.path.dirname(input_file_path)
        return os.path.join(input_dir, output_filename)

# メインの実行部分
if __name__ == "__main__":
    # コマンドライン引数を読みこむ
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('org_csv', help='匿名化したいcsvファイル(e.g., B32_3.csv)')
    parser.add_argument('--output', '-o', help='出力ディレクトリ（指定しない場合は入力ファイルと同じディレクトリ）')
    args = parser.parse_args()

    # CSVファイルパスの読み込み
    input_file_path = args.org_csv

    # 出力ディレクトリの取得
    output_dir = args.output

    # 匿名化ファイル名の決定
    output_file_path = generate_output_filename(input_file_path, output_dir)

    # CSVファイルをpandasのデータフレームとして読み込む
    # 不正なファイルパスを指定するとここで強制終了
    Bi = pd.read_csv(input_file_path)

    # 匿名化処理
    Ci = anonymize(Bi)

    # 結果の出力
    Ci.to_csv(output_file_path, index=False)
    print(f"匿名化ファイルを{output_file_path}に保存しました")

