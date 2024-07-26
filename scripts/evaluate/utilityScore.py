"""

匿名化データ群の有用性スコアを評価するプログラムです。
分割後配布データ群(e.g., B00_0.csv ~ B00_9.csv), 匿名化データ群(e.g., C00_0.csv ~ C00_9.csv)
id.txt(この場合中身は"00"だけ)を配置したフォルダで実行してください。

あるいは、
--id でidの値、
--input で分割後配布データ群の配置先フォルダ、
--output で匿名化データ群の配置先フォルダ
を指定してください。

"""

import sys
import argparse
import re

from utilityScoreSingle import find_max_mae_and_columns

def validate_id(id_value):
    """IDが2桁の数字であるか確認する。"""
    if not re.match(r'^\d{2}$', id_value):
        raise argparse.ArgumentTypeError("Invalid ID '{}'. ID must be a two-digit number.".format(id_value))
    return id_value

def get_input_output_path(args):
    """入力と出力のパスを取得する。"""
    input_path = args.input if args.input else "."
    output_path = args.output if args.output else "."
    return input_path, output_path

def us(id, input_path, output_path):
    """有用性スコアを計算する関数。"""
    min_us = 100.0
    for i in range(10):
        file1 = input_path + '/' + 'B' + id + '_' + str(i) + '.csv'
        file2 = output_path + '/' + 'C' + id + '_' + str(i) + '.csv'
        max_mae_columns, max_mae = find_max_mae_and_columns(file1, file2, parallel)
        us = "{:.3f}".format((1-max_mae)*100)
        max_mae_value = "{:.5f}".format(max_mae)
        print(f"Max Mean Absolute Error ({i}): {max_mae_value}")
        print(f"Columns with max MAE ({i}): {max_mae_columns}")
        print(f"Utility Score ({i}): {us}")
        if float(us) < float(min_us):
            min_us = us
    print(f"Utility Score: {min_us}")
    return min_us

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--id', type=validate_id, help='Specify the ID directly.')
    parser.add_argument('--input', help='Specify the path for input files.')
    parser.add_argument('--output', help='Specify the path for output files.')
    parser.add_argument('--parallel', default=1, help='Number of parallel processing threads.')
    args = parser.parse_args()

    parallel = int(args.parallel)

    if args.id:
        id = args.id
    else:
        try:
            with open('id.txt', 'r') as file:
                id = file.read().strip()
            validate_id(id)  # Validate the ID from file
        except Exception as e:
            sys.exit(f"Error reading ID: {e}")

    input_path, output_path = get_input_output_path(args)
    min_us = us(id, input_path, output_path)
    print(min_us)

