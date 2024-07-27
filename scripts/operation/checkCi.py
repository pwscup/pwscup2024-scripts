"""

このプログラムは入力されたCSVファイルが有用性評価プログラムに適した形式であるかを検証します。
「すべてのチェックをクリアしました」
と表示されれば、有用性評価ブログラムが適切に採点できる形式になっています。
強制終了した場合はエラーメッセージを参考にCSVファイルを再検討してください。

"""

import argparse
import os
import sys
import re

import pandas as pd
from tqdm import tqdm

valid_num_rows = 10000

def check_file2_name_format(file2_basename):
    # 正規表現パターン：Cから始まり、2桁の数字が続き、_の後に1桁の数字、そして.csvで終わる
    pattern = r'^C\d{2}_\d\.csv$'
    if not re.match(pattern, file2_basename):
        return False
    return True

def check_csv_file(file1, file2):
    # CSVファイルの存在確認
    if not os.path.exists(file1):
        print(f"エラー: ファイル '{file1}' が存在しません")
        return False, [f"ファイル '{file1}' が存在しません"]
    if not os.path.exists(file2):
        print(f"エラー: ファイル '{file2}' が存在しません")
        return False, [f"ファイル '{file2}' が存在しません"]

    # file2のフォーマット確認
    if not check_file2_name_format(os.path.basename(file2)):
        print(f"エラー: ファイル '{file2}' の名前のフォーマットが正しくありません")
        return False, [f"ファイル '{file2}' の名前のフォーマットが正しくありません"]

    # CSVファイルを読み込む
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)

    # "Name"列を削除して比較用のデータを作成
    B = df1.drop(columns=["Name"], errors='ignore')
    C = df2.drop(columns=["Name"], errors='ignore')

    # チェックNGの箇所を記録するリスト
    errors = []

    # 進捗表示用のtqdmの設定
    total_checks = len(C.columns) + 2  # 行数・列数チェック + 列ごとのチェック
    progress_bar = tqdm(total=total_checks, desc="チェック進行中", ncols=100)

    # 1. 行数が指定どおりであること
    if C.shape[0] != valid_num_rows:
        errors.append(f"行数が{valid_num_rows}ではありません")
        progress_bar.update(1)
        progress_bar.close()
        return False, errors
    progress_bar.update(1)

    # 2. 列名が一致していることを確認
    if not all(B.columns == C.columns):
        errors.append("列名が一致しません")
        progress_bar.update(1)
        progress_bar.close()
        return False, errors
    progress_bar.update(1)

    # 3. 列ごとのチェック
    for col in C.columns:
        if col.isdigit():
            if not C[col].isin([0, 1, 2, 3, 4, 5]).all():
                errors.append(f"列 {col} に0から5の整数以外の値が含まれています")
                if len(errors) >= 20:
                    break
        else:
            if not C[col].isin(B[col]).all():
                errors.append(f"列 {col} にBの当該列に含まれる値以外の値が含まれています")
                if len(errors) >= 20:
                    break
        progress_bar.update(1)

    progress_bar.close()

    if errors:
        return False, errors

    return True, []

def main():
    # コマンドライン引数のパーサーを定義
    parser = argparse.ArgumentParser(description=__doc__)

    # コマンドライン引数を定義
    parser.add_argument('org_csv',
         help='分割された配布ファイル名(e.g., B32_9.csv)')
    parser.add_argument('ano_csv',
        help='検証したい匿名化ファイル名(e.g., C32_9.csv)')

    # 引数を解析
    args = parser.parse_args()

    file1 = args.org_csv
    file2 = args.ano_csv

    result, error_list = check_csv_file(file1, file2)

    if not result:
        print("チェックがNGの箇所(20箇所まで表示します)：")
        for error in error_list:
            print(error)
    else:
        print("すべてのチェックをクリアしました")

if __name__ == "__main__":
    main()
