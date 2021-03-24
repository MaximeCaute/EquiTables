"""
Author(s): Maxime Cauté
Created: 17.03.2021

This file is dedicated to the seperation of data into appropriate groups
"""
def compute_subgroups_indices( data_to_match, data_to_differentiate,
                            groups_size = 2):
    """
    This function computes indices for groups based on data.

    WIP
    ATM only computes indices over the last differentiation parameter
    --
    Input:
        - data_to_match: pandas DataFrame.
            The part of data that should be matched.
        - data_to_differentiate: pandas DataFrame.
            The part of data that should be differentiated.
    Parameters:
        - groups_size: int. The sizes of the group to create.
            Defaults to groups of size 2 (TO BE CHANGED)
    Outputs:
        - subgroups_indices : int list list. The indices of the elements in each groups.
            The i-th element contains the indices of the elements in group i.
    """
    ## NOTE : FONCTION RENVOYER PDSERIES avec var indicatrices
    # Ignorer les lignes non dans sous-groupes
    #print(data_to_match)

    for differentiation_parameter in data_to_differentiate:
        parameter_dataframe = data_to_differentiate[differentiation_parameter]

        groups_indices = []
        for truth_value in [True,False]:
            differentiated_data_index = data_to_differentiate.index[
                                        parameter_dataframe == truth_value]

            groups_indices.append(differentiated_data_index.to_list())


    subgroups_indices = [group_indices[:groups_size] for group_indices
                                                    in groups_indices]

    return subgroups_indices
