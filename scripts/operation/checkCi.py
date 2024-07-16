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

        # 各列の値の辞書を作成
        value_dicts = []
        for i in range(1, len(rows_a[0])):
            value_dict = {row[i].strip() for row in rows_a}
            value_dicts.append(value_dict)

        # NG箇所の記録
        ng_positions = []
        total_checks = 0

        # 各列の値をチェック
        print("各列の値のチェックを開始します。")
        for i in tqdm(range(1, len(header_b)), desc="Checking columns"):
            # 6～51列目の場合、0～5の範囲内かを確認
            if 6 <= i <= 51:
                for row_index in range(1, len(rows_b)):  # Skip header row
                    total_checks += 1
                    value_b = rows_b[row_index][i].strip()
                    if not (value_b.isdigit() and 0 <= int(value_b) <= 5):
                        if len(ng_positions) < 20:
                            ng_positions.append((row_index, i, value_b))
            else:
                for row_index in range(1, len(rows_b)):  # Skip header row
                    total_checks += 1
                    value_b = rows_b[row_index][i].strip()
                    if value_b not in value_dicts[i - 1]:
                        if len(ng_positions) < 20:
                            ng_positions.append((row_index, i, value_b))

        # NG箇所を表示
        if ng_positions:
            for pos in ng_positions:
                print(f"NG: Value '{pos[2]}' in column '{header_b[pos[1]]}', row '{pos[0]}' is invalid.")
            print(f"...and more errors. Total NG positions: {len(ng_positions)}")
        else:
            print("OK: All checks passed successfully.")

        # 最終的な統計を表示
        print(f"Total NG positions: {len(ng_positions)}")
        print(f"Total checks performed: {total_checks}")

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

