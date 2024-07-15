# pwscup2024-dev

# PWSCUP 2024 Dev

このリポジトリは、PWSCUP 2024 の開発用プロジェクトです。以下に、プロジェクトの構成と使用方法を説明します。

## ディレクトリ構成

```
pwscup2024-dev/
├── data/
│   ├── raw/
│   │   └── A.csv
│   └── sample/
│       └── sampleBi.csv
├── scripts/
│   ├── anonymize/
│   │   └── anonymize.py
│   ├── evaluate/
│   │   ├── tmp.txt
│   │   ├── utilityScore0.py
│   │   └── utilityScore0_progressbar.py
│   └── operation/
│       └── checkhashvalue.py
├── .gitignore
└── README.md
```

## 使用方法

### スクリプトの実行
#### 加工・評価の実行
`/run.bash` は、
- /scripts/anonymize/anomymize.pyの内容で加工して、
- /scripts/evaluate/utilityScore0_progressbar.py の内容で評価する
のを一貫して実行します。

使い方：-hで表示されるヘルプをご参照ください
```bash
bash run.bash -h
bash run.bash  <入力ファイルパス> <出力ファイルパス>
```

#### 匿名化スクリプト

`anonymize.py` はデータを匿名化するためのスクリプトです。以下のコマンドで実行します：

```bash
python3 scripts/anonymize/anonymize.py <入力ファイルパス> <出力ファイルパス>
```

#### 評価スクリプト

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

- `data/raw/` フォルダには生データが含まれています。
- `data/sample/` フォルダにはサンプルデータが含まれています。
- `.gitignore` ファイルには、Git で無視するファイルやディレクトリが指定されています。

プロジェクトに関する質問や問題がある場合は、slackにてお問い合わせください。
