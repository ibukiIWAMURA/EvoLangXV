# EvoLangXV
## Requirements
  - Python3
  - nltk==3.8.1
  - tqdm==4.66.1
  - matplotlib==3.8.0
  - typed-argument-parser==1.8.1
  - python-Levenshtein==0.22.0
## Environment setting
For the initial setup, follow these steps.

Ensure you are in the EvoLangXV directory:
```sh
>> pwd
.../EvoLangXV
```
Activate the virtual environment and install the required libraries with the following script:
```sh
>> python -m venv evolangxv
>> source evolangxv/bin/activate
>> pip install -r requirements.txt
```

Also, create the EvoLangXV/out directory.
## Experiment
- `src/iterated_learning.py` is the experiment script
- Adjustable arguments:
  - `data`: File path for the utterance space and meaning space. Default = "data"
  - `initial_grammar`: Path to the .txt file that records the initial holistic rules. If not specified, it will be randomly generated. Default = None
  - `P`: Probability of inferring the correct conceptual label. Default = 0.8
  - `n_gens`: Number of generations. Default = 1
  - `n_samples`: Number of utterances each generation passes on to the next. Default = 100
  - `zeros_size`: Proportion of samples with conceptual label 0 out of n_samples. If set to 1, all samples will have conceptual label 0, which corresponds to the traditional ILM setting. Default = 0.5
  - `visualize`: Whether to output the expressiveness-grammar size graph. Default = True
  - `separated`: If True, chunk01 and chunk02 are treated as separate rules. If the argument --separated is specified, it will be True; otherwise, it will be False. Default = False
  - `search_order`: The search order for learning rules. Provide the following space-separated:
    - `c`: chunk01, chunk02
    - `c1`: chunk01
    - `c2`: chunk02
    - `m`: merge
    - `r`: replace
    Default = "c m r"
  - `compositional_size`: The proportion of meaning-utterance pairs to be manually created and given to the ancestor out of compositional_size$\times 100$ % (extracted from semantic_space.txt)
  - `seed`: Seed. Default = 1
  - `output_grammars`: If True, outputs the grammar of each generation. Default = False
### Preparation
Ensure you are in the EvoLangXV directory:
```sh
>> pwd
...EvoLangXV
```
Activate the virtual environment:
```sh
source evolangxv/bin/activate
```

### Example usage
An example script for inheriting 100 generations:
```sh
>> python3 src/iterated_learning.py --n_gens 100
```

When the grammar given to the ancestor is data/foo.txt:
```sh
>> python3 src/iterated_learning.py --initial_grammar data/foo.txt --n_gens 100
```

When half of the grammar given to the ancestor is manually created data:
```sh
>> python3 src/iterated_learning.py --compositional_size 0.5 --n_gens 100
```

When searching in the order of chunk, replace, merge:
```sh
>> python3 src/iterated_learning.py --initial_grammar data/foo.txt --n_gens 100 --search_order "c r m"
```

When treating chunk01 and chunk02 as separate entities:
```sh
>> python3 src/iterated_learning.py --initial_grammar data/foo.txt --n_gens 100 --search_order "c1 c2 r m" --separated
```

### Output
```
.
└── out/
    └── expYYYYMMDD_HHMMSS/
        ├── generations (grammar of each generation)/
        │   ├── gen-0.txt
        │   ├── ...
        │   └── gen-[n_gens].txt
        ├── states.json(various settings and results)
        ├── topsim.png (TopSim transition graph image)
        └── eps_len.png (Expressiveness-grammar size graph image)
```