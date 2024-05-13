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
_5verbs = [("f", "_kick"), ("g", "_know"), ("h", "_meet"), ("i", "_like"), ("j", "_admire")]
_5verbs_pss = [("k", "_kick"), ("l", "_know"), ("m", "_meet"), ("n", "_like"), ("o", "_admire")]

if __name__ == '__main__':
    args = Args().parse_args()
    logging.basicConfig(
        format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
        level=logging.INFO
    )
    if args.output_all_holistics == True:
        # generate fully compositional utterances
        out_path = os.path.join(args.out, "semantic_space.txt")
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
                    for verb, verb_sem in _5verbs_pss:
                        for subj, subj_sem in _5nouns:
                            for obj, obj_sem in _5nouns:
                                if subj != obj:
                                    f.write(f"S/{verb_sem}({subj_sem},{obj_sem})/{con} -> {obj}{verb}{subj}\n")
                            else:
                                continue
    if args.output_all_queries == True:
        # generate all possible queries
        q_path = os.path.join(args.out, "query_space.txt")
        s_path_0 = os.path.join(args.out, "string_space_0.txt")
        s_path_1 = os.path.join(args.out, "string_space_1.txt")
        logging.info(f"A file {q_path} will be created.")
        logging.info(f"A file {s_path_0}/{s_path_1} will be created.")
        with open(q_path, "w") as f:
                for con in CONCEPTS:
                    if con == 0:
                        with open(s_path_0, "a") as g:
                            for verb, verb_sem in _5verbs:
                                for subj, subj_sem in _5nouns:
                                    for obj, obj_sem in _5nouns:
                                        if subj_sem != obj_sem:
                                            f.write(f"{verb_sem}({subj_sem},{obj_sem})\t{con}\n")
                                            g.write(f"{subj}{verb}{obj}\n")
                                        else:
                                            continue
                    if con == 1:
                        with open(s_path_1, "a") as g:
                            for verb, verb_pss_sem in _5verbs_pss:
                                for subj, subj_sem in _5nouns:
                                    for obj, obj_sem in _5nouns:
                                        if subj_sem != obj_sem:
                                            f.write(f"{verb_pss_sem}({obj_sem},{subj_sem})\t{con}\n")
                                            g.write(f"{obj}{verb}{subj}\n")
                                        else:
                                            continue


