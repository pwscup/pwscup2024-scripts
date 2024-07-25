"""

匿名化データ群の有用性スコアを評価するプログラムです。
分割後配布データ群(e.g., B32_0.csv ~ B32_9.csv), 匿名化データ群(e.g., C32_0.csv ~ C32_9.csv)
id.txt(この場合中身は"32"だけ)を配置したフォルダで実行してください。

"""

import sys
import argparse

from utilityScoreSingle import find_max_mae_and_columns


def us(id):
    min_us=100.0
    for i in range(10):
        file1 = 'B' + id + '_' + str(i) + '.csv'
        file2 = 'C' + id + '_' + str(i) + '.csv'
        max_mae_columns, max_mae = find_max_mae_and_columns(file1, file2, parallel)
        us = "{:.3f}".format((1-max_mae)*100)
        max_mae_value = "{:.5f}".format(max_mae)
        print(f"Max Mean Absolute Error ({i}): {max_mae_value}")
        print(f"Columns with max MAE ({i}): {max_mae_columns}")
        print(f"Utility Score ({i}): {us}")
        if(float(us)<float(min_us)):
            min_us=us
    print(f"Utility Score: {min_us}")
    return min_us

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--parallel', default=1, help='並列処理スレッド数')
    args = parser.parse_args()

    parallel = args.parallel  # デフォルトはシングルスレッド

    with open('id.txt', 'r') as file:
        id = file.read().rstrip('\n')
    min_us = us(id)
    print(min_us)
