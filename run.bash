#!/bin/bash

# ヘルプメッセージの表示
show_help() {
  echo "使い方: bash $(basename $0) <加工対象ファイルのフルパス(.csv)> <加工後ファイルの出力先フルパス(.csv)>"
    echo "引数が2つ必要です。"
    echo "  -h      ヘルプを表示します。"
}

# 引数が2つでない場合、または -h オプションが指定された場合
if [[ $# -ne 2 || "$1" == "-h" ]]; then
    show_help
    exit 1
fi

dir=$(dirname $0)

INPUT_FILE_PATH=$1
OUTPUT_FILE_PATH=$2

python3 $dir/scripts/anonymize/anonymize.py $INPUT_FILE_PATH $OUTPUT_FILE_PATH
python3 $dir/scripts/evaluate/utilityScore0_progressbar.py $INPUT_FILE_PATH $OUTPUT_FILE_PATH

