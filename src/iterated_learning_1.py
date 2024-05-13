import random
from tap import Tap
import logging
import os
from tqdm import tqdm
import datetime
import json
import numpy as np
import pandas as pd
from Levenshtein import distance
from utils import sem_distance
from grammar import Grammar
from visualize import eps_len, TopSim, algo_counts
import matplotlib.pyplot as plt




logger = logging.getLogger(__name__)

class Args(Tap):
    data: str = "data"
    initial_grammar: str = None
    P: float = 0.8
    n_gens: int = 1
    n_samples: int = 100
    visualize: bool = True
    zeros_size: float = 0.5
    separated: bool = False
    seed: int = 1
    search_order: str = "c m r"
    compositional_size: float = None
    output_grammars: bool = False

# 追加：発話が正しく推論された回数を数える関数
def count_correct_inferences(utterances, P):
    correct_count = 0
    for utterance in tqdm(utterances, desc="Counting Correct Inferences"):
        utt_split = utterance.split(" ")
        lhs_con_gold = int(utt_split[0].split("/")[2])
        infered_con = infer_concept(lhs_con_gold, P)
        if infered_con == lhs_con_gold:
            correct_count += 1
    return correct_count

if __name__ == '__main__':
    args = Args().parse_args()
    logging.basicConfig(
        format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
        level=logging.INFO
    )
    random.seed(args.seed)
    P = args.P
    now = datetime.datetime.now()
    now_fmt = now.strftime('%Y%m%d_%H%M%S')
    os.mkdir(f"out/exp{now_fmt}")
    if args.output_grammars:
        os.mkdir(f"out/exp{now_fmt}/generations")

    # 追加：各世代ごとの正しく推論された割合を格納するリスト
    correct_ratios = []

    def infer_concept(gold, p_correct):
        if random.random() < p_correct:
            return gold
        else:
            return 1 - gold

    # （既存のコード）
    if args.initial_grammar == "compositional":
        semspace_file = os.path.join(args.data, "semantic_space.txt")
        with open(semspace_file, "r") as f:
            semantic_space = f.read()[:-1]
    elif args.initial_grammar != None:
        semspace_file = args.initial_grammar
        with open(semspace_file, "r") as f:
            semantic_space = f.read()[:-1]
    elif args.compositional_size != None:
        assert 0 <= args.compositional_size <= 1
        n_comps = int((args.n_samples)*args.compositional_size)
        n_randoms = args.n_samples - n_comps
        semspace_file = os.path.join(args.data, "semantic_space.txt")
        with open(semspace_file, "r") as f:
            compositionals = f.read()[:-1]
            compositionals_list = compositionals.split("\n")
            compositionals_list_samples = random.sample(compositionals_list, n_comps)
        randoms = generate_random_holistics(args.seed,
                                                n_randoms,
                                                args.data,
                                                args.zeros_size)
        randoms_list = randoms.split("\n")
        semantic_space_list = compositionals_list_samples + randoms_list
        semantic_space = "\n".join(semantic_space_list)
    else:
        semantic_space = generate_random_holistics(args.seed,
                                                    args.n_samples,
                                                    args.data,
                                                    args.zeros_size)

    qspace_file = os.path.join(args.data, "query_space.txt")
    with open(qspace_file, "r") as f:
        query_lines = f.read().splitlines()
        query_space = [(q.split("\t")[0], int(q.split("\t")[1])) for q in query_lines]
        query_zeros_space = [(q.split("\t")[0], int(q.split("\t")[1])) for q in query_lines if int(q.split("\t")[1])==0]
        query_ones_space = [(q.split("\t")[0], int(q.split("\t")[1])) for q in query_lines if int(q.split("\t")[1])==1]

    OPERATIONS = ["chunk01", "chunk02", "merge", "replace"]
    SEARCH_ORDER = args.search_order.split(" ")
    
    all_learning_algorithm_application_count = []

    def apply_rule(grammar, search_order, learning_algorithm_application_count):
        changed = None
        if args.separated:
            assert len(search_order) == 4, "Since separated is True, search_order must consist of the following three values: c1, c2, m, r (e.g., \"c1 c2 m r\")"
            while changed != False:
                for rule in search_order:
                    if rule == "c1":
                        rules_before = grammar.to_string()
                        grammar.chunk01()
                        rules_after = grammar.to_string()
                        if rules_before != rules_after:
                            changed == True
                            learning_algorithm_application_count["chunk1"] += 1
                            break
                        else:
                            changed = False
                            continue
                    if rule == "c2":
                        rules_before = grammar.to_string()
                        grammar.chunk02()
                        rules_after = grammar.to_string()
                        if rules_before != rules_after:
                            changed == True
                            learning_algorithm_application_count["chunk2"] += 1
                            break
                        else:
                            changed = False
                            continue
                    if rule == "m":
                        rules_before = grammar.to_string()
                        grammar.merge()
                        rules_after = grammar.to_string()
                        if rules_before != rules_after:
                            changed == True
                            learning_algorithm_application_count["merge"] += 1
                            break
                        else:
                            changed = False
                            continue
                    if rule == "r":
                        rules_before = grammar.to_string()
                        grammar.replace()
                        rules_after = grammar.to_string()
                        if rules_before != rules_after:
                            changed == True
                            learning_algorithm_application_count["replace"] += 1
                            break
                        else:
                            changed = False
                            continue
        if args.separated == False:
            assert len(search_order) == 3, "Since separated is False, search_order must consist of the following three values: c, m, r (e.g., \"c m r\")"
            while changed != False:
                for rule in search_order:
                    if rule == "c":
                        rules_before = grammar.to_string()
                        grammar.chunk01()
                        grammar.chunk02()
                        rules_after = grammar.to_string()
                        if rules_before != rules_after:
                            changed == True
                            learning_algorithm_application_count["chunk"] += 1
                            break
                        else:
                            changed = False
                            continue
                    if rule == "m":
                        rules_before = grammar.to_string()
                        grammar.merge()
                        rules_after = grammar.to_string()
                        if rules_before != rules_after:
                            changed == True
                            learning_algorithm_application_count["merge"] += 1
                            break
                        else:
                            changed = False
                            continue
                    if rule == "r":
                        rules_before = grammar.to_string()
                        grammar.replace()
                        rules_after = grammar.to_string()
                        if rules_before != rules_after:
                            changed == True
                            learning_algorithm_application_count["replace"] += 1
                            break
                        else:
                            changed = False
                            continue
        return grammar

    grammar = Grammar()
    grammar.from_string(semantic_space)
    utterances = grammar.to_string().split("\n") [:-2]

    n_gens = args.n_gens
    n_samples = args.n_samples

    use_rules_only_hist = []
    grammars = []
    epsilons = []
    lengths = []
    topsims_zero = []
    topsims_one = []

    for i in range(n_gens):
        logging.info(f"GENERATION {i} STARTS LEARNING")
        last_generation = Grammar()
        if args.separated == True:
            learning_algorithm_application_count = {"chunk1": 0, "chunk2": 0, "merge": 0, "replace":0}
        elif args.separated == False:
            learning_algorithm_application_count = {"chunk": 0, "merge": 0, "replace":0}
        # n_chunk01 = 0
        # n_chunk02 = 0
        # n_merge = 0
        # n_replace = 0
        for utterance in tqdm(utterances):
            # print(utterance)
            utt_split = utterance.split(" ")
            lhs = utt_split[0].split("/")
            rhs = utt_split[2]
            lhs_cat = lhs[0]
            lhs_sem = lhs[1]
            lhs_con_gold = int(lhs[2])
            if args.zeros_size != 1:
                infered_con = infer_concept(lhs_con_gold, P)
            else:
                infered_con = 0
            infered_utt = f"S/{lhs_sem}/{infered_con} -> {rhs}"
            last_generation.add_rule(str(infered_utt))
            # operation = random.sample(OPERATIONS, 1)[0]
            last_generation = apply_rule(last_generation, SEARCH_ORDER, learning_algorithm_application_count)
        all_learning_algorithm_application_count.append(learning_algorithm_application_count)
        length = len(last_generation.rules)
        grammars.append(last_generation.rules)
        logging.info(f"Learning finished. Result: out/exp{now_fmt}/generations/gen-{i}.txt")
        # print(f"chunk01: {n_chunk01}\nchunk02: {n_chunk02}\nmerge: {n_merge}\nreplace: {n_replace}")
        if args.output_grammars:
            with open(f"out/exp{now_fmt}/generations/gen-{i}.txt", "w") as f:
                f.write(last_generation.to_string())

        utterances = []
        use_rules_only = 0
        use_invention = 0
        if args.zeros_size != 1:
            queries = random.sample(query_space, n_samples) # bottleneck
        else:
            queries = random.sample(query_zeros_space, n_samples) # bottleneck
        generator = Grammar()
        generator.from_string(last_generation.to_string()[:-2])

        logging.info(f"generating {n_samples} utterances")
        for query, query_con in queries:
            utterance, strategy = generator.generate(query, query_con) # generate n_samples utterances
            utterances.append(utterance)
        logging.info(f"evaluating")
        if args.zeros_size != 1: # considering conceptualization
            selected_queries_zero = []
            selected_queries_one = []
            uttered_forms_zero = []
            uttered_forms_one = []
            for query, query_con in query_space:
                generator = Grammar()
                generator.from_string(last_generation.to_string()[:-2])
                uttered, strategy = generator.generate(query, query_con)
                if query_con == 0:
                    selected_queries_zero.append(query)
                    uttered_forms_zero.append(uttered.split(" ")[2])
                    if (strategy == "by-composition") or (strategy == "by-holistic-rule"):
                        use_rules_only += 1
                    else:
                        use_invention += 1
                if query_con == 1:
                    selected_queries_one.append(query)
                    uttered_forms_one.append(uttered.split(" ")[2])
                    if (strategy == "by-composition") or (strategy == "by-holistic-rule"):
                        use_rules_only += 1
                    else:
                        use_invention += 1
            epsilons.append((use_rules_only/(len(query_space)))*100)
            lengths.append(length)
            print(f"ε: {epsilons}")
            print(f"Length: {lengths}")
        else: # conventional ILM
            selected_queries = []
            uttered_forms = []
            for query, query_con in query_zeros_space:
                selected_queries.append(query)
                generator = Grammar()
                generator.from_string(last_generation.to_string()[:-2])
                uttered, strategy = generator.generate(query, query_con)
                uttered_forms.append(uttered.split(" ")[2])
                if (strategy == "by-composition") or (strategy == "by-holistic-rule"):
                    use_rules_only += 1
                else:
                    use_invention += 1
            epsilons.append((use_rules_only/len(query_zeros_space))*100)
            lengths.append(length)
            print(f"epsilon: {use_rules_only}/{len(query_zeros_space)}")
            print("History:")
            print(f"\tε: {epsilons}")
            print(f"\tLength: {lengths}")
        if args.zeros_size != 1:
            sem_distances_zero = []
            form_distances_zero = []
            sem_distances_one = []
            form_distances_one = []
            for i in range(len(selected_queries_zero)):
                for j in range(i+1, len(selected_queries_zero)):
                    sem_i, sem_j = selected_queries_zero[i], selected_queries_zero[j]
                    utt_i, utt_j = uttered_forms_zero[i], uttered_forms_zero[j]
                    sem_distances_zero.append(sem_distance(sem_i, sem_j))
                    form_distances_zero.append(distance(utt_i, utt_j))
            for i in range(len(selected_queries_one)):
                for j in range(i+1, len(selected_queries_one)):
                    sem_i, sem_j = selected_queries_one[i], selected_queries_one[j]
                    utt_i, utt_j = uttered_forms_one[i], uttered_forms_one[j]
                    sem_distances_one.append(sem_distance(sem_i, sem_j))
                    form_distances_one.append(distance(utt_i, utt_j))
        else:
            sem_distances_zero = []
            form_distances_zero = []
            for i in range(len(selected_queries)):
                for j in range(i+1, len(selected_queries)):
                    sem_i, sem_j = selected_queries[i], selected_queries[j]
                    utt_i, utt_j = uttered_forms[i], uttered_forms[j]
                    sem_distances_zero.append(sem_distance(sem_i, sem_j))
                    form_distances_zero.append(distance(utt_i, utt_j))
        topsim_zero = np.corrcoef(sem_distances_zero, form_distances_zero)[0][1]
        topsims_zero.append(topsim_zero)
        if args.zeros_size != 1:
            topsim_one = np.corrcoef(sem_distances_one, form_distances_one)[0][1]
            topsims_one.append(topsim_one)
        print(f"\tTopSims_0: {topsims_zero}")
        print(f"\tTopSims_1: {topsims_one}")
    with open(f"out/exp{now_fmt}/states.json", "w") as f:
        settings = {"initial_grammar":args.initial_grammar, "n_gens":args.n_gens,
                    "n_samples":args.n_samples, "p":args.P,
                    "zeros_size":args.zeros_size,
                    "compositional_size": args.compositional_size,
                    "seed":args.seed}
        results = {"epsilons":epsilons, "lengths":lengths, "topsims_0":topsims_zero, "topsims_1":topsims_one}
        states = {"settings":settings, "results":results}
        states_json = json.dumps(states)
        f.write(states_json)
    if args.visualize:
        eps_len(epsilons, lengths, n_gens, f"out/exp{now_fmt}/eps_len.png")
        TopSim(topsims_zero, n_gens, f"out/exp{now_fmt}/topsim_0.png")
        if args.zeros_size != 1:
            TopSim(topsims_one, n_gens, f"out/exp{now_fmt}/topsim_1.png")
    
    df_learning_algorithm_application_count = pd.DataFrame(all_learning_algorithm_application_count)
    df_learning_algorithm_application_count.to_csv(f"out/exp{now_fmt}/counts.csv", index=False)
    algo_counts(df_learning_algorithm_application_count, f"out/exp{now_fmt}/algo_counts.png")

    if __name__ == '__main__':
        args = Args().parse_args()
        # （既存のコード）

        for i in range(args.n_gens):
            # （既存のコード）

            # 追加：発話が正しく推論された回数を数える
            correct_count = count_correct_inferences(utterances, args.P)
            
            # 追加：正しく推論された割合を計算してリストに追加
            correct_ratio = correct_count / (args.n_samples)
            correct_ratios.append(correct_ratio)
            print(f"Generation {i}, Correct Ratio: {correct_ratio}")

            # （既存のコード）

            # 結果を出力
            with open(f"out/exp{now_fmt}/states.json", "w") as f:
                settings = {"initial_grammar":args.initial_grammar, "n_gens":args.n_gens,
                            "n_samples":args.n_samples, "p":args.P,
                            "zeros_size":args.zeros_size,
                            "compositional_size": args.compositional_size,
                            "seed":args.seed}
                results = {"epsilons":epsilons, "lengths":lengths, "topsims_0":topsims_zero, "topsims_1":topsims_one, "correct_count": correct_count, "correct_ratios": correct_ratios}
                states = {"settings":settings, "results":results}
                states_json = json.dumps(states)
                f.write(states_json)

            # 追加：matplotlibを使用してグラフに描画
            plt.plot(range(1, i+2), correct_ratios, marker='o')
            plt.title('Correct Ratio Over Generations')
            plt.xlabel('Generation')
            plt.ylabel('Correct Ratio')
            plt.grid(True)
            plt.savefig(f"out/exp{now_fmt}/correct_ratio_over_generations.png")
            plt.show()

            # （残りのコード）
