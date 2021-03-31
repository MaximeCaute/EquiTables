"""
Author(s): Maxime Cauté
Created: 17.03.2021


This file is dedicated to implementation of search trees.
"""
class SearchTree():
    def __init__(self, groups_indices, subgroups_size):
        self.num_nodes = 1
        self.root = PossibleSubgroupsNode(groups_indices, subgroups_size, id = self.num_nodes-1)
        self.mothers_by_nodes = {}
        self.current_node = self.root


    def __str__(self):
        return (f"Root: {repr(self.root)}\n"
                f"Branches: {self.mothers_by_nodes}\n"
                f"Current node: {repr(self.current_node)}")

    def add_node(self, new_node,source_node):
        self.mothers_by_nodes[new_node] = source_node
        self.num_nodes+=1

    #Name it decide index from current_node
    def decide_index_for_subgroup_in_tuple_from_current_node(self,
                                                            index,
                                                            subgroup_index,
                                                            tuple_index
                                                            ):
        new_node = self.current_node.decide_index_for_subgroup_in_tuple(
                index, subgroup_index, tuple_index, new_node_id = self.num_nodes
        )
        self.add_node(new_node, self.current_node)
        self.current_node = new_node

    def get_current_solution(self):
        return self.current_node.subgroups_chosen_indices_tuples


class PossibleSubgroupsNode():
    def __init__(self, indices_sets_for_groups, subgroups_size, id =""):

        self.subgroups_possible_indices_tuples = [
                indices_sets_for_groups.copy() for i in range(subgroups_size)
        ]
        self.subgroups_chosen_indices_tuples = [
                [-1]*len(indices_sets_for_groups) for i in range(subgroups_size)
        ]

        self.id = str(id)


    def copy(self, copy_id=""):
        copy_node = PossibleSubgroupsNode([1],1, id = copy_id)
        copy_node.subgroups_possible_indices_tuples = self.subgroups_possible_indices_tuples.copy()
        copy_node.subgroups_chosen_indices_tuples = self.subgroups_chosen_indices_tuples.copy()
        return copy_node

    def __repr__(self):
        return f"Node{self.id}"

    def __str__(self):
        return f"[Node{self.id} <- {self.subgroups_chosen_indices_tuples} <- {self.subgroups_possible_indices_tuples}]"

    #subgroup index is not necessary, but hopefully only fastens computation
    #beware of not having on index for two subgroups
    #DO a none case?
    def discard_possible_index(self, index, subgroup_index):
        for subgroups_possible_indices in self.subgroups_possible_indices_tuples:
            subgroups_possible_indices[subgroup_index].discard(index)


    def decide_index_for_subgroup_in_tuple(self, chosen_element_index, subgroup_index, tuple_index, new_node_id =""):
        new_node = self.copy(copy_id=new_node_id)
        new_node.subgroups_possible_indices_tuples[tuple_index][subgroup_index] = set()
        new_node.subgroups_chosen_indices_tuples[tuple_index][subgroup_index] = chosen_element_index
        new_node.discard_possible_index(chosen_element_index, subgroup_index)
        return new_node

    def compute_index_in_subgroup_in_tuple_with_local_heuristic(
            self, heuristic, subgroup_index, tuple_index
    ):
        possible_indices = self.subgroups_possible_indices_tuples[tuple_index][subgroup_index]
        return heuristic(possible_indices)
