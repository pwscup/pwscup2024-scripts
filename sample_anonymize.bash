#!/bin/bash

# スクリプトファイルのディレクトリを取得
dir=$(dirname $0)

# エラーが発生したら停止
set -e

# ヘルプメッセージの関数
show_help() {
    echo "Usage: $0 --id <ID> [--parallel <number_of_parallel_jobs>]"
    echo "ID は2桁の数字です."
    echo "サンプル匿名化では、data/input/B<ID>.csvを加工します。B<ID>.csvファイルをdata/input/に配置してください"
}

# デフォルト値の設定
parallel=1

# パラメータがない場合、またはヘルプが要求された場合
if [ "$#" -eq 0 ] || [ "$1" == "--help" ] || [ "$1" == "-h" ]; then
    show_help
    exit 0
fi

# IDの処理
if [ "$1" == "--id" ] && [[ "$2" =~ ^[0-9]{2}$ ]]; then
    id=$2
    shift 2
else
    echo "Error: Invalid or missing ID argument."
    show_help
    exit 1
fi

# オプション引数の処理
while [[ $# -gt 0 ]]
do
key="$1"

case $key in
    --parallel)
    parallel="$2"
    shift # オプションの値をスキップ
    shift # オプション自体をスキップ
    ;;
    *)
    echo "Error: Invalid argument $1"
    show_help
    exit 1
    ;;
esac
done

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

# Step 5: 安全性スコアを計算
echo "5. 安全性スコアを計算"

# 5.1 PIDを利用して、作業用一時ディレクトリを、${dir}/data/に作成する
temp_dir="${dir}/data/temp_${id}_$$"
mkdir -p $temp_dir

# 5.2 作業用ディレクトリに、${dir}/data/input/B${id}.csvと、${dir}/data/output/C${id}_*.csvを配置
cp ${dir}/data/input/B${id}.csv $temp_dir
cp ${dir}/data/output/C${id}_*.csv $temp_dir

# 5.3 作業用一時ディレクトリに移動して、python3 ${dir}/scripts/operation/maketest.py B${id}を実行
(
    cd $temp_dir
    echo "作業用一時ディレクトリでmaketest.pyを実行中..."
    python3 ../../scripts/operation/maketest.py B${id}
)

# 5.4 python3 ${dir}/scripts/attack/sampleAttack.py --id ${id} を実行
(
    cd $temp_dir
    echo "作業用一時ディレクトリでsampleAttack.pyを実行中..."
    python3 ../../scripts/attack/sampleAttack.py --id ${id}
)

# 5.5 そのまま、python3 ${dir}/scripts/operation/answerCheck.py B${id}x E を実行
(
    cd $temp_dir
    echo "安全性評価：個人特定攻撃とDB再構築攻撃の成功数(??/100)を集計中..."
    python3 ../../scripts/operation/answerCheck.py B${id}x E
)

# 作業用一時ディレクトリの削除（必要に応じてコメントアウト）
rm -rf $temp_dir

echo "サンプル加工の実行を完了"

