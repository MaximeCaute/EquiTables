#! /usr/bin/env python
"""
Author(s): Maxime Cauté
Created: 03.03.2021
Modifs:  Time-stamp: <2021-04-12 15:39:30 christophe@pallier.org>

This file is the main .py file for the match program.
Github repository: https://github.com/MaximeCaute/Equitables
"""

import os.path as op
import argparse
import pandas as pd

import local_heuristics
from search_tree import SearchTree


def split_by_labels(df, factors):
    """ split dataframe df according to
    the subgroups obtained by crossing the columns listed in factors
    and drop factors"""
    x = df[factors].astype(str).agg('-'.join, axis=1)  # merge columns
    return df.drop(factors, axis=1).groupby(x)


def find_matched_subgroups(groups,
                           columns_to_match,
                           local_heuristic,
                           subgroup_size=2):
    """
    Extract subgroups' from a list of data.frames (groups), matched on `columns_to_match`

    Input:
        - groups :  list of pandas DataFrame

    Parameters:
        - subgroup_size: int     size of the subgroups to extract.

    Outputs:
        a list of dataframes of length subgroup_size

    """
    #### TBD  # needs modificatoins in searchtree

    search_tree = SearchTree(groups, subgroup_size)
    subgroups = search_tree.search_and_get_solution(local_heuristic = local_heuristic)
    # subgroups = groups  # no selection"
    return subgroups


def get_arguments():
    return args


if __name__ == "__main__":
    """
    Upon being executed, returns a subset from (WIP)

    ---
    Call example:
        - python3 match.py ToySets/toy_data.csv -m Value -g Control -s 2
        - python3 match.py ToySets/toy_data.csv -m Value -g Control -s 2 -p results/
        - python3 match.py ToySets/toy_data_expanded.csv -m Value -g "Control;Paradigm1;Paradigm2" -s 2 -p results/
        - python3 match.py ToySets/toy_data_expanded.csv -m Value -g "Control;Paradigm1;Paradigm2" -h first_possible -s 2 -p results/
    """

    parser = argparse.ArgumentParser(add_help=False)

    required = parser.add_argument_group('required arguments')
    optional = parser.add_argument_group('optional arguments')

    required.add_argument("DATAFILE",
                          type=argparse.FileType('r'),
                          help="Acsv datafile to select matching sets from.")

    required.add_argument("-m",
                          "--match",
                          type=str,
                          help="variables to match. Separate with ';'. " +
                          "Names should match the data column names. ",
                          required=True)
    required.add_argument("-g",
                          "--group",
                          type=str,
                          help="grouping variables. Separate with ';'. " +
                          "Names should match the data column names. ",
                          required=True)
    required.add_argument("-s",
                          "--subset_size",
                          type=int,
                          help="The size of the data subset to return. ",
                          required=True)

    allowed_heuristic_names = list(
        local_heuristics.ALLOWED_LOCAL_HEURISTIC_NAMES.keys())
    optional.add_argument(
        "-h",
        "--local_heuristic_name",
        type=str,
        default=allowed_heuristic_names[0],
        help="The name of the local heuristic to use. " +
        f"Allowed options are {str(allowed_heuristic_names)}. " +
        f"Defaults to '{str(allowed_heuristic_names[0])}'. ")

    optional.add_argument("-d",
                          "--delimiter",
                          type=str,
                          default=";",
                          help="The delimiter for the .csv data file. " +
                          "Defaults to ';'.")
    optional.add_argument("-p",
                          "--save_path",
                          type=str,
                          default="",
                          help="The path to where to save the results, " +
                          "from the current folder. " +
                          "Defaults to current folder. ")
    args = parser.parse_args()

    df = pd.read_csv(args.DATAFILE, sep=args.delimiter)
    variables_to_match = args.match.split(";")
    grouping_factors = args.group.split(";")
    subsets_size = args.subset_size

    local_heuristic = local_heuristics.get_local_heuristic_by_name(
        args.local_heuristic_name)

    groups = split_by_labels(df, grouping_factors)

    subgroups = find_matched_subgroups(groups,
                                       variables_to_match,
                                       local_heuristic,
                                       subsets_size)

    for i, subgroup in enumerate(subgroups):
        pd.DataFrame(subgroup).to_csv(op.join(args.save_path, f'subgroup_{i + 1:02d}.csv'))
