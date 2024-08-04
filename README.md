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
  - [配布データチェックスクリプト](#配布データチェックスクリプト)
  - [配布データの分割スクリプト](#配布データの分割スクリプト)
  - [匿名化の個別実行のサンプル](#匿名化の個別実行のサンプル)
  - [匿名化データチェックスクリプト](#匿名化データチェックスクリプト)
  - [有用性評価スクリプト(個別)](#有用性個別評価スクリプト)
  - [有用性評価スクリプト(一括)](#有用性一括評価スクリプト)
  - [攻撃のサンプル](#攻撃のサンプル)
  - [匿名スコア評価スクリプト](#匿名スコア評価スクリプト)
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
│   ├── input/　：匿名化対象ファイル(B)置き場
│   │   └── (省略)
│   ├── output/　：匿名化後ファイル(C)置き場
│   │   └── sampleC.csv
│   └── sample/　：サンプルの匿名化前ファイル(B)置き場
│       └── sampleBi.csv
├── scripts/　　　：スクリプト置き場
│   ├── anonymize/：加工スクリプト
│   │   └── anonymize.py            ：(匿名化フェーズ) サンプル匿名化スクリプト
│   ├── evaluate/：評価スクリプト
│   │   ├── utilityScore.py         ：(匿名化フェーズ) 有用性評価スクリプト C<id>_0-9の10ファイル全てを一括で評価する
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

各Pythonスクリプトはコマンドラインで実行する際にオプション引数-hをつけて実行すると簡単な説明をコマンドラインに出力するようにしています。

**注意: サンプルプログラムのいくつかはB32.csvやB32_3.csvのようなB<チームid>.csvやB<チームid>_3.csvのようなファイル名が配布データに付けられていることを想定して作られています。
一方で、メールで送付された配布データはBi98.csvのようにBi<チームIDと無関係な通し番号>.csvのような形式になっています。
ハッシュ値の確認以降は配布データの名前を変更することを推奨します。
詳しくはコンテストページ(https://www.codabench.org/competitions/3262/ )のHow to anonymizeタブから確認してください。**

### 匿名化と評価の一括実行

```data/input/B00.csv``` のように、```data/input```にBファイルがある前提で、

```bash
bash sample_anonymize.bash --id 00
```

などとして、idを指定すると、サンプル加工スクリプトにより、配布データチェック・匿名化・匿名化データの形式チェック、有用性評価、サンプル匿名性評価、が一括して実行されます。

また、自作の匿名化スクリプトを作成した場合は、
```bash
bash sample_anonymize.bash --id 00 --anonymize_script /file/path/to/my_anonymize.py
```
などとして、--anonymize_scriptオプションにてスクリプトのパスを指定すると、自作の匿名化スクリプトを用いて、一括実行が走ります。


### 配布データチェックスクリプト

`./scripts/operation/checkhashvalue.py` 配布データのハッシュ値を確認します。以下のコマンドで実行します：

```bash
python3 ./scripts/operation/checkhashvalue.py <配布データ.csv>
```

例えば、配布データがBi98.csvだった場合、次のように使ってください:

```bash
python3 ./scripts/operation/checkhashvalue.py Bi98.csv
```

コマンドラインにハッシュ値が出力されるので、そのハッシュ値がForum(https://www.codabench.org/forums/3180/504/ )に掲示されているものと一致しているか確認してください。
もし一致していなかった場合、参加者自身が配布データのファイルを変更してしまったか、事務局が間違ったファイルを送付してしまった可能性があります。
参加者自身が変更してしまっていないことが確認できたにも関わらずハッシュ値が一致しない場合、事務局にご連絡ください。
間違ったファイルを元に作った匿名化ファイルは正しく採点されない可能性が高いので、ハッシュ値の不一致は放置しないことを強く推奨します。

ヘルプを表示したい場合は次のコマンドを実行してください:

```bash
python3 ./scripts/operation/checkhashvalue.py -h
```

### 配布データの分割スクリプト

`./scripts/operation/split.py`
事務局が配布データBi.csvから10個の小データBi_0.csv ~ Bi_9.csvを作るために使ったスクリプトです。
参加者はこのスクリプト利用する必要はありませんが、プログラムのテスト用に作ったオリジナルのBiから分割データを作りたいときなどに使うことを想定して公開しています。

以下のコマンドで実行します:

```bash
python3 ./scripts/operation/split.py <配布データのprefix>
```

例えば、./data/input/B32.csvを分割したい場合、次のように使ってください:

```bash
python3 ./scripts/operation/split.py ./data/input/B32
```

この例の場合、B32.csvと同じディレクトリにB32_0.csv ~ B32_9.csvが保存されます。

### 匿名化の個別実行のサンプル

`scripts/anonymize/anonymize.py` は、./data/input/B32_1.csvのような匿名化前データのパスを引数として渡して、データを匿名化するためのサンプルスクリプトです。
参加者はこのスクリプトの一部を書き換えて匿名化ファイルを作ることができます。
採点は提出されたcsvファイルに対して実施するので、csvファイルが正しく作れてさえいればこのサンプルスクリプトを元にしたプログラムを使っていなくても問題ありません。

以下のコマンドで実行します：

```bash
python3 scripts/anonymize/anonymize.py <入力ファイルパス> 
```

具体例: 

```bash
python3 scripts/anonymize/anonymize.py ./data/input/B32_1.csv 
```

この例では匿名化ファイルを`./data/input/C32_1.csv`に書き出します。

匿名化ファイルを配布データと同じディレクトリに保存したくない場合は`--output`または`-o`を使って保存先を指定することもできます:

```bash
python3 scripts/anonymize/anonymize.py ./data/input/B32_1.csv --output ./data/output/
```

**注意: この例では、分割後のファイルB32_1.csvから匿名化ファイルC32_1.csvを作ることを想定して説明しましたが、参加者がこの方法にこだわる必要はありません。
分割前の配布データB32.csvを匿名化して、それを分割してC32_0.csv ~ C32_9.csvを作っても構いません。
どんな方法を使ったとしても、C32_0.csv ~ C32_9.csvに相当するcsvファイルを事務局が指定するフォーマットで準備できれば採点対象になります。**

### 匿名化データチェックスクリプト

`./scripts/operation/checkCi.py` 匿名化ファイルが有用性評価用のスクリプトの想定するフォーマットになっていることを確認するスクリプトです。
有用性評価スクリプトがエラーを吐く場合に使ってみてください。
どんな点でフォーマットを違反しているのか具体的に教えてくれます。
違反がない場合は`すべてのチェックをクリアしました`とコマンドラインに出力します。
このスクリプトがエラー吐く匿名化ファイルはcodaBenchでも正しく採点されない可能性が高いです。

以下のコマンドで実行します：

```bash
python3 ./scripts/operation/checkCi.py <入力ファイルパス> <出力ファイルパス>
```

具体例:

```bash
python3 ./scripts/operation/checkCi.py ./data/input/B32_3.csv ./data/output/C32_3.csv
```

### 有用性個別評価スクリプト

`./script/evaluate/utilityScoreSingle.py`匿名化ファイルの有用性を評価します。
以下のコマンドで実行します:

```bash
python3 ./scripts/evaluate/utilityScoreSingle.py <分割された配布データ> <匿名化データ>
```

具体例: 

```bash
python3 ./scripts/evaluate/utilityScoreSingle.py ./data/input/B32_3.csv ./data/output/C32_3.csv
```

`--parallel`で並列処理スレッド数を指定すると評価時間が短くなる可能性があります。使用するコンピュータに依存するので、実行時間があまり変わらない場合もあります。
使用例:

```bash
python3 ./scripts/evaluate/utilityScoreSingle.py ./data/input/B32_3.csv ./data/output/C32_3.csv --parallel 4
```

### 有用性一括評価スクリプト

`./script/evaluate/utilityScore.py`10個の匿名化ファイルの有用性を一括で評価します。
コンテストでの順位付けに使われる有用性スコアはこのスクリプトと同じ方法で計算されます。
2つの実行方法を用意しました。

(実行方法1) `.`に`id.txt`というテキストファイルを配置して、そこにidを書き込んでください。例えば、`98`。
分割された配布データ群(例: B32_0.csv ~ B32_9.csv)と匿名化ファイル群(C32_0.csv ~ C32_9.csv)も同じディレクトリに配置してください。
その後、以下のコマンドで実行します:

```bash
python3 ./scripts/evaluate/utilityScoreSingle.py
```

(実行方法2) `--id`でidを、`--input`で分割された配布データ群が配置されたディレクトリを、`--output`で匿名化データ群が配置されたディレクトリを与えてください。
(`id.txt`は不要)。具体例:

```bash
python3 ./scripts/evaluate/utilityScoreSingle.py --id 32 --input ./data/input --output ./data/output
```

また、このスクリプトも`--parallel`で並列化処理スレッド数を指定できます。

**注意:** 
- **このスクリプトを実行してもcodaBenchへの匿名化ファイルの提出は行われません。CodaBenchへの提出は別途必要です。**
- **チームの有用性評価値は、```_0```から```_9```までの10ファイルの評価値から定めます（[ルール資料](https://www.iwsec.org/pws/2024/cup24.html#%E5%8F%82%E5%8A%A0%E8%80%85%E5%90%91%E3%81%91%E8%B3%87%E6%96%99:~:text=%E6%B1%BA%E5%AE%9A%E3%81%97%E3%81%BE%E3%81%99%E3%80%82-,%E5%8F%82%E5%8A%A0%E8%80%85%E5%90%91%E3%81%91%E8%B3%87%E6%96%99,-PWSCup2024%EF%BC%86iPWSCup2024%20%E3%83%AB%E3%83%BC%E3%83%AB)【匿名化フェーズ】 有用性とサンプル匿名性を参照）**

### 攻撃のサンプル

`scripts/attack/sampleAttack.py`攻撃のサンプルコードです。サンプル匿名性の計算に使っている攻撃方法でもあります。
2種類の実行方法を用意しました。

(実行方法1) 以下のコマンドで実行します:
```bash
python scripts/attack/sampleAttack.py <Ba_prefix> <Bb_prefix> <C_prefix>
```
具体例:
```bash
python scripts/attack/sampleAttack.py data/input/B32a data/input/B32b data/output/C32
```
実行の経過を出力しながら攻撃を行います。
実行後、攻撃結果E.csvがコマンドを実行したディレクトリに保存されます。

(実行方法2) コマンドを実行するディレクトリに攻撃用ファイル群(e.g., B32a.csvとB32b.csv)と匿名化ファイル群(e.g., C32_0.csv ~ C32_9.csv)を配置した後、以下のコマンドで実行します:
```bash
python scripts/attack/sampleAttack.py --id <id>
```
具体例:
```bash
python scripts/attack/sampleAttack.py --id 32
```

いずれの実行方法でも`--no_print`をコマンドに追加すると実行経過を出力しません。攻撃結果E.csvの保存だけを行います。

### 匿名スコア評価スクリプト

`scripts/operation/answerCheck.py`攻撃結果から攻撃成功数を計算します。
以下のコマンドで実行します:
```bash
python scripts/operation/answerCheck.py <Bx_csv_prefix> <E_csv_prefix>
```
具体例:
```bash
python scripts/operation/answerCheck.py data/input/B32x E
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
- その他、プロジェクトに関する質問や問題がある場合は、[slack](https://join.slack.com/t/pwscup/shared_invite/zt-7wxs8az7-aFBs2~BTpQeriLZRZ5H4ew)の「公開_運営への質問要望」チャンネルにて個別にてお問い合わせください。
