# Match-and-Mix

This repository is dedicated to the reimplementation of the programs Match and Mix :
[Original link](https://www.mrc-cbu.cam.ac.uk/people/maarten-van-casteren/mixandmatch/)

# TODO

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
