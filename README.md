# EvoLangXV
## Requirements
  - Python3
  - nltk==3.8.1
  - tqdm==4.66.1
  - matplotlib==3.8.0
  - typed-argument-parser==1.8.1
  - python-Levenshtein==0.22.0
## Environment setting
初回の環境構築は以下の手順で実施する。

`EvoLangXV` ディレクトリにいることを確認:
```sh
>> pwd
.../EvoLangXV
```
以下スクリプトで仮想環境の有効化、ライブラリのインストール:
```sh
>> python -m venv evolangxv
>> source evolangxv/bin/activate
>> pip install -r requirements.txt
```

また、`EvoLangXV/out` ディレクトリを作成しておく。
## Experiment
- `src/iterated_learning.py` が実験スクリプト
- 調整可能な引数:
  - `data`: 発話空間、意味空間のファイルパス。デフォルト = "data"
  - `initial_grammar`: 最初に与える全体論的規則が記録された.txtファイルへのパス。何も指定しなければランダム生成する。デフォルト = None
  - `P`: 正しい概念化ラベルを推論する確率。デフォルト = 0.8
  - `n_gens`: 世代数。デフォルト = 1
  - `n_samples`: 各世代が次の世代へと伝える発話数。デフォルト = 100
  - `zeros_size`: `n_samples` のうち、概念ラベル `0` のサンプルの割合。`1` にすると全て概念ラベル `0` となり、従来のILMと同じセッティングになる。デフォルト = 0.5
  - `visualize`: 表現度-文法大きさグラフを出力するかどうか。デフォルト = True
  - `separated`: True の場合、`chunk01` と `chunk02` は別個のルールとして扱われる。引数に `--separated` と記述すると True、何もしなければ False になる。デフォルト = False
  - `search_order`: 学習規則の検索順序。以下をスペース区切りで並べ与える:
    - `c`: chunk01, chunk02
    - `c1`: chunk01
    - `c2`: chunk02
    - `m`: merge
    - `r`: replace
    デフォルト = "c m r"
  - `compositional_size`: 始祖に渡す意味-発話ペアのうち `compositional_size`$\times 100$ % を、人為的に作成した意味-発話ペアからサンプリングして与える（`semantic_space.txt` から抽出する）
  - `seed`: シード。デフォルト = 1
  - `output_grammars`: True の場合、各世代の文法を出力する。デフォルト = False
### Preparation
EvoLangXV にいることを確認:
```sh
>> pwd
...EvoLangXV
```
仮想環境を有効化:
```sh
source evolangxv/bin/activate
```

### Example usage
100世代継承するスクリプト例:
```sh
>> python3 src/iterated_learning.py --n_gens 100
```

始祖に渡す文法が `data/foo.txt` であるとき:
```sh
>> python3 src/iterated_learning.py --initial_grammar data/foo.txt --n_gens 100
```

始祖に渡す文法の半分を人為データで実施するとき:
```sh
>> python3 src/iterated_learning.py --compositional_size 0.5 --n_gens 100
```

chunk, replace, merge の順で検索させるとき:
```sh
>> python3 src/iterated_learning.py --initial_grammar data/foo.txt --n_gens 100 --search_order "c r m"
```

chunk01 と chunk02 を別物扱いするとき:
```sh
>> python3 src/iterated_learning.py --initial_grammar data/foo.txt --n_gens 100 --search_order "c1 c2 r m" --separated
```

### 出力
```
.
└── out/
    └── expYYYYMMDD_HHMMSS/
        ├── generations (各世代の文法)/
        │   ├── gen-0.txt
        │   ├── ...
        │   └── gen-[n_gens].txt
        ├── states.json (各種設定と結果)
        ├── topsim.png (TopSimの推移グラフ画像)
        └── eps_len.png (表現度-文法サイズのグラフ画像)
```