from nltk.sem.logic import *
import ast
import random
import string
import copy

NOUNS = [
    "david", "alice", "bob", "carol", "eve", "frank", "grace", "helen", 
    "ivan", "jack", "karen", "larry", "mike", "nina", "oscar", "paul", 
    "quincy", "rachel", "steve", "tracy", "ursula", "victor", "wendy", 
    "xander", "yasmine", "zach"
]

VERBS = [
    "know", "admire", "like", "kick", "meet", "call", "defend", "encourage"
    , "follow", "greet", "help", "invite", "judge", "notice", "obey", 
    "praise", "question", "respect", "support", "trust", "understand", 
    "value", "warn", "x-ray", "yell", "zap"
]

VERBS_PSS = [
    "known", "admired", "liked", "kicked", "met"
]

def generate_noun(n_sorts: str, stopword: str = ""):
    assert n_sorts <= len(string.ascii_lowercase)
    chars_wo_stopword = [char for char in string.ascii_lowercase[:n_sorts] if char not in stopword]
    return random.choice(chars_wo_stopword)

def generate_verb(n_sorts: str, stopword: str = ""):
    greek_lowercase = [chr(i) for i in range(945, 970)]
    chars_wo_stopword = [char for char in greek_lowercase[:n_sorts] if char not in stopword]
    return random.choice(chars_wo_stopword)

def generate_noun_sem(n_sorts: str, stopword: str = ""):
    assert n_sorts <= len(NOUNS)
    chars_wo_stopword = [char for char in NOUNS[:n_sorts] if char not in stopword]
    return random.choice(chars_wo_stopword)

def generate_verb_sem(n_sorts: str, stopword: str = ""):
    chars_wo_stopword = [char for char in (VERBS[:n_sorts]+VERBS_PSS[:n_sorts]) if char not in stopword]
    return random.choice(chars_wo_stopword)

def replace_at_index(s, index, replacement):
    return s[:index] + replacement + s[index + 1:]

N_SORTS = 5
NONTERMINALS = [char for char in string.ascii_uppercase if char != "S"]
VERB_CATS = NONTERMINALS[:10]
NOUN_CATS = NONTERMINALS[10:]
INDIVIDUAL_VARIABLES = ["x", "y"]
FUNCTIONAL_VARIABLES = ["X"]
GREEK_LOWER = [chr(i) for i in range(945, 970)]
ENGLISH_LOWER = [char for char in string.ascii_lowercase[:N_SORTS] if char not in ["x", "y"]]

