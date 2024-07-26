# pwscup2024(開発中)

- このリポジトリは、PWS Cup 2024/iPWS Cup 2024 の**開発用プロジェクト**です。以下に、プロジェクトの構成と使用方法を説明します。
- コンテスト開始直前に最終化します　開発中の内容を、コンテスト開始後に利用しないように、ご注意ください。
- コンテストルールにつきましては、[ルール資料](https://www.iwsec.org/pws/2024/cup24.html#%E5%8F%82%E5%8A%A0%E8%80%85%E5%90%91%E3%81%91%E8%B3%87%E6%96%99:~:text=%E6%B1%BA%E5%AE%9A%E3%81%97%E3%81%BE%E3%81%99%E3%80%82-,%E5%8F%82%E5%8A%A0%E8%80%85%E5%90%91%E3%81%91%E8%B3%87%E6%96%99,-PWSCup2024%EF%BC%86iPWSCup2024%20%E3%83%AB%E3%83%BC%E3%83%AB)をご確認ください。
## 使い方概要
- [環境構築](#環境構築)を参照して実行環境を作成し、
- scripts/anonymize/anonymize.pyを参照して、加工手法を実装して、
- [スクリプトの実行](#スクリプトの実行)を参照して、加工・チェック・評価を実行し、
- 加工後データをCodaBenchに提出してください

## 目次
- [ディレクトリ構成](#ディレクトリ構成)
- [スクリプトの実行](#スクリプトの実行)
  - [匿名化・評価の一括実行](#匿名化と評価の一括実行)
  - [匿名化の個別実行](#匿名化の個別実行)
  - [評価の個別実行](#評価の個別実行)
  - [配布データチェックスクリプト](#配布データチェックスクリプト)
  - [匿名化データチェックスクリプト](#匿名化データチェックスクリプト)
- [環境構築](#環境構築)
- [その他](#その他)

## ディレクトリ構成

```
pwscup2024-dev/
├── README.md　：本ファイル
├── sample_anonymize.bash　：(匿名化フェーズ) 加工・評価のサンプル実行用スクリプト
├── data/　　　：データ置き場
│   ├── raw/
│   │   └── A.csv
│   ├── output/　：匿名化後ファイル(C)置き場
│   │   └── sampleC.csv
│   └── sample/　：匿名化前ファイル(B)置き場
│       └── sampleBi.csv
├── scripts/　　　：スクリプト置き場
│   ├── anonymize/：加工スクリプト
│   │   └── anonymize.py            ：(匿名化フェーズ) 匿名化スクリプト
│   ├── evaluate/：評価スクリプト
│   │   ├── utilityScore.py         ：(匿名化フェーズ) 有用性評価スクリプト 0-9まで全てを一括で評価する
│   │   └── utilityScoreSingle.py   ：(匿名化フェーズ) 有用性評価スクリプト 単体の評価
│   ├── attack/　：攻撃スクリプト
│   │   └── sampleAttack.py   ：(匿名化フェーズ/攻撃フェーズ) サンプル匿名性評価とサンプル攻撃用スクリプト
│   └── operation/：その他
│   │   ├── checkhashvalue.py ：(匿名化フェーズ) 配布データのintegrityを確認する際に利用する
│   │   ├── checkCi.py        ：(匿名化フェーズ) Bから作成した匿名化データCの形式が正しいことをチェックする際に利用する
│   │   ├── maketest.py       ：(攻撃フェーズ) 配布データから攻撃用データを作成する際に利用する
│   │   ├── answercheck.py    ：(攻撃フェーズ) 正解と攻撃結果を比較して、攻撃得点を計算する際に利用する
│       └── split.py          ：(運営用) 運営が、Bi.csvから10パターンのサブセットデータを作成する際に利用する
└── .gitignore
```

## スクリプトの実行

### 匿名化と評価の一括実行

```bash
bash sample_anonymize.bash --id 00
```
などとして、idを指定すると、サンプル加工スクリプトによる加工と評価が実行されます。

### 匿名化の個別実行

`scripts/anonymize/anonymize.py` は、./data/smaple/B00_1.csvのような匿名化前データのパスと、./data/output/C00_1.csvのように匿名化後データの出力先パスを引数として渡して、データを匿名化するためのスクリプトです。以下のコマンドで実行します：

```bash
python3 scripts/anonymize/anonymize.py <入力ファイルパス> <出力ファイルパス>
```


### 評価の個別実行

`./scripts/evaluate/utilityScoreSingle.py` は、./data/sample/B00_1.csvと./data/output/C00_1.csvのような匿名化前後データのパスを引数として渡して、データの有用性評価を行うスクリプトです。
- 提出は行われません。CodaBenchへの提出は別途必要です。ご注意ください
- チームの有用性評価値は、```_0```から```_9```までの10ファイルの評価値から定めます（[ルール資料](https://www.iwsec.org/pws/2024/cup24.html#%E5%8F%82%E5%8A%A0%E8%80%85%E5%90%91%E3%81%91%E8%B3%87%E6%96%99:~:text=%E6%B1%BA%E5%AE%9A%E3%81%97%E3%81%BE%E3%81%99%E3%80%82-,%E5%8F%82%E5%8A%A0%E8%80%85%E5%90%91%E3%81%91%E8%B3%87%E6%96%99,-PWSCup2024%EF%BC%86iPWSCup2024%20%E3%83%AB%E3%83%BC%E3%83%AB)【匿名化フェーズ】 有用性とサンプル匿名性を参照）

以下のコマンドで実行します：

```bash
python3 ./scripts/evaluate/utilityScoreSingle.py <入力ファイルパス> <出力ファイルパス>
```

### 配布データチェックスクリプト

`./scripts/operation/checkhashvalue.py` 配布データのハッシュ値を確認します。以下のコマンドで実行します：

```bash
python3 ./scripts/operation/checkhashvalue.py <配布データ.csv>
```


### 匿名化データチェックスクリプト

`./scripts/operation/checkCi.py` 匿名化後データの値域が正しいことを確認するスクリプトです。以下のコマンドで実行します：

```bash
python3 ./scripts/operation/checkCi.py <入力ファイルパス> <出力ファイルパス>
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
uv venv
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
