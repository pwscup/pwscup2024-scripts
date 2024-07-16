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

    anonymized_df = random_shuffle(anonymized_df)

    return anonymized_df

def random_shuffle(df):
    # ランダムに選んだ列の中でセルの入れ替え　x 1000回
    anonymized_df = df.copy()
    for _ in range(1000):
        col_ind = random.randint(5, 50)
        users = np.random.choice(np.arange(10000), 2, replace=False)
        tmp = anonymized_df.loc[users[0], anonymized_df.columns[col_ind]]
        anonymized_df.loc[users[0], anonymized_df.columns[col_ind]] = anonymized_df.loc[users[1],
                                                                anonymized_df.columns[col_ind]]
        anonymized_df.loc[users[1], df.columns[col_ind]] = tmp

    return anonymized_df


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

    # 読み込んだデータフレームの行数と列数を簡易チェック
    # 行数と列数が間違ったcsvファイルを読み込んだ場合はここで強制終了
    assert Bi.shape == (10000, 51), "invalid Bi"

    # 匿名化処理
    Ci = anonymize(Bi)

    # 匿名化されたデータフレームの行数と列数を簡易チェック
    # 行数と列数が間違っていた場合はここで強制終了
    assert Ci.shape == (10000, 51), "invalid Ci"
    
    # 結果の出力
    Ci.to_csv(output_file_path, index=False)
