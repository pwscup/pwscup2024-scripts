# pwscup2024(開発中)

- このリポジトリは、PWS Cup 2024/iPWS Cup 2024 の**開発用プロジェクト**です。以下に、プロジェクトの構成と使用方法を説明します。
- コンテスト開始直前に最終化します　開発中の内容を、コンテスト開始後に利用しないように、ご注意ください。

## 使い方概要
- [環境構築](#環境構築)を参照して実行環境を作成し、
- scripts/anonymize/anonymize.pyを参照して、加工手法を実装して、
- [スクリプトの実行](#スクリプトの実行)を参照して、加工・チェック・評価を実行し、
- 加工後データをCodaBenchに提出してください

## 目次
- [ディレクトリ構成](#ディレクトリ構成)
- [スクリプトの実行](#スクリプトの実行)
  - [加工・評価の一括実行](#加工と評価の一括実行)
  - [加工の個別実行](#加工の個別実行)
  - [評価の個別実行](#評価の個別実行)
  - [ハッシュ値チェックスクリプト](#ハッシュ値チェックスクリプト)
- [環境構築](#環境構築)
- [その他](#その他)

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

使い方は、-hで表示されるヘルプをご参照ください。

-aで匿名化のみ、-cでチェックのみ、-eで評価のみ、オプションなしだとすべてを順番に実行します。

```bash
bash run.bash -h
```

### 加工の個別実行

`scripts/anonymize/anonymize.py` はデータを匿名化するためのスクリプトです。以下のコマンドで実行します：

```bash
python3 scripts/anonymize/anonymize.py <入力ファイルパス> <出力ファイルパス>
```
または、

```bash
bash run.bash -a  <入力ファイルパス> <出力ファイルパス>
```


### 評価の個別実行

`scripts/evaluate/utilityScore0.py` はデータの有用性評価を行うスクリプトです(CodaBenchへの提出は別途必要です。ご注意ください)。以下のコマンドで実行します：

```bash
python3 scripts/evaluate/utilityScore0.py <入力ファイルパス> <出力ファイルパス>
```
または、

```bash
bash run.bash -e  <入力ファイルパス> <出力ファイルパス>
```


### データチェックスクリプト

`scripts/operation/checkCi.py` 加工後データの値域が正しいことを確認するスクリプトです。以下のコマンドで実行します：

```bash
python3 scripts/operation/checkCi.py <入力ファイルパス> <出力ファイルパス>
```
または、

```bash
bash run.bash -c  <入力ファイルパス> <出力ファイルパス>
```

## 環境構築

慣れている人向け：requiments.txtを参照して、Python環境を作成してください

以下は、慣れていない方向けです。

### 0. Python環境を作成する
Python3.10以上にて、動作を確認しています。

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
uv pip install -r requirements.txt
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
