import sys
import csv
from tqdm import tqdm

valid_num_rows = 10001

def check_csv_files(file_a, file_b):
    try:
        with open(file_a, newline='') as csvfile_a:
            reader_a = csv.reader(csvfile_a)
            rows_a = list(reader_a)
        with open(file_b, newline='') as csvfile_b:
            reader_b = csv.reader(csvfile_b)
            rows_b = list(reader_b)

        # 行数をチェック
        print("行数のチェックを開始します。")
        if len(rows_b) != valid_num_rows:
            print(f"NG (row number): Expected {valid_num_rows} rows, but found {len(rows_b)} rows.")
            return

        # ヘッダー行を取得
        header_b = rows_b[0]

        # 各列の値をチェック
        print("各列の値のチェックを開始します。")
        for i in tqdm(range(1, len(header_b)), desc="Checking columns"):
            for row_index in range(len(rows_b)):
                value_b = rows_b[row_index][i].strip()
                if value_b not in [row[i].strip() for row in rows_a]:
                    print(f"NG: Value '{value_b}' in column '{header_b[i]}' is invalid.")
                    return

        # すべてのチェックがOKだった場合
        print("OK: All checks passed successfully.")

    except FileNotFoundError:
        print(f"NG (file not found): File '{file_a}' or '{file_b}' not found.")

if __name__ == "__main__":
    # コマンドライン引数からファイル名を取得
    if len(sys.argv) != 3:
        print("Usage: python program.py <a.csv> <b.csv>")
        sys.exit(1)
    
    file_a = sys.argv[1]
    file_b = sys.argv[2]
    check_csv_files(file_a, file_b)

