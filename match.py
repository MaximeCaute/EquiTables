#!/usr/bin/env python3
# -*- coding: utf-8 -*-
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
import global_heuristics
import preprocessing
from search_tree import SearchTree


def split_by_labels(df, factors):
    """
    Splits a dataframe according to the subgroups obtained
    by crossing the columns listed in factors.
    Each subgroup thus matches a given n-uple of values along these factors.
    It then proceeds to drop the factors.
    --
    Input:
        - df: pd.DataFrame. The dataframe to split.
        - factors: string list.
            The name of the columns to split the dataframe over.
    Output:
        - grouped_df: pd.DataFrameGroupBy.
            The dataframe grouped by factored groups.
    """
    x = df[factors].astype(str).agg('-'.join, axis=1)  # merge columns
    return df.drop(factors, axis=1).groupby(x)


def find_matched_subgroups(grouped_dataframe,
                           columns_to_match,
                           local_heuristic,
                           global_heuristic,
                           subgroup_size=2):
    """
    Computes matched subgroups from a grouped dataframe.
    --
    Input:
        - grouped_dataframe: pd.DataFrameGroupBy.
            The grouped dataframe to compute subgroups from.
        - columns_to_match: string_list. The columns to match the subgroups on.
        - local_heuristic: local heuristic.
            The local heuristic to use in the search.
            See EquiTables.local_heuristics for details
        - global_heuristic: global heuristic.
            The global heuristic to use in the search.
            See EquiTables.global_heuristics for details
    Parameters:
        - subgroup_size: int. The size of the subgroups to compute.
            Defaults to 2.
    Outputs:
        - subgrouped_dataframe: pd.DataFrameGroupBy.
            The dataframe made of the subgroups of the original dataframe.
            Non-grouped elements have been removed.
    """
    search_tree = SearchTree(grouped_dataframe, subgroup_size)
    subgrouped_dataframe = search_tree.search_and_get_solution( local_heuristic,
                                                                global_heuristic)
    return subgrouped_dataframe

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

    allowed_local_heuristic_names = list(
        local_heuristics.ALLOWED_LOCAL_HEURISTIC_NAMES.keys())
    allowed_global_heuristic_names = list(
        global_heuristics.ALLOWED_GLOBAL_HEURISTIC_NAMES.keys()
    )
    optional.add_argument(
        "-h",
        "--local_heuristic_name",
        type=str,
        default=allowed_local_heuristic_names[0],
        help="The name of the local heuristic to use. " +
        f"Allowed options are {str(allowed_local_heuristic_names)}. " +
        f"Defaults to '{str(allowed_local_heuristic_names[0])}'. ")

    optional.add_argument(
        "-b",
        "--global_heuristic_name",
        type=str,
        default=allowed_global_heuristic_names[0],
        help="The name of the global (branch) heuristic to use. " +
        f"Allowed options are {str(allowed_global_heuristic_names)}. " +
        f"Defaults to '{str(allowed_global_heuristic_names[0])}'. ")


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

    global_heuristic = global_heuristics.get_global_heuristic_by_name(
        args.global_heuristic_name, local_heuristic)


    df = preprocessing.drop_non_relevant_columns(df,  variables_to_match+grouping_factors)
    grouped_dataframe = split_by_labels(df, grouping_factors)
    subgrouped_dataframe = find_matched_subgroups(grouped_dataframe,
                                                    variables_to_match,
                                                    local_heuristic,
                                                    global_heuristic,
                                                    subsets_size)

    for i, subgroup_dataframe in enumerate(subgrouped_dataframe):
        pd.DataFrame(subgroup_dataframe).to_csv(op.join(args.save_path, f'subgroup_{i + 1:02d}.csv'))