class Grammar():
    def __init__(self):
        self.rules = []

    def from_string(self, string: str):
        self.rules = []
        rules_str = string.split("\n")
        for rule_str in rules_str:
            if rule_str != "\n":
                if len(rule_str.split("\t")) == 2:
                    rule_body, assignments = rule_str.split("\t")[0], rule_str.split("\t")[1]
                    assignments = assignments.replace("(", "").replace(")", "")
                    asignments_list = assignments.split(", ")
                    asignments_dict = {str(assig.split(":")[0]):int(assig.split(":")[1]) for assig in asignments_list}
                    assignments_sorted = sorted(asignments_dict.items())
                    asignments_sorted_dict = dict((var, idx) for var, idx in assignments_sorted)
                    rule = rule_body.split(" ")
                    lhs = rule[0].split("/")
                    rhs = rule[2]
                    lhs_cat = lhs[0]
                    lhs_sem = lhs[1]
                    lhs_con = int(lhs[2])
                    rule = {'lhs':{'cat':lhs_cat, 'sem':lhs_sem, 'con':lhs_con}, 'rhs':rhs, 'var':asignments_sorted_dict}
                    self.rules.append(rule)
                if len(rule_str.split("\t")) == 1:
                    rule = rule_str.split(" ")
                    lhs = rule[0].split("/")
                    rhs = rule[2]
                    if len(lhs) == 3:
                        lhs_cat = lhs[0]
                        lhs_sem = lhs[1]
                        lhs_con = int(lhs[2])
                        rule = {'lhs':{'cat':lhs_cat, 'sem':lhs_sem, 'con':lhs_con}, 'rhs':rhs}
                    if len(lhs) == 2:
                        lhs_cat = lhs[0]
                        lhs_sem = lhs[1]
                        rule = {'lhs':{'cat':lhs_cat, 'sem':lhs_sem}, 'rhs':rhs}
                    self.rules.append(rule)
    
    def add_rule(self, string: str):
        rules_str = string.split("\n")
        for rule_str in rules_str:
            if rule_str != "\n":
                if len(rule_str.split("\t")) == 2:
                    rule_body, assignments = rule_str.split("\t")[0], rule_str.split("\t")[1]
                    assignments = assignments.replace("(", "").replace(")", "")
                    asignments_list = assignments.split(", ")
                    asignments_dict = {str(assig.split(":")[0]):int(assig.split(":")[1]) for assig in asignments_list}
                    assignments_sorted = sorted(asignments_dict.items())
                    asignments_sorted_dict = dict((var, idx) for var, idx in assignments_sorted)
                    rule = rule_body.split(" ")
                    lhs = rule[0].split("/")
                    rhs = rule[2]
                    lhs_cat = lhs[0]
                    lhs_sem = lhs[1]
                    lhs_con = int(lhs[2])
                    rule = {'lhs':{'cat':lhs_cat, 'sem':lhs_sem, 'con':lhs_con}, 'rhs':rhs, 'var':asignments_sorted_dict}
                    self.rules.append(rule)
                if len(rule_str.split("\t")) == 1:
                    rule = rule_str.split(" ")
                    lhs = rule[0].split("/")
                    rhs = rule[2]
                    if len(lhs) == 3:
                        lhs_cat = lhs[0]
                        lhs_sem = lhs[1]
                        lhs_con = int(lhs[2])
                        rule = {'lhs':{'cat':lhs_cat, 'sem':lhs_sem, 'con':lhs_con}, 'rhs':rhs}
                    if len(lhs) == 2:
                        lhs_cat = lhs[0]
                        lhs_sem = lhs[1]
                        rule = {'lhs':{'cat':lhs_cat, 'sem':lhs_sem}, 'rhs':rhs}
                    self.rules.append(rule)
    
    def to_string(self):
        rules_list = []
        rules_str = ""
        for rule in self.rules:
            if 'var' in rule:
                asigs_str = "(" + ", ".join(f"{k}:{v}" for k, v in rule['var'].items()) + ")"
                rules_list.append(f"{rule['lhs']['cat']}/{rule['lhs']['sem']}/{rule['lhs']['con']} -> {rule['rhs']}\t{asigs_str}\n")
            elif 'con' in rule['lhs']:
                rules_list.append(f"{rule['lhs']['cat']}/{rule['lhs']['sem']}/{rule['lhs']['con']} -> {rule['rhs']}\n")
            else:
                rules_list.append(f"{rule['lhs']['cat']}/{rule['lhs']['sem']} -> {rule['rhs']}\n")
        sorted_list = sorted(sorted(rules_list), key=lambda x: -len(x))
        rules_str += ''.join(sorted_list)+"\n"
        return rules_str
    
    def str2dict(self, string):
        return ast.literal_eval(string)
    
    def sem_list(self):
        return [d['lhs']['sem'] for d in self.rules]
    
    def cat_list(self):
        return [d['lhs']['cat'] for d in self.rules]
    
    def sentence_list(self):
        return [d['rhs'] for d in self.rules]
    
    def is_well_formed(self, expr_str, form):
        expr = Expression.fromstring(expr_str)
        num_var_expr = len([term for term in expr.free()])
        num_uppercase = sum(1 for char in form if char.isupper())
        return num_var_expr == num_uppercase

    def is_well_assigned(self, form, assignments):
        num_uppercase = sum(1 for char in form if char.isupper())
        num_assigs = len(assignments)
        return num_assigs == num_uppercase

    def can_chunk01(self, rule1, rule2):
        str1, str2 = rule1["rhs"], rule2["rhs"]
        sem1_logic = Expression.fromstring(rule1["lhs"]["sem"])
        sem2_logic = Expression.fromstring(rule2["lhs"]["sem"])
        con1 = rule1["lhs"]["con"]
        con2 = rule2["lhs"]["con"]

        if len(str1) != 3 or len(str2) != 3: # TODO: Better to judge by category (not sentence length)
            return None, None, False
        if con1 != con2:
            return None, None, False
        sem1, sem2 = [sem1_logic.pred, sem1_logic.args[0], sem1_logic.args[1]], [sem2_logic.pred, sem2_logic.args[0], sem2_logic.args[1]]
        # print(str1, str2)
        diff_count_str = 0
        diff_positions_str = []
        for i, (char1, char2) in enumerate(zip(str1, str2)):
            if (char1 != char2):
                # diff_count_str += 1
                diff_positions_str.append(i)
        diff_count_sem = 0
        diff_positions_sem = []
        for i, (elm1, elm2) in enumerate(zip(sem1, sem2)):
            if (elm1 != elm2):
                # diff_count_sem += 1
                diff_positions_sem.append(i)
        if (len(diff_positions_str) == len(diff_positions_sem) == 1) and ((isinstance(sem1[diff_positions_sem[0]], ConstantExpression)) and (isinstance(sem2[diff_positions_sem[0]], ConstantExpression))):
            if str1[diff_positions_str[0]].islower() and str2[diff_positions_str[0]].islower():
                return diff_positions_str[0], diff_positions_sem[0], True
            else:
                return None, None, False
        else:
            return None, None, False

    def find_diff_position_for_chunk01(self, str1, str2):
        if len(str1) != 3 or len(str2) != 3:
            return None

        diff_count = 0
        diff_index = None
        for index, (char1, char2) in enumerate(zip(str1, str2)):
            if char1 != char2:
                diff_count += 1
                diff_index = index
                if not (char1.islower() and char2.islower()):
                    return None

        if diff_count == 1:
            if diff_index == 0:
                diff_index_sem = 1
            if diff_index == 1:
                diff_index_sem = 0
            if diff_index == 2:
                diff_index_sem = 2
            return diff_index, diff_index_sem
        else:
            return None
    
    def can_chunk02(self, rule1, rule2):
        str1, str2 = rule1["rhs"], rule2["rhs"]
        sem1_logic = Expression.fromstring(rule1["lhs"]["sem"])
        sem2_logic = Expression.fromstring(rule2["lhs"]["sem"])
        sem1, sem2 = [sem1_logic.pred, sem1_logic.args[0], sem1_logic.args[1]], [sem2_logic.pred, sem2_logic.args[0], sem2_logic.args[1]]
        con1 = rule1["lhs"]["con"]
        con2 = rule2["lhs"]["con"]

        if len(str1) != 3 or len(str2) != 3: # TODO: Better to judge by category (not sentence length)
            return None, None, False, None, None
        if con1 != con2:
            return None, None, False, None, None
        # print(str1, str2)
        diff_count_str = 0
        diff_positions_str = []
        for i, (char1, char2) in enumerate(zip(str1, str2)):
            if (char1 != char2):
                # if (char1.islower() and char2.isupper()):
                diff_count_str += 1
                diff_positions_str.append(i)
                # elif (char1.isupper() and char2.islower()):
                # else:
                #    None, False, None, None
        diff_count_sem = 0
        diff_positions_sem = []
        for i, (elm1, elm2) in enumerate(zip(sem1, sem2)):
            if (elm1 != elm2):
                diff_count_sem += 1
                diff_positions_sem.append(i)
        if len(diff_positions_str) == len(diff_positions_sem) == 1:
            if (str1[diff_positions_str[0]].islower() and str2[diff_positions_str[0]].isupper()):
                upper_in_str, lower_in_str = 1, 0
                return diff_positions_str[0], diff_positions_sem[0], True, upper_in_str, lower_in_str
            elif (str1[diff_positions_str[0]].isupper() and str2[diff_positions_str[0]].islower()):
                upper_in_str, lower_in_str = 0, 1
                return diff_positions_str[0], diff_positions_sem[0], True, upper_in_str, lower_in_str
            else:
                return None, None, False, None, None
        else:
            return None, None, False, None, None
    
    def find_diff_position_for_chunk02(self, str1, str2):
        if len(str1) != 3 or len(str2) != 3:
            return None, None

        diff_count = 0
        diff_index = None
        upper_in_str = None

        for index, (char1, char2) in enumerate(zip(str1, str2)):
            if char1 != char2:
                diff_count += 1
                diff_index = index
                if (char1.islower() and char2.isupper()):
                    lower_in_str = 0
                    upper_in_str = 1
                elif (char1.isupper() and char2.islower()):
                    lower_in_str = 1
                    upper_in_str = 0
                else:
                    return None, None

        if diff_count == 1:
            if diff_index == 0:
                diff_index_sem = 1
            if diff_index == 1:
                diff_index_sem = 0
            if diff_index == 2:
                diff_index_sem = 2
            return diff_index, diff_index_sem, upper_in_str, lower_in_str
        else:
            return None, None

    def highlight_for_replace(self, str1, str2):
        if (len(str1) == 3) & (len(str2) == 1):
            if str1.count(str2) == 1:
                non_word_level, word_level = 0, 1
                return non_word_level, word_level
            else:
                return None, None
        elif (len(str1) == 1) & (len(str2) == 3):
            if str2.count(str1) == 1:
                non_word_level, word_level = 1, 0
                return non_word_level, word_level
            else:
                return None, None
        else:
            return None, None

    def find_diff_position_for_replace(self, str1, str2):
        if len(str1) != 3 or len(str2) != 1:
            return None

        for i, char in enumerate(str1):
            if str2 == char:
                diff_index = i
            else:
                continue

        if diff_index == 0:
            diff_index_sem = 1
        if diff_index == 1:
            diff_index_sem = 0
        if diff_index == 2:
            diff_index_sem = 2
        return diff_index, diff_index_sem
    
    def existing_variables(self, elements: list):
        result = [str(element) for element in elements if not isinstance(element, ConstantExpression)]
        return result

    # TODO: Sentence-meaning positions do not necessarily have to correspond
    def chunk01(self):
        rules = self.rules

        chuncked_rules = []
        new_rules = []

        for i in range(len(rules)):
            for j in range(i+1, len(rules)):
                first_sem = Expression.fromstring(rules[i]["lhs"]["sem"])
                second_sem = Expression.fromstring(rules[j]["lhs"]["sem"])
                first_sentence = rules[i]["rhs"]
                second_sentence = rules[j]["rhs"]
                if isinstance(first_sem, ApplicationExpression) & isinstance(second_sem, ApplicationExpression):
                    diff_index, diff_index_sem, can_chunk = self.can_chunk01(rules[i], rules[j])
                    if can_chunk:
                        #print(rules[i])
                        #print(rules[j])
                        assert rules[i]["lhs"]["con"] == rules[j]["lhs"]["con"]
                        con = rules[i]["lhs"]["con"]
                        first_sem_elements = [first_sem.pred, first_sem.args[0], first_sem.args[1]]
                        second_sem_elements = [second_sem.pred, second_sem.args[0], second_sem.args[1]]

                        if "var" in rules[i]:
                            assignments = copy.deepcopy(rules[i]["var"])
                        else:
                            assignments = {}

                        chuncked_rules.append(rules[i])
                        chuncked_rules.append(rules[j])

                        if diff_index_sem == 0:
                            random_category = random.choice(VERB_CATS)
                            var = Expression.fromstring("X")
                        else:
                            # FIX: efficiency
                            random_category = random.choice(NOUN_CATS)
                            existing_variables = self.existing_variables(first_sem_elements)
                            var = [var for var in INDIVIDUAL_VARIABLES if var not in existing_variables][0]
                        first_sem_elements_abstracted = copy.deepcopy(first_sem_elements)
                        first_sem_elements_abstracted[diff_index_sem] = var
                        new_sem_str = f"{str(first_sem_elements_abstracted[0])}({str(first_sem_elements_abstracted[1])},{str(first_sem_elements_abstracted[2])})"
                        # random_category = random.choice(NONTERMINALS)
                        new_sen_str = replace_at_index(first_sentence, diff_index, random_category)
                        assignments[str(var)] = diff_index
                        assignments_sorted = sorted(assignments.items())
                        asignments_sorted_dict = dict((var, idx) for var, idx in assignments_sorted)
                        
                        new_rule_0 = {"lhs": {"cat":"S", "sem": new_sem_str, "con":con}, "rhs": new_sen_str, "var":asignments_sorted_dict}
                        
                        assert self.is_well_formed(new_sem_str, new_sen_str), f"Ill-formed rule generated: {new_rule_0}"
                        assert self.is_well_assigned(new_sen_str, asignments_sorted_dict), f"Ill-assigned rule generated: {new_rule_0}"

                        new_rule_1 = {"lhs": {"cat":random_category, "sem": str(first_sem_elements[diff_index_sem])}, "rhs": first_sentence[diff_index]}
                        new_rule_2 = {"lhs": {"cat":random_category, "sem": str(second_sem_elements[diff_index_sem])}, "rhs": second_sentence[diff_index]}
                        #print("⌄⌄⌄ Chunk1 Results ⌄⌄⌄")
                        #print(new_rule_0)
                        #print(new_rule_1)
                        #print(new_rule_2)
                        #print("⌃⌃⌃ Chunk1 Results ⌃⌃⌃")
                        new_rules += [new_rule_0] + [new_rule_1] + [new_rule_2]
        rules = [rule for rule in rules if rule not in chuncked_rules]
        rules = rules + new_rules
        rules_unique = list(set([str(rule) for rule in rules]))
        self.rules = [self.str2dict(rule) for rule in rules_unique]

    def chunk02(self):
        rules = self.rules

        chuncked_rules = []
        new_rules = []

        for i in range(len(rules)):
            for j in range(i+1, len(rules)):
                first_sem = Expression.fromstring(rules[i]["lhs"]["sem"])
                second_sem = Expression.fromstring(rules[j]["lhs"]["sem"])
                first_sentence = rules[i]["rhs"]
                second_sentence = rules[j]["rhs"]
                if isinstance(first_sem, ApplicationExpression) & isinstance(second_sem, ApplicationExpression):
                    diff_index, diff_index_sem, can_chunk, upper_in_str, lower_in_str = self.can_chunk02(rules[i], rules[j])
                    if can_chunk:
                        assert rules[i]["lhs"]["con"] == rules[j]["lhs"]["con"]
                        con = rules[i]["lhs"]["con"]
                        first_sem_elements = [first_sem.pred, first_sem.args[0], first_sem.args[1]]
                        second_sem_elements = [second_sem.pred, second_sem.args[0], second_sem.args[1]]

                        target_position = [i,j][lower_in_str]
                        nontarget_position = [i,j][upper_in_str]
                        chuncked_rules.append(rules[target_position])

                        target_sem = Expression.fromstring(rules[target_position]["lhs"]["sem"])
                        target_sem_elements = [target_sem.pred, target_sem.args[0], target_sem.args[1]]
                        target_sentence = rules[target_position]["rhs"]
                        nontarget_sentence = rules[nontarget_position]["rhs"]
                        new_rule = {"lhs": {"cat":nontarget_sentence[diff_index], "sem": str(target_sem_elements[diff_index_sem])}, "rhs": target_sentence[diff_index]}
                        new_rules.append(new_rule)
                        # print(new_rule)
        rules = [rule for rule in rules if rule not in chuncked_rules]
        rules = rules + new_rules
        rules_unique = list(set([str(rule) for rule in rules]))
        self.rules = [self.str2dict(rule) for rule in rules_unique]
        
    def abstract(self, element, var, idx, diff_idx):
        if idx == diff_idx:
            return var
        else:
            return element
    
    def can_replace(self, rule1, rule2):
        str1, str2 = rule1["rhs"], rule2["rhs"]
        cat1, cat2 = rule1["lhs"]["cat"], rule2["lhs"]["cat"]
        sem1_logic = Expression.fromstring(rule1["lhs"]["sem"])
        sem2_logic = Expression.fromstring(rule2["lhs"]["sem"])
        
        if (cat1 == "S") and (cat2 != "S"):
            sem1, sem2 = [sem1_logic.pred, sem1_logic.args[0], sem1_logic.args[1]], sem2_logic
            same_positions_str = []
            same_positions_sem = []
            for i, char in enumerate(str1):
                if str2 == char:
                    same_positions_str.append(i)
            for i, elm in enumerate(sem1):
                if sem2 == elm:
                    same_positions_sem.append(i)
            if len(same_positions_str) == len(same_positions_sem) > 0:
                return True, same_positions_str[0], same_positions_sem[0], 0, 1
                # 0: non-word-rule, 1: word-rule
            else:
                return False, None, None, None, None
        elif (cat2 == "S") and (cat1 != "S"):
            sem2, sem1 = [sem2_logic.pred, sem2_logic.args[0], sem2_logic.args[1]], sem1_logic
            same_positions_str = []
            same_positions_sem = []
            for i, char in enumerate(str2):
                if str1 == char:
                    same_positions_str.append(i)
            for i, elm in enumerate(sem2):
                if sem1 == elm:
                    same_positions_sem.append(i)
            if len(same_positions_str) == len(same_positions_sem) > 0:
                return True, same_positions_str[0], same_positions_sem[0], 1, 0
                # 1: non-word-rule, 0: word-rule
            else:
                return False, None, None, None, None
        else:
            return False, None, None, None, None

    def replace(self):
        rules = self.rules

        replaced_rules = []
        new_rules = []

        for i in range(len(rules)):
            for j in range(i+1, len(rules)):
                # first_sem = Expression.fromstring(rules[i]["lhs"]["sem"])
                # second_sem = Expression.fromstring(rules[j]["lhs"]["sem"])
                first_sentence = rules[i]["rhs"]
                second_sentence = rules[j]["rhs"]
                # non_word_level, word_level = self.highlight_for_replace(first_sentence, second_sentence)
                can_replace, same_index_str, same_index_sem, sentence_level, word_level = self.can_replace(rules[i], rules[j])
                if can_replace:
                    # print(rules[i])
                    # print(rules[j])
                    sentencerule_index = [i,j][sentence_level]
                    wordrule_index = [i,j][word_level]
                    sentencerule = rules[sentencerule_index]
                    wordrule = rules[wordrule_index]
                    replaced_rules.append(sentencerule)
                    sentencerule_sem = Expression.fromstring(sentencerule["lhs"]["sem"])
                    sentencerule_sem_elms = [sentencerule_sem.pred, sentencerule_sem.args[0], sentencerule_sem.args[1]]
                    
                    if "var" in sentencerule:
                        assignments = copy.deepcopy(sentencerule["var"])
                    else:
                        assignments = {}
                    
                    if same_index_sem == 0:
                        var = Expression.fromstring("X")
                    else:
                        # FIX: efficiency
                        # existing_variables = self.existing_variables(sentencerule_sem_elms)
                        # print([var for var in INDIVIDUAL_VARIABLES if var not in existing_variables])
                        var = [var for var in INDIVIDUAL_VARIABLES if var not in assignments][0]
                    sentencerule_rhs = sentencerule["rhs"]
                    abstracted_sem_elms = []
                    for i, elm in enumerate(sentencerule_sem_elms):
                        if i == same_index_sem:
                            abstracted_sem_elms.append(var)
                        else:
                            abstracted_sem_elms.append(sentencerule_sem_elms[i])
                    abstracted_sem = f"{str(abstracted_sem_elms[0])}({str(abstracted_sem_elms[1])},{abstracted_sem_elms[2]})"

                    sentencerule_con = sentencerule["lhs"]["con"]

                    assignments[str(var)] = same_index_str
                    assignments_sorted = sorted(assignments.items())
                    asignments_sorted_dict = dict((var, idx) for var, idx in assignments_sorted)

                    wordrule_rhs = wordrule["rhs"]
                    wordrule_cat = wordrule["lhs"]["cat"]
                    abstracted_sentencerule_rhs = sentencerule_rhs.replace(wordrule_rhs, wordrule_cat)
                    
                    new_rule = {"lhs": {"cat":"S", "sem":abstracted_sem, "con":sentencerule_con}, "rhs": abstracted_sentencerule_rhs, "var":asignments_sorted_dict}
                    
                    assert self.is_well_formed(abstracted_sem, abstracted_sentencerule_rhs), f"Ill-formed rule generated: {new_rule}"
                    assert self.is_well_assigned(abstracted_sentencerule_rhs, asignments_sorted_dict), f"Ill-assigned rule generated: \nBefore:\t{sentencerule}\n\t{wordrule}\nAfter: {new_rule}"
                    
                    # print("Replace result: ", new_rule)
                    new_rules.append(new_rule)
        rules = [rule for rule in rules if rule not in replaced_rules]
        rules = rules + new_rules
        rules_unique = list(set([str(rule) for rule in rules]))
        self.rules = [self.str2dict(rule) for rule in rules_unique]
    
    def repaint_rule(self, rule, replacee, replacer):
        print(f"Before Merge: {rule}")
        # print(rule, replacee, replacer)
        if rule["lhs"]["cat"] == replacee["lhs"]["cat"]:
            assert len(rule["rhs"]) == 1
            # print(rule["lhs"]["cat"], "->",replacer["lhs"]["cat"])
            rule["lhs"]["cat"] = replacer["lhs"]["cat"]
        else:
            rhs = copy.deepcopy(rule["rhs"])
            new_rhs = rhs.replace(replacee["lhs"]["cat"], replacer["lhs"]["cat"])
            rule["rhs"] = new_rhs
            # print(rhs, "->", new_rhs)
        assert self.is_well_formed(rule["lhs"]["sem"], rule["rhs"]), f"Ill-formed rule generated: {rule}"
        if "var" in rule:
            assert self.is_well_assigned(rule["rhs"], rule["var"]), f"Ill-assigned rule generated: {rule}"
        print(f"After Merge: {rule}")
        return rule
    
    def is_WordRule(self, rule):
        assert type(rule) == dict
        if rule["lhs"]["cat"] == "S":
            return False # SentenceRule
        else:
            return True # WordRule

    def can_merge(self, rule1, rule2):
        rule1_cat = copy.deepcopy(rule1["lhs"]["cat"])
        rule1_sem = copy.deepcopy(rule1["lhs"]["sem"])
        rule1_rhs = copy.deepcopy(rule1["rhs"])
        rule2_cat = copy.deepcopy(rule2["lhs"]["cat"])
        rule2_sem = copy.deepcopy(rule2["lhs"]["sem"])
        rule2_rhs = copy.deepcopy(rule2["rhs"])
        if self.is_WordRule(rule1) and self.is_WordRule(rule2):
            if (rule1_sem == rule2_sem) & (rule1_rhs == rule2_rhs) & (rule1_cat != rule2_cat):
                cats = [rule1_cat, rule2_cat]
                random.shuffle(cats)
                selected_cat = cats[0]
                deleted_cat = cats[1]
                assert (selected_cat.isupper()) and (deleted_cat.isupper())
                return True, selected_cat, deleted_cat
            else:
                return False, None, None
        else:
            return False, None, None
        
    def merge(self):
        for i in range(len(self.rules)):
            for j in range(i+1, len(self.rules)):
                can_merge, selected_cat, deleted_cat = self.can_merge(self.rules[i], self.rules[j])
                if can_merge:
                    for rule in self.rules:
                        rule["lhs"]["cat"] = rule["lhs"]["cat"].replace(deleted_cat, selected_cat)
                        rule["rhs"] = rule["rhs"].replace(deleted_cat, selected_cat)
                        assert self.is_well_formed(rule["lhs"]["sem"], rule["rhs"]), f"Ill-formed rule generated: {rule}"
                        if "var" in rule:
                            assert self.is_well_assigned(rule["rhs"], rule["var"]), f"Ill-assigned rule generated: {rule}"
        rules = self.rules
        rules_unique = list(set([str(rule) for rule in rules]))
        self.rules = [self.str2dict(rule) for rule in rules_unique]

    def leg_merge(self):
        rules = self.rules
        invited = []
        replacer_cats = []
        for i in range(len(rules)):
            for j in range(i+1, len(rules)):
                if self.can_merge(rules[i], rules[j]):
                    # print(f"can merge {rules[i]} and {rules[j]}")
                    if (rules[i]["lhs"]["cat"] not in replacer_cats) and (rules[j]["lhs"]["cat"] not in replacer_cats):
                        indices = [i, j]
                        # print(indices)
                        random.shuffle(indices)
                        replacer_rule = copy.deepcopy(rules[indices[0]])
                        replacee_rule = copy.deepcopy(rules[indices[1]])
                        replacer_cats.append(replacer_rule["lhs"]["cat"])
                        # print("replacee_rule: ", replacee_rule)
                        # print("replacer_rule: ", replacer_rule)
                        rules = [self.repaint_rule(rule, replacee_rule, replacer_rule) for rule in rules]
                    elif (rules[i]["lhs"]["cat"] in replacer_cats) and (rules[j]["lhs"]["cat"] in replacer_cats):
                        continue
                    elif rules[i]["lhs"]["cat"] in replacer_cats:
                        replacer_rule = copy.deepcopy(rules[i])
                        replacee_rule = copy.deepcopy(rules[j])
                        # print("replacee_rule: ", replacee_rule)
                        # print("replacer_rule: ", replacer_rule)
                        rules = [self.repaint_rule(rule, replacee_rule, replacer_rule) for rule in rules]
                    else:
                        replacer_rule = copy.deepcopy(rules[j])
                        replacee_rule = copy.deepcopy(rules[i])
                        # print("replacee_rule: ", replacee_rule)
                        # print("replacer_rule: ", replacer_rule)
                        rules = [self.repaint_rule(rule, replacee_rule, replacer_rule) for rule in rules]
                else:
                    continue
        for rule in rules:
            assert self.is_well_formed(rule["lhs"]["sem"], rule["rhs"]), f"Ill-formed rule generated: {rule}"
            if "var" in rule:
                assert self.is_well_assigned(rule["rhs"], rule["var"]), f"Ill-assigned rule generated: {rule}"
        rules_unique = list(set([str(rule) for rule in rules]))
        self.rules = [self.str2dict(rule) for rule in rules_unique]

    def invent_wordrule(self, sem):
        if str(sem).replace("_","") in NOUNS:
            random_category = random.choice(NOUN_CATS)
            rhs = generate_noun(5, ["x", "y"])
        if str(sem).replace("_","") in (VERBS+VERBS_PSS):
            random_category = random.choice(VERB_CATS)
            rhs = generate_verb(5)
        self.add_rule(f"{random_category}/{str(sem)} -> {rhs}")
        return rhs

    def invent_holisticrule(self, sem, query_con):
        subj = generate_noun(5, ["x", "y"])
        obj = generate_noun(5, [subj, "x", "y"])
        verb = generate_verb(5)
        sentence = f"{subj}{verb}{obj}"
        self.add_rule(f"S/{sem}/{query_con} -> {sentence}")
        return sentence
    # TODO: test
    def generate(self, query_str, query_con, debug=False):
        rules = self.rules

        if debug:
            print("query: ", query_str)

        query = Expression.fromstring(query_str)
        query_elements = [query.args[0], query.pred, query.args[1]]

        sem_list = self.sem_list()
        sentence_list = self.sentence_list()

        if (query_str in sem_list) and (rules[sem_list.index(query_str)]['lhs']['con']==query_con):
            holistic_rule = rules[sem_list.index(query_str)]
            holistic_rule_rhs = holistic_rule['rhs']
            if debug:
                print("generated by a holictic rule: ", f"S/{str(query)}/{query_con} -> {holistic_rule_rhs}")
            return f"S/{str(query)}/{query_con} -> {holistic_rule_rhs}", "by-holistic-rule"
        else:
            for i, sem_str in enumerate(sem_list):
                sem = Expression.fromstring(sem_str)
                if isinstance(sem, ApplicationExpression):
                    rule = rules[i]
                    con = rule["lhs"]["con"]
                    sem_elements = [sem.args[0], sem.pred, sem.args[1]]
                    matches = [(i, (query_element,sem_element)) for i, (query_element,sem_element) in enumerate(zip(query_elements, sem_elements)) if (query_element==sem_element) & (isinstance(query_element, ConstantExpression) & isinstance(sem_element, ConstantExpression))]
                    slots = [(i, (query_element,sem_element)) for i, (query_element,sem_element) in enumerate(zip(query_elements, sem_elements)) if (query_element!=sem_element) & (not isinstance(sem_element, ConstantExpression))]
                    if (len(matches)==2) & (len(slots)==1) & (query_con==con):
                        sentence_with_slot = sentence_list[i]
                        slot_position = slots[0][0]
                        slot_sem = slots[0][1][0]
                        slot_var_sem = slots[0][1][1]
                        substitute_position = rule["var"][str(slot_var_sem)]
                        slot_category = sentence_with_slot[substitute_position]
                        word_rules = [rule for rule in rules if (rule['lhs']['cat']==slot_category) & (rule['lhs']['sem']==str(slot_sem))]
                        if len(word_rules) > 0:
                            selected_rule = self.str2dict(str(random.sample(word_rules, 1)[0]))
                            if substitute_position == 0:
                                generated_sentence = selected_rule['rhs'] + sentence_with_slot[1:]
                            if substitute_position == 1:
                                generated_sentence = sentence_with_slot[0] + selected_rule['rhs'] + sentence_with_slot[2]
                            if substitute_position == 2:
                                generated_sentence = sentence_with_slot[:2] + selected_rule['rhs']
                            assert generated_sentence.islower()
                            return f"S/{str(query)}/{query_con} -> {generated_sentence}", "by-composition"
                        if len(word_rules) == 0:
                            invented_form = self.invent_wordrule(slot_sem)
                            if substitute_position == 0:
                                generated_sentence = invented_form + sentence_with_slot[1:]
                            if substitute_position == 1:
                                generated_sentence = sentence_with_slot[0] + invented_form + sentence_with_slot[2]
                            if substitute_position == 2:
                                generated_sentence = sentence_with_slot[:2] + invented_form
                            assert generated_sentence.islower()
                            return f"S/{str(query)}/{query_con} -> {generated_sentence}", "by-word-invention"
                    if (len(matches)==1) & (len(slots)==2) & (query_con==con):
                        sentence_with_slot = sentence_list[i]
                        slot_position = slots[0][0]
                        slot_sem = slots[0][1][0]
                        slot_var_sem = slots[0][1][1]
                        substitute_position = rule["var"][str(slot_var_sem)]
                        slot_category = sentence_with_slot[substitute_position]
                        word_rules = [rule for rule in rules if (rule['lhs']['cat']==slot_category) & (rule['lhs']['sem']==str(slot_sem))]
                        if len(word_rules) > 0:
                            selected_rule = self.str2dict(str(random.sample(word_rules, 1)[0]))
                            if substitute_position == 0:
                                new_sentence_with_slot = selected_rule['rhs'] + sentence_with_slot[1:]
                            if substitute_position == 1:
                                new_sentence_with_slot = sentence_with_slot[0] + selected_rule['rhs'] + sentence_with_slot[2]
                            if substitute_position == 2:
                                new_sentence_with_slot = sentence_with_slot[:2] + selected_rule['rhs']
                            strategy = "by-composition"
                        if len(word_rules) == 0:
                            invented_form = self.invent_wordrule(slot_sem)
                            if substitute_position == 0:
                                new_sentence_with_slot = invented_form + sentence_with_slot[1:]
                            if substitute_position == 1:
                                new_sentence_with_slot = sentence_with_slot[0] + invented_form + sentence_with_slot[2]
                            if substitute_position == 2:
                                new_sentence_with_slot = sentence_with_slot[:2] + invented_form
                            strategy = "by-word-invention"
                        slot_position = slots[1][0]
                        slot_sem = slots[1][1][0]
                        slot_var_sem = slots[1][1][1]
                        substitute_position = rule["var"][str(slot_var_sem)]
                        slot_category = sentence_with_slot[substitute_position]
                        word_rules = [rule for rule in rules if (rule['lhs']['cat']==slot_category) & (rule['lhs']['sem']==str(slot_sem))]
                        if len(word_rules) > 0:
                            selected_rule = self.str2dict(str(random.sample(word_rules, 1)[0]))
                            if substitute_position == 0:
                                generated_sentence = selected_rule['rhs'] + new_sentence_with_slot[1:]
                            if substitute_position == 1:
                                generated_sentence = new_sentence_with_slot[0] + selected_rule['rhs'] + new_sentence_with_slot[2]
                            if substitute_position == 2:
                                generated_sentence = new_sentence_with_slot[:2] + selected_rule['rhs']
                            assert generated_sentence.islower()
                            if strategy == "by-composition":
                                return f"S/{str(query)}/{query_con} -> {generated_sentence}", strategy
                            else:
                                return f"S/{str(query)}/{query_con} -> {generated_sentence}", strategy
                        if len(word_rules) == 0:
                            if strategy == "by-composition":
                                invented_form = self.invent_wordrule(slot_sem)
                                if substitute_position == 0:
                                    generated_sentence = invented_form + new_sentence_with_slot[1:]
                                if substitute_position == 1:
                                    generated_sentence = new_sentence_with_slot[0] + invented_form + new_sentence_with_slot[2]
                                if substitute_position == 2:
                                    generated_sentence = new_sentence_with_slot[:2] + invented_form
                                assert generated_sentence.islower(), query_str
                                strategy = "by-word-invention"
                                return f"S/{str(query)}/{query_con} -> {generated_sentence}", strategy
                            else:
                                self.rules = self.rules[:-1]
                                generated_sentence = self.invent_holisticrule(query, query_con)
                                assert generated_sentence.islower()
                                return f"S/{str(query)}/{query_con} -> {generated_sentence}", "by-holistic-invention"
                    if (len(matches)==0) & (len(slots)==3) & (query_con==con):
                        sentence_with_slot = sentence_list[i]
                        slot_position = slots[0][0]
                        slot_sem = slots[0][1][0]
                        slot_var_sem = slots[0][1][1]
                        substitute_position = rule["var"][str(slot_var_sem)]
                        slot_category = sentence_with_slot[substitute_position]
                        word_rules = [rule for rule in rules if (rule['lhs']['cat']==slot_category) & (rule['lhs']['sem']==str(slot_sem))]
                        if len(word_rules) > 0:
                            selected_rule = self.str2dict(str(random.sample(word_rules, 1)[0]))
                            if substitute_position == 0:
                                new_sentence_with_slot = selected_rule['rhs'] + sentence_with_slot[1:]
                            if substitute_position == 1:
                                new_sentence_with_slot = sentence_with_slot[0] + selected_rule['rhs'] + sentence_with_slot[2]
                            if substitute_position == 2:
                                new_sentence_with_slot = sentence_with_slot[:2] + selected_rule['rhs']
                            strategy = "by-composition"
                        if len(word_rules) == 0:
                            invented_form = self.invent_wordrule(slot_sem)
                            if substitute_position == 0:
                                new_sentence_with_slot = invented_form + sentence_with_slot[1:]
                            if substitute_position == 1:
                                new_sentence_with_slot = sentence_with_slot[0] + invented_form + sentence_with_slot[2]
                            if substitute_position == 2:
                                new_sentence_with_slot = sentence_with_slot[:2] + invented_form
                            strategy = "by-word-invention"
                        slot_sem = slots[1][1][0]
                        slot_var_sem = slots[1][1][1]
                        substitute_position = rule["var"][str(slot_var_sem)]
                        slot_category = sentence_with_slot[substitute_position]
                        word_rules = [rule for rule in rules if (rule['lhs']['cat']==slot_category) & (rule['lhs']['sem']==str(slot_sem))]
                        if len(word_rules) > 0:
                            selected_rule = self.str2dict(str(random.sample(word_rules, 1)[0]))
                            if substitute_position == 0:
                                new_sentence_with_slot = selected_rule['rhs'] + new_sentence_with_slot[1:]
                            if substitute_position == 1:
                                new_sentence_with_slot = new_sentence_with_slot[0] + selected_rule['rhs'] + new_sentence_with_slot[2]
                            if substitute_position == 2:
                                new_sentence_with_slot = new_sentence_with_slot[:2] + selected_rule['rhs']
                        if len(word_rules) == 0:
                            if strategy == "by-composition":
                                invented_form = self.invent_wordrule(slot_sem)
                                if substitute_position == 0:
                                    new_sentence_with_slot = invented_form + new_sentence_with_slot[1:]
                                if substitute_position == 1:
                                    new_sentence_with_slot = new_sentence_with_slot[0] + invented_form + new_sentence_with_slot[2]
                                if substitute_position == 2:
                                    new_sentence_with_slot = new_sentence_with_slot[:2] + invented_form
                                strategy = "by-word-invention"
                            else:
                                self.rules = self.rules[:-1]
                                generated_sentence = self.invent_holisticrule(query, query_con)
                                assert generated_sentence.islower()
                                return f"S/{str(query)}/{query_con} -> {generated_sentence}", "by-holistic-invention"
                        slot_position = slots[2][0]
                        slot_sem = slots[2][1][0]
                        slot_var_sem = slots[2][1][1]
                        substitute_position = rule["var"][str(slot_var_sem)]
                        slot_category = sentence_with_slot[substitute_position]
                        word_rules = [rule for rule in rules if (rule['lhs']['cat']==slot_category) & (rule['lhs']['sem']==str(slot_sem))]
                        if len(word_rules) > 0:
                            selected_rule = self.str2dict(str(random.sample(word_rules, 1)[0]))
                            if substitute_position == 0:
                                generated_sentence = selected_rule['rhs'] + new_sentence_with_slot[1:]
                            if substitute_position == 1:
                                generated_sentence = new_sentence_with_slot[0] + selected_rule['rhs'] + new_sentence_with_slot[2]
                            if substitute_position == 2:
                                generated_sentence = new_sentence_with_slot[:2] + selected_rule['rhs']
                            assert generated_sentence.islower()
                            return f"S/{str(query)}/{query_con} -> {generated_sentence}", strategy
                        if len(word_rules) == 0:
                            if strategy == "by-composition":
                                invented_form = self.invent_wordrule(slot_sem)
                                if substitute_position == 0:
                                    generated_sentence = invented_form + new_sentence_with_slot[1:]
                                if substitute_position == 1:
                                    generated_sentence = new_sentence_with_slot[0] + invented_form + new_sentence_with_slot[2]
                                if substitute_position == 2:
                                    generated_sentence = new_sentence_with_slot[:2] + invented_form
                                strategy = "by-word-invention"
                                assert generated_sentence.islower()
                                return f"S/{str(query)}/{query_con} -> {generated_sentence}", strategy
                            else:
                                self.rules = self.rules[:-1]
                                generated_sentence = self.invent_holisticrule(query, query_con)
                                assert generated_sentence.islower()
                                return f"S/{str(query)}/{query_con} -> {generated_sentence}", "by-holistic-invention"
                    else:
                        continue
                else:
                    continue
            generated_sentence = self.invent_holisticrule(query, query_con)
            assert generated_sentence.islower()
            return f"S/{str(query)}/{query_con} -> {generated_sentence}", "by-holistic-invention"