"""
Author(s): Maxime Cauté
Created: 03.03.2021

This file is the main .py file for the match program.
Github repository: https://github.com/MaximeCaute/Match-and-Mix

The input to the program should be as follow:
    - a .csv file containing all the data with the relevant information;
    - a .txt file listing out parameters to match;
    - a .txt file listing out parameters to differentiate;
"""

import argparse

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

    parser.add_argument("-d", "--delimiter", type = str,
                        default = ";",
                        help = "The delimiter for the .csv data file. "
                        + "Defaults to ';'.")
    parser.add_argument("-s", "--subset_size", type = int,
                        default = "50",
                        help = "The size of the data subset to return. "
                        + "Defaults to 50")

    args = parser.parse_args()
    return args


if __name__ == "__main__":
    """
    Upon being executed, returns a subset from (WIP)

    ---
    Call example:
        - python3 match.py ToySets/toy_data.csv -mp Value -dp Control
    """
    args = get_arguments()
    with args.datafile as datafile:
        data = datafile.readlines()
    pass
