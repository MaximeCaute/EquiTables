"""
Author: Maxime Cauté
Created: 31/03/2021

This file is dedicated to the implementation and selection of global heuristics.
Heuristics are functions that take a node and return a boolean.
This boolean reflects wether or not the search should be continued from this node.
Defined heuristics should be added to the ALLOWED_GLOBAL_HEURISTIC_NAMES dictionnary with their name.
"""

def search_full_tree(node):
    return True

def positive_local_score(local_heuristic, node):
    _, _, _, score = local_heuristic(node)
    return score >= 0

def threshold_score(local_heuristic, node):
    _, _, _, score = local_heuristic(node)
    return score >= 0.5

ALLOWED_GLOBAL_HEURISTIC_NAMES = {
    'full_tree': lambda h: search_full_tree,
    'positive_score': lambda h : lambda node : positive_local_score(h,node),
    'absolute_threshold': lambda h : lambda node : positive_local_score(h,node)
}

def get_global_heuristic_by_name(heuristic_name, local_heuristic = None):
    """
    This function retrieves a given global heuristic by its name.
    If this heuristic depends on a local_heuristic,
    the latter can be precised to define it already,
    otherwised the returned heuristic will be a lambda function of a local_heuristic.
    If the name is not valid, returns "full_tree" heuristic,
    and raises a warning.
    --
    Input:
        - heuristic_name: string. The name of the heuristic.
            Current possible options are:
                + full_tree.
    Parameters
    Outputs:
        - global_heuristic: global_heuristic. The chosen global heuristic.
            Is "full_tree" heuristic by default for invalid names.

    """
    if heuristic_name in ALLOWED_GLOBAL_HEURISTIC_NAMES:
        return  ALLOWED_GLOBAL_HEURISTIC_NAMES[heuristic_name](local_heuristic)
    default_global_heuristic_name = list(ALLOWED_GLOBAL_HEURISTIC_NAMES.keys())[0]
    print(  f"WARNING: invalid name - {heuristic_name}!\n"+
            f"Resolving to default heuristic '{default_global_heuristic_name}'.")
    return ALLOWED_GLOBAL_HEURISTIC_NAMES[default_local_heuristic_name]
