from nltk.sem.logic import *

def nltk2list(expr):
    if type(expr) == str:
        expr_nltk = Expression.fromstring(expr)
        result = [expr_nltk.pred, expr_nltk.args[0], expr_nltk.args[1]]
    else:
        result = [expr.pred, expr.args[0], expr.args[1]]
    return result

def sem_distance(sem1, sem2):
    sem1_list, sem2_list = nltk2list(sem1), nltk2list(sem2)
    assert len(sem1_list) == len(sem2_list) == 3
    is_diff = [sem1 != sem2 for sem1, sem2 in zip(sem1_list, sem2_list)]
    result = sum(is_diff) / len(sem1_list)
    return result