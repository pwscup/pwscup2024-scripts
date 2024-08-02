"""

攻撃得点を計算するプログラムです。
正解csv(e.g., B32x.csv)と攻撃結果csv(e.g., E32.csv)を比較して得点を計算します。

"""

import argparse
import sys

import pandas as pd


def count_matching_cells(file1, file2):
    # CSVファイルを読み込む
    df1 = pd.read_csv(file1, header=None)
    df2 = pd.read_csv(file2, header=None)

    # 両方のデータフレームの形状を確認
    if df1.shape != df2.shape:
        print("Error: The CSV files do not have the same shape.")
        return

    # 一致しているセルの個数をカウント
    matching_count = (df1.values == df2.values).sum()

    return matching_count


def count_matching_cells_detail(file1, file2):
    # CSVファイルを読み込む
    df1 = pd.read_csv(file1, header=None)
    df2 = pd.read_csv(file2, header=None)

    # 両方のデータフレームの形状を確認
    if df1.shape != df2.shape:
        print("Error: The CSV files do not have the same shape.")
        return

    # 個人特定攻撃成功数をprint
    identify_count = (df1.values[:, 0] == df2.values[:, 0]).sum()
    print(f"個人特定攻撃成功数: {identify_count}/50")

    # DP再構築攻撃成功数をprint
    dbra_count = (df1.values[:, 1] == df2.values[:, 1]).sum()
    print(f'DP再構築攻撃成功数: {dbra_count}/50')

    total_count = identify_count+dbra_count
    print(f'合計攻撃成功数: {total_count}/100')
    print(f'匿名性スコア: {100-total_count}')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('Bx_csv_prefix', help='答え合わせ用csvのprefix(e.g., B32x)')
    parser.add_argument('E_csv_prefix', help='攻撃結果のcsvのprefix(e.g., E32)')
    parser.add_argument('-d', '--detail', action='store_true', help='内訳を表示')
    args = parser.parse_args()

    file1 = f'{args.Bx_csv_prefix}.csv'
    file2 = f'{args.E_csv_prefix}.csv'

    if args.detail:
        count_matching_cells_detail(file1, file2)

    else:
        count = count_matching_cells(file1, file2)
        print(f"Number of matching cells: {count}")
