"""
Author(s): Maxime Cauté
Created: 17.03.2021


This file is dedicated to implementation of search trees.
"""
import numpy as np
import metrics
import copy

ROOT_ID = "root"

class SearchTree():
    def __init__(self, groups_indices, subgroups_size, base_dataframe):
        self.num_nodes = 1
        self.root = PossibleSubgroupsNode(groups_indices, subgroups_size, id = ROOT_ID)
        self.mothers_by_nodes = {}
        self.current_node = self.root
        self.base_dataframe = base_dataframe


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
                index, subgroup_index, tuple_index, self.base_dataframe,
                new_node_id = self.num_nodes
        )
        self.add_node(new_node, self.current_node)
        self.current_node = new_node

    def get_current_solution(self):
        return self.current_node.solution

    def step_forward(self, local_heuristic):
        chosen_element_index, subgroup_index, tuple_index = local_heuristic(
                self.current_node
        )
        #TODO check validity
        self.decide_index_for_subgroup_in_tuple_from_current_node(
            chosen_element_index, subgroup_index, tuple_index
        )

    def backtrack(self):
        origin_node = self.current_node
        self.current_node = self.mothers_by_nodes[origin_node]

        if origin_node.has_better_distance_than(self.current_node):
            self.current_node.internal_distance = origin_node.internal_distance
            self.current_node.solution = origin_node.solution
        self.current_node.remove_decision(origin_node.indices_decision)

    def backtrack_to_root(self):
        while not self.current_node.is_root():
            print("backtrack", self.current_node)
            self.backtrack()

    def search_step_and_confirm(self,   local_heuristic = lambda x: (0,0,0),
                                        global_heuristic = lambda x: True):
        is_at_root = self.current_node.is_root()
        is_at_end_of_branch = self.current_node.is_end_of_branch()

        if not is_at_end_of_branch and global_heuristic(self.current_node):
            self.step_forward(local_heuristic)
            return True
        if not is_at_root:
            self.backtrack()
            return True
        return False

    def search_and_get_solution(self,       local_heuristic = lambda x: (0,0,0),
                                            global_heuristic = lambda x: True,
                                            max_iterations = 10000):
        stop_search = False
        for num_iterations in range(max_iterations):
            print(num_iterations, self.current_node)
            searched_step = self.search_step_and_confirm(local_heuristic, global_heuristic)
            if not searched_step:
                break

        self.backtrack_to_root()
        return self.get_current_solution()


class PossibleSubgroupsNode():
    def __init__(self, indices_sets_for_groups, subgroups_size, id =""):
        self.subgroups_possible_indices_tuples = [
                copy.deepcopy(indices_sets_for_groups) for i in range(subgroups_size)
        ]
        self.subgroups_chosen_indices_tuples = [
                [-1]*len(indices_sets_for_groups) for i in range(subgroups_size)
        ]

        self.id = str(id)
        self.internal_distance = -1
        self.solution = None
        self.indices_decision = (-1,-1,-1)

    def copy(self, copy_id=""):
        copy_node = PossibleSubgroupsNode([1],1, id = copy_id)
        copy_node.subgroups_possible_indices_tuples = copy.deepcopy(self.subgroups_possible_indices_tuples)
        copy_node.subgroups_chosen_indices_tuples = copy.deepcopy(self.subgroups_chosen_indices_tuples)
        return copy_node

    def __repr__(self):
        return f"Node {self.id}"

    def __str__(self):
        return (f"[Node {self.id} <- {self.subgroups_chosen_indices_tuples} <- {self.subgroups_possible_indices_tuples}; "
                f"Solution: {self.solution}; internal_distance = {self.internal_distance}]")

    #################################

    def is_leaf(self):
        return np.all(np.asarray(self.subgroups_chosen_indices_tuples) != -1)
    def is_end_of_branch(self):
        return np.all(np.asarray(self.subgroups_possible_indices_tuples) == set())
    def is_root(self):
        return self.id == ROOT_ID

    def has_better_distance_than(self, target_node):
        if self.internal_distance < 0:
            return False
        if target_node.internal_distance < 0:
            return True
        return self.internal_distance < target_node.internal_distance

    #subgroup index is not necessary, but hopefully only fastens computation
    #beware of not having on index for two subgroups
    #DO a none case?
    def discard_possible_index(self, index, subgroup_index):
        for subgroups_possible_indices in self.subgroups_possible_indices_tuples:
            subgroups_possible_indices[subgroup_index].discard(index)

    #factoriser les deux?
    def remove_decision(self, decision):
        tuple_index, group_index, element_index = decision
        self.subgroups_possible_indices_tuples[tuple_index][group_index].discard(element_index)

    def decide_index_for_subgroup_in_tuple(self,
                chosen_element_index,
                subgroup_index, tuple_index,
                base_dataframe,
                new_node_id =""):
        new_node = self.copy(copy_id=new_node_id)
        new_node.subgroups_possible_indices_tuples[tuple_index][subgroup_index] = set()
        new_node.subgroups_chosen_indices_tuples[tuple_index][subgroup_index] = chosen_element_index
        new_node.indices_decision = (tuple_index, subgroup_index, chosen_element_index)
        new_node.internal_distance = -1
        new_node.solution = None
        new_node.discard_possible_index(chosen_element_index, subgroup_index)

        if new_node.is_leaf():
            new_node.internal_distance = metrics.compute_distance_between_subgroups(
                new_node.subgroups_chosen_indices_tuples,
                base_dataframe
            )
            new_node.solution = new_node.subgroups_chosen_indices_tuples
        return new_node

    def compute_index_in_subgroup_in_tuple_with_local_heuristic(
            self, heuristic, subgroup_index, tuple_index
    ):
        possible_indices = self.subgroups_possible_indices_tuples[tuple_index][subgroup_index]
        return heuristic(possible_indices)
