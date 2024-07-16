# pwscup2024(開発中)

- このリポジトリは、PWSCUP 2024 の**開発用プロジェクト**です。以下に、プロジェクトの構成と使用方法を説明します。
- コンテスト開始直前に最終化します　開発中の内容を、コンテスト開始後に利用しないように、ご注意ください。

## 目次
- [ディレクトリ構成](#ディレクトリ構成)
- [スクリプトの実行](#スクリプトの実行)
  - [加工・評価の一括実行](#加工と評価の一括実行)
  - [加工の個別実行](#加工の個別実行)
  - [評価の個別実行](#評価の個別実行)
  - [ハッシュ値チェックスクリプト](#ハッシュ値チェックスクリプト)
- [その他](#その他)
  - [環境構築](#環境構築)

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
│   │   └── utilityScore0.py
│   └── operation/：その他
│   │   ├── checkCi.py
│       └── checkhashvalue.py
└── .gitignore
```

## スクリプトの実行

### 加工と評価の一括実行

`/run.bash` は、

- /scripts/anonymize/anomymize.py の内容で加工して、
- /scripts/operation/checkCi.py の内容でデータ品質をチェックして、
- /scripts/evaluate/utilityScore0_progressbar.py 等の内容で評価する

処理を、一貫して実行します。

使い方は、-hで表示されるヘルプをご参照ください
```bash
bash run.bash -h
```

### 加工の個別実行

`anonymize.py` はデータを匿名化するためのスクリプトです。以下のコマンドで実行します：

```bash
python3 scripts/anonymize/anonymize.py <入力ファイルパス> <出力ファイルパス>
```
または、

```bash
bash run.bash -a  <入力ファイルパス> <出力ファイルパス>
```


### 評価の個別実行

`utilityScore0_progressbar.py` はデータの有用性評価を行うスクリプトです。進行状況を表示するプログレスバー付きです。以下のコマンドで実行します：

```bash
python3 scripts/evaluate/utilityScore0.py <入力ファイルパス> <出力ファイルパス>
```
または、

```bash
bash run.bash -e  <入力ファイルパス> <出力ファイルパス>
```


### ハッシュ値チェックスクリプト

`checkCi.py` 加工後データの値域が正しいことを確認するスクリプトです。以下のコマンドで実行します：

```bash
python3 scripts/operation/checkCi.py <入力ファイルパス> <出力ファイルパス>
```
または、

```bash
bash run.bash -c  <入力ファイルパス> <出力ファイルパス>
```

## 環境構築


### 1. uvをインストールする
まず、uvをインストールします。uvはPythonの仮想環境を管理するツールです。

```bash
pip install uv
```

### 2. uvでpythonの仮想環境を作成する
次に、uvを使用してPythonの仮想環境を作成します。ここでは、仮想環境の名前を`venv`としています。

```bash
uv create venv
```

### 3. uvでpip installする（requirements.txtを参照して）
仮想環境をアクティベートした後、requirements.txtファイルを参照して必要なパッケージをインストールします。

```bash
source .venv/bin/activate
pip install -r requirements.txt
```

これで環境構築は完了です。

仮想環境から抜ける際には、

```bash
deactivate
```
を実行してください。再度仮想環境を利用する場合は、
```bash
source .venv/bin/activate
```
を実行してください。


## その他
- Linux環境にて動作確認をしています。
- その他、プロジェクトに関する質問や問題がある場合は、slackにてお問い合わせください。
