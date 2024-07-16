# pwscup2024(開発中)

- このリポジトリは、PWSCUP 2024 の**開発用プロジェクト**です。以下に、プロジェクトの構成と使用方法を説明します。
- コンテスト開始直前に最終化します　開発中の内容を、コンテスト開始後に利用しないように、ご注意ください。

## ディレクトリ構成

```
pwscup2024-dev/
├── README.md　：本ファイル
├── run.bash　：加工・評価の一括実行用スクリプト
├── data/　　　：データ置き場
│   ├── raw/
│   │   └── A.csv
│   ├── output/　：加工後ファイル置き場
│   │   └── C.csv
│   └── sample/　：加工前ファイル置き場
│       └── sampleBi.csv
├── scripts/　　　：スクリプト置き場
│   ├── anonymize/：加工スクリプト
│   │   └── anonymize.py
│   ├── evaluate/：評価スクリプト
│   │   ├── utilityScore0.py
│   │   └── utilityScore0_progressbar.py
│   └── operation/：その他
│       └── checkhashvalue.py
└── .gitignore
```

## 使用方法

### スクリプトの実行
#### 加工・評価の実行
`/run.bash` は、

- /scripts/anonymize/anomymize.py の内容で加工して、
- /scripts/evaluate/utilityScore0_progressbar.py 等の内容で評価する

処理を、一貫して実行します。

使い方は、-hで表示されるヘルプをご参照ください
```bash
bash run.bash -h
bash run.bash  <入力ファイルパス> <出力ファイルパス>
```

#### 加工の個別実行

`anonymize.py` はデータを匿名化するためのスクリプトです。以下のコマンドで実行します：

```bash
python3 scripts/anonymize/anonymize.py <入力ファイルパス> <出力ファイルパス>
```

#### 評価の個別実行

`utilityScore0_progressbar.py` はデータの有用性評価を行うスクリプトです。進行状況を表示するプログレスバー付きです。以下のコマンドで実行します：

```bash
python3 scripts/evaluate/utilityScore0_progressbar.py <入力ファイルパス> <出力ファイルパス>
```

### ハッシュ値チェックスクリプト

`checkhashvalue.py` はファイルのハッシュ値をチェックするためのスクリプトです。以下のコマンドで実行します：

```bash
python3 scripts/operation/checkhashvalue.py <入力ファイルパス>
```

## その他
### 環境構築
- python3.12にて動作確認をしています。/requirements.txtの内容をpip installしてください
- Linux環境にて動作確認をしています。
- その他、プロジェクトに関する質問や問題がある場合は、slackにてお問い合わせください。
