# Match-and-Mix

This repository is dedicated to the reimplementation of the programs Match and Mix :
[Original link](https://www.mrc-cbu.cam.ac.uk/people/maarten-van-casteren/mixandmatch/)

## Program description

### Intent

EquiTables is a program designed to simplify subgroup selection for psychological tasks.
In these, a major difficulty is to ensure that subject or stimuli groups do not happen to be differenciable along undesired variables. EquiTables precisely aims at computing subgroups that are matched over specific variables.

EquiTables is designed to be both a stand-alone program runnable in command (or possibly with an GUI later), and a Python library.

### Main design

EquiTables explore the space of solution through a search tree that aims to make optimal single item assignements at every step -using what we called *local heuristics*-, and adequatly backtracking to search better path -using what we called *global heuristics*.

### Current state

At the time this README was updated, the program is fully working, being able to run searches with predefined local and global heuristics. It is also possible to define and use custom ones in the appropriate files.

A few improvements are planned, in making the program:
  1. more user-friendly;
  2. an intuitive, clean and documented Python library;
  3. richer, especially by adding further heuristics.

## How to run the program

The main file is `match.py` (name bound to change). Running it requires to use the following command line in your terminal, with the relevant arguments:

  python3 match.py -m MATCH -g GROUP -s SUBSET_SIZE [-h LOCAL_HEURISTIC_NAME]
              [-b GLOBAL_HEURISTIC_NAME] [-d DELIMITER] [-p SAVE_PATH]
              DATAFILE

If you want to make a simple test of the program, you may run the following command to try out our toy examples:

  python3 match.py ToySets/toy_data.csv -m Value -g Control -s 2

**!** You may want to put the result in a separate file! You will have to create it and then add its name to the arguments. If you named your folder `results`, you could thus extend the previous command as:

  python3 match.py ToySets/toy_data.csv -m Value -g Control -s 2 -p results/

Further examples are mentionned in the main file.

___

# Planned (and raw) improvements

- Heuristics as objects?(add doc element)
- Tuples as objects
- keyword arguments for heuristic selection?
- move remove_wrong_indices? (EquiTables.metrics)
- by default, normalization should cover all numeric params (EquiTables.preprocessing)
- deal with categorical group column.
- add possibility not to drop custom Equitable groups (Equitables.preprocessing)
- graceful handling of invalid functions use.
- do not go to the end of nodes with a missing chosen index and no choice left for it (EquiTables.search_tree).
- parametrize discard_possible_index (EquiTables.search_tree) so that the group index is not necessary
- rename possible_indices_tuple and chosen_indices_tuple to choice & decision tuples. (EquiTables.search_tree)
- rename decide_index_for_subgroup_in_tuple as create_new_node_from_decision and change params to a decision for explicitness? (EquiTables.search_tree)
- create debug version of search trees. (EquiTables.search_tree)
- move get_elements_indices_by_group_in_dataframe (EquiTables.search_tree)
- rename element as item
