"""
Author(s): Maxime Cauté
Created: 03.03.2021

This file is the main .py file for the match program.
Github repository: https://github.com/MaximeCaute/Equitables

The input to the program should be as follow:
    - a .csv file containing all the data with the relevant information;
    - a .txt file listing out parameters to match;
    - a .txt file listing out parameters to differentiate;
"""

import argparse
import pandas

import data_spliter
import local_heuristics

def get_arguments():
    """
    This function parses command line arguments.
    --
    Output:
        - args: list. The list of the arguments.
    """
    parser = argparse.ArgumentParser()

    parser.add_argument("datafile", type = argparse.FileType('r'),
                        help = "The data to select matching sets from. Should follow .csv format.")

    # Optional arguments
    parser.add_argument("-mp", "--matching_parameters", type = str,
                        default = "",
                        help = "The parameters to match. Separate with ';'. "
                        + "Names should match the data column names. "
                        + "Defaults to none.")
    parser.add_argument("-dp", "--differentiation_parameters", type = str,
                        default = "",
                        help = "The parameters to differentiate. Separate with ';'. "
                        + "Names should match the data column names. "
                        + "Defaults to none.")

    parser.add_argument("-lh", "--local_heuristic_name", type = str,
                        default = "first_possible",
                        help = "The name of the local heuristic to use."
                        + f"Allowed options are {str(ALLOWED_HEURISTIC_NAMES)}."
                        + f"Defaults to '{str(ALLOWED_HEURISTIC_NAMES[0])}'.")

    parser.add_argument("-d", "--delimiter", type = str,
                        default = ";",
                        help = "The delimiter for the .csv data file. "
                        + "Defaults to ';'.")
    parser.add_argument("-s", "--subset_size", type = int,
                        default = "50",
                        help = "The size of the data subset to return. "
                        + "Defaults to 50")
    parser.add_argument("-p", "--save_path", type = str,
                        default = "",
                        help = "The path to where to save the results, "
                        +"from the current folder. "
                        +"Defaults to current folder.")
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    """
    Upon being executed, returns a subset from (WIP)

    ---
    Call example:
        - python3 match.py ToySets/toy_data.csv -mp Value -dp Control -s 2
        - python3 match.py ToySets/toy_data.csv -mp Value -dp Control -s 2 -p results/
        - python3 match.py ToySets/toy_data_expanded.csv -mp Value -dp "Control;Paradigm1;Paradigm2" -s 2 -p results/
        - python3 match.py ToySets/toy_data_expanded.csv -mp Value -dp "Control;Paradigm1;Paradigm2" -lh first_possible -s 2 -p results/
    """
    SAVE_NAME = "data_group"
    LOCAL_HEURISTIC_NAME = "first_possible"
    #Note: first is default!
    ALLOWED_HEURISTIC_NAMES = ['first_possible']

    args = get_arguments()
    with args.datafile as datafile:
        dataframe = pandas.read_csv(datafile, sep = args.delimiter)

    parameters_to_match = args.matching_parameters.split(";")
    parameters_to_differentiate = args.differentiation_parameters.split(";")

    data_to_match = dataframe[parameters_to_match]
    data_to_differentiate = dataframe[parameters_to_differentiate]

    local_heuristic = local_heuristics.get_local_heuristic_by_name(
            args.local_heuristic_name
    )
    subgroups_indices = data_spliter.compute_subgroups_indices(
                                    data_to_match,
                                    data_to_differentiate,
                                    local_heuristic,
                                    groups_size = args.subset_size)

    for i, subgroup_indices in enumerate(subgroups_indices):
        subgroup_data = dataframe.iloc[subgroup_indices]

        #More explicit name?
        path = args.save_path+SAVE_NAME+str(i+1)+".csv"
        with open(path, "w") as f:
            subgroup_data.to_csv(f, index = False)
