#!/bin/bash

# スクリプトファイルのディレクトリを取得
dir=$(dirname $0)

# ヘルプメッセージの関数
show_help() {
    echo "Usage: $0 --id <ID>"
    echo "ID must be a two-digit number."
    echo "--help or -h to show this help message."
}

# パラメータがない場合、またはヘルプが要求された場合
if [ "$#" -eq 0 ] || [ "$1" == "--help" ] || [ "$1" == "-h" ]; then
    show_help
    exit 0
fi

# IDの処理
if [ "$1" == "--id" ] && [[ "$2" =~ ^[0-9]{2}$ ]]; then
    id=$2
elif [ "$1" == "--id" ] && ! [[ "$2" =~ ^[0-9]{2}$ ]]; then
    echo "Error: Invalid ID format. ID must be a two-digit number."
    show_help
    exit 1
else
    echo "Error: Invalid or missing ID argument."
    show_help
    exit 1
fi

# Step 0: ハッシュ値の確認
echo "0. ハッシュ値の確認"
python3 ${dir}/scripts/operation/checkhashvalue.py ${dir}/data/input/B${id}.csv

# Step 1: ファイルを_0から_9まで作成
echo "1. _0から_9のファイルを作成"
python3 ${dir}/scripts/operation/split.py ${dir}/data/input/B${id}

# Step 2: 匿名加工を実行
echo "2. 匿名加工を実行"
for i in {0..9}
do
    echo "_${i}のファイルを加工中..."
    python3 ${dir}/scripts/anonymize/anonymize.py ${dir}/data/input/B${id}_$i.csv --output ${dir}/data/output/
    echo "_${i}のファイルを加工完了"
done

# Step 3: 匿名化データの形式を確認
echo "3. 匿名化データの形式を確認"
for i in {0..9}
do
    echo "_${i}のデータ形式を確認中..."
    python3 ${dir}/scripts/operation/checkCi.py ${dir}/data/input/B${id}_$i.csv ${dir}/data/output/C${id}_$i.csv
    echo "_${i}のデータ形式を確認完了"
done

# Step 4: 有用性スコアを計算
echo "4. 有用性スコアを計算"
python3 ${dir}/scripts/evaluate/utilityScore.py --id ${id} --input ${dir}/data/input --output ${dir}/data/output

