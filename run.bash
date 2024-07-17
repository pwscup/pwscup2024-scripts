show_help() {
  echo "使い方: bash $(basename $0) [オプション] <加工対象ファイルのフルパス(.csv)> <加工後ファイルの出力先フルパス(.csv)>"
  echo "引数が2つ必要です。"
  echo "  -h, --help         ヘルプを表示します。"
  echo "  -a, --anon         加工のみ実行します。"
  echo "  -e, --evaluate     評価のみ実行します。"
  echo "  -c, --check        チェックのみ実行します。"
}

# 引数の解析
POSITIONAL_ARGS=()

while [[ $# -gt 0 ]]; do
  case $1 in
    -h|--help)
      show_help
      exit 0
      ;;
    -a|--anon)
      ANON_ONLY=1
      shift # 引数を消費
      ;;
    -e|--evaluate)
      EVALUATE_ONLY=1
      shift # 引数を消費
      ;;
    -c|--check)
      CHECK_ONLY=1
      shift # 引数を消費
      ;;
    -*|--*)
      echo "不明なオプション $1"
      show_help
      exit 1
      ;;
    *)
      POSITIONAL_ARGS+=("$1") # 保存しておく位置引数
      shift # 引数を消費
      ;;
  esac
done

# 位置引数を元に戻す
set -- "${POSITIONAL_ARGS[@]}"

# 位置引数が2つでない場合はエラー
if [[ $# -ne 2 ]]; then
  show_help
  exit 1
fi

dir=$(dirname $0)

INPUT_FILE_PATH=$1
OUTPUT_FILE_PATH=$2

# 加工対象ファイルの存在を確認
if [[ ! -f $INPUT_FILE_PATH ]]; then
  echo "エラー: 加工対象ファイル $INPUT_FILE_PATH が存在しません。"
  exit 1
fi

# デフォルトはすべて実行
if [[ -z $ANON_ONLY && -z $EVALUATE_ONLY && -z $CHECK_ONLY ]]; then
  echo "加工を開始します。"
  python3 $dir/scripts/anonymize/anonymize.py $INPUT_FILE_PATH $OUTPUT_FILE_PATH
  echo "チェックを開始します。"
  python3 $dir/scripts/operation/checkCi.py $INPUT_FILE_PATH $OUTPUT_FILE_PATH
  echo "評価を開始します。"
  python3 $dir/scripts/evaluate/utilityScore0.py $INPUT_FILE_PATH $OUTPUT_FILE_PATH
else
  if [[ -n $ANON_ONLY ]]; then
    echo "加工を開始します。"
    python3 $dir/scripts/anonymize/anonymize.py $INPUT_FILE_PATH $OUTPUT_FILE_PATH
  fi
  
  if [[ -n $CHECK_ONLY ]]; then
    echo "チェックを開始します。"
    python3 $dir/scripts/operation/checkCi.py $INPUT_FILE_PATH $OUTPUT_FILE_PATH
  fi

  if [[ -n $EVALUATE_ONLY ]]; then
    echo "評価を開始します。"
    python3 $dir/scripts/evaluate/utilityScore0.py $INPUT_FILE_PATH $OUTPUT_FILE_PATH
  fi

fi

