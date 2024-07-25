"""

配布データのハッシュ値を計算するプログラムです。
受け取った配布データのハッシュ値がForumに掲示されているものと同一か確認してください。
配布データを誤って上書きした時もハッシュ値が変わります。

"""

import argparse
import sys, hashlib


# コマンドライン引数のパーサーを定義
parser = argparse.ArgumentParser(description=__doc__)

# コマンドライン引数を定義
parser.add_argument('org_csv', help='配布データ(e.g., B32.csv)')

# 引数を解析
args = parser.parse_args()

fn = args.org_csv
f = open(fn, 'r') # csvファイルを開く
data = f.read()   # csvファイルの中身を読み込み
f.close()         # csvファイルを閉じる

# SHA-256でハッシュ値を計算
hv = hashlib.sha256(data.encode()).hexdigest()

print(hv) # ハッシュ値をコマンドラインに表示
