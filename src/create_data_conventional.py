from tap import Tap
import logging
import os
logger = logging.getLogger(__name__)

class Args(Tap):
    output_all_holistics: bool = True
    output_all_queries: bool = True
    out: str = "data"

CONCEPTS = [0, 1]

_5nouns = [("a", "_alice"), ("b", "_bob"), ("c", "_carol"), ("d", "_david"), ("e", "_eve")]
_5verbs = [("α", "_kick"), ("β", "_know"), ("γ", "_meet"), ("δ", "_like"), ("ε", "_admire")]
_5verbs_pss = [("ζ", "_kick"), ("η", "_know"), ("θ", "_meet"), ("ι", "_like"), ("κ", "_admire")]

if __name__ == '__main__':
    args = Args().parse_args()
    logging.basicConfig(
        format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
        level=logging.INFO
    )
    if args.output_all_holistics == True:
        # generate fully compositional utterances
        out_path = os.path.join(args.out, "conventional_semantic_space.txt")
        logging.info(f"A file {out_path} will be created.")
        with open(out_path, "w") as f:
            for con in CONCEPTS:
                if con == 0:
                    for verb, verb_sem in _5verbs:
                        for subj, subj_sem in _5nouns:
                            for obj, obj_sem in _5nouns:
                                if subj != obj:
                                    f.write(f"S/{verb_sem}({subj_sem},{obj_sem})/{con} -> {subj}{verb}{obj}\n")
                            else:
                                continue
                if con == 1:
                    continue
    if args.output_all_queries == True:
        # generate all possible queries
        out_path = os.path.join(args.out, "conventional_query_space.txt")
        logging.info(f"A file {out_path} will be created.")
        with open(out_path, "w") as f:
            for con in CONCEPTS:
                if con == 0:
                    for verb, verb_sem in _5verbs:
                        for subj, subj_sem in _5nouns:
                            for obj, obj_sem in _5nouns:
                                if subj_sem != obj_sem:
                                    f.write(f"{verb_sem}({subj_sem},{obj_sem})\t{con}\n")
                                else:
                                    continue
                if con == 1:
                    continue


