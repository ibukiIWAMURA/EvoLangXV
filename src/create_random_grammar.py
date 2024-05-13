from create_initial_grammar import generate_random_holistics
from grammar import Grammar
from tap import Tap

class Args(Tap):
    n_samples: int
    zeros_size: float
    data_path: str = "data"
    out_path: str

if __name__ == '__main__':
    args = Args().parse_args()
    grammar = Grammar()
    space = generate_random_holistics(n=args.n_samples,
                                        data_path=args.data_path,
                                        zeros_size=args.zeros_size)
    
    grammar.from_string(space)
    generated_grammar = grammar.to_string()
    
    with open(args.out_path, "w") as f:
        f.write(generated_grammar)