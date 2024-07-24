import pandas as pd
import sys

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

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <file1_prefix> <file2_prefix>")
        sys.exit(1)

    file1 = f'{sys.argv[1]}.csv'
    file2 = f'{sys.argv[2]}.csv'

    count = count_matching_cells(file1, file2)
    print(f"Number of matching cells: {count}")
