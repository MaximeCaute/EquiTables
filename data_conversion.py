"""
Author(s): Maxime Cauté
Created: 03.03.2021

This file regroups the functions dedicated to data conversion from input files to python data.
"""

import pandas as pd

def check_length_validity(dataline, header, line = None):
    """
    This function checks that the given dataline fits with the header.

    Raises an Exception if not.
    --
    Inputs:
        - dataline: string list. The line for the piece data.
        - header: string list. The header for the data.
            Each element is the tag for each element of a piece of data.
    Parameters:
        - line: int. If specified, represents the line of the issue in the data.
            Defaults to None (unspecified).
    """
    if len(dataline) < len(header):
        line_message =  ("Data line: "+str(line)+" "
                        +"("+str(line+1)+" with header)."
                        if line is not None
                        else "")
        wrong_format_message = "Wrong format detected! "+line_message
        print(wrong_format_message)
        raise Exception


def convert_from_csv(data_with_header, delimiter:str = ";"):
    """
    This function converts a full (line-split) csv data into a data list
    and its associated header.

    Note: There is no data conversion yet, might be implemented at some point.
    Note: Data might be interesting as a class.
    --
    Input:
        - data_with_header: string list. The data, with the header as the first line.
            Every line should have at least as many element as the header.
    Parameters:
        - delimiter: string. The delimiter for data elements.
            Defaults to ';'.
    Outputs:
        - data: string list list. The data as a list of lists.
            Each element of the list represents one piece of data, as a list.
        - header: string list. The header for the data.
            Each element is the tag for each element of a piece of data.

    """
    header = data_with_header[0].split(";")
    unsplit_data = data_with_header[1:]
    data = []
    for line, unsplit_dataline in enumerate(unsplit_data):
        split_dataline = unsplit_dataline.split(";")
        check_length_validity(split_dataline, header, line = line)
        data.append(split_dataline)
    return data, header
