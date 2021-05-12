"""
Author(s): Maxime Cauté
Created: 17.03.2021


This file is dedicated to implementation of search trees.
"""
import numpy as np
import metrics
import copy

ROOT_ID = "root"

def get_elements_indices_by_group_in_dataframe(grouped_dataframe):
    """
    Retrieves the sets of indices for each group
    in a grouped dataframe
    """
    if grouped_dataframe is None:
        return {}
    dataframe_and_id_per_group= [
        (group_id,grouped_dataframe.get_group(group_id)) for group_id
                                             in grouped_dataframe.indices.keys()
    ]
    indices_sets_by_group = {
        group_id:set(dataframe.index)   for group_id,dataframe
                                        in dataframe_and_id_per_group
    }
    return indices_sets_by_group


class SearchTree():
    """
    Search trees for subgroups computation.
    """
    def __init__(self, groups_dataframe, subgroups_size):
        self.num_nodes = 1
        self.root = PossibleSubgroupsNode(groups_dataframe, subgroups_size, id = ROOT_ID)
        self.mothers_by_nodes = {}
        self.current_node = self.root
        self.base_dataframe = groups_dataframe


    def __str__(self):
        return (f"Root: {repr(self.root)}\n"
                f"Branches: {self.mothers_by_nodes}\n"
                f"Current node: {repr(self.current_node)}")

    def add_node(self, new_node,source_node):
        """
        Adds a node to the tree
        """
        self.mothers_by_nodes[new_node] = source_node
        self.num_nodes+=1

    #Name it decide index from current_node
    def decide_index_for_subgroup_in_tuple_from_current_node(self,
                                                            index,
                                                            subgroup_index,
                                                            tuple_index
                                                            ):
        """
        Creates a new node based on the decision of an element
        from the current node, and moves to this new node.
        """
        new_node = self.current_node.decide_index_for_subgroup_in_tuple(
                index, subgroup_index, tuple_index, self.base_dataframe,
                new_node_id = self.num_nodes
        )
        self.add_node(new_node, self.current_node)
        self.current_node = new_node

    def get_current_solution(self):
        """
        Return the solution computed at the current node.
        """
        return self.current_node.solution

    def step_forward(self, local_heuristic):
        """
        Moves down to a new node according to a local heuristic
        """
        chosen_element_index, subgroup_index, tuple_index, _ = local_heuristic(
                self.current_node
        )
        #TODO check validity
        self.decide_index_for_subgroup_in_tuple_from_current_node(
            chosen_element_index, subgroup_index, tuple_index
        )

    def backtrack(self):
        """
        Moves back to the mother node of the current one,
        and brings information up from it.
        """
        origin_node = self.current_node
        self.current_node = self.mothers_by_nodes[origin_node]

        if origin_node.has_better_distance_than(self.current_node):
            self.current_node.internal_distance = origin_node.internal_distance
            self.current_node.solution = origin_node.solution
        self.current_node.discard_decision(origin_node.indices_decision)

    def backtrack_to_root(self):
        """
        Backtracks up to the root of the tree.
        """
        while not self.current_node.is_root():
            #print("backtrack", self.current_node)
            self.backtrack()

    def search_step_and_confirm(self,   local_heuristic = lambda x: (0,0,0),
                                        global_heuristic = lambda x: True):
        """
        Does a search step according to a global heuristic,
        to know if it should further the current path.
        Returns whether the step was successful (going deeper) or not.
        """
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
        """
        Computes a tree search and return the computed solution.
        """
        stop_search = False
        for num_iterations in range(max_iterations):
            #print(num_iterations, self.current_node)
            searched_step = self.search_step_and_confirm(local_heuristic, global_heuristic)
            if not searched_step:
                break

        self.backtrack_to_root()

        return self.get_current_subgroup_dataframe()

    def get_current_subgroup_dataframe(self):
        """
        Returns the subgrouped dataframe associated with the current solution.
        """
        solution = self.get_current_solution()
        original_indices = set(self.base_dataframe.apply(lambda x: x).index)
        selected_indices = set(np.asarray(
            [list(tuple.values()) for tuple in solution]).flatten())
        dropped_indices = original_indices - selected_indices

        solution_dataframe = self.base_dataframe.apply(
            lambda x: x.drop(dropped_indices.intersection(x.index))
        )
        grouping = list(solution_dataframe.index.get_level_values(0))
        solution_dataframe.index = solution_dataframe.index.droplevel(0)
        return solution_dataframe.groupby(grouping)


class PossibleSubgroupsNode():
    """
    Nodes of the tree.
    """
    def __init__(self, groups_dataframe, subgroups_size, id =""):
        indices_sets_by_group = get_elements_indices_by_group_in_dataframe(
            groups_dataframe
        )
        self.subgroups_possible_indices_tuples = [
            copy.deepcopy(indices_sets_by_group) for i in range(subgroups_size)
        ]
        self.subgroups_chosen_indices_tuples = [
            {group_id:-1 for group_id in indices_sets_by_group}
                    for i in range(subgroups_size)
        ]
        self.groups_dataframe = groups_dataframe

        self.id = str(id)
        self.internal_distance = -1
        self.solution = None
        self.indices_decision = (-1,-1,-1)

    def list_possible_decisions(self):
        """
        Returns a list of possible decisions,
        as triples of tuple, subgroup, and element index.
        Intended for use in for loops
        """
        # TODO try to recode with enumerate_choices_left?
        possible_decisions_list = []
        for tuple, subgroup, possible_element_indices in self.list_choices_to_make():
            for element_index in possible_element_indices:
                possible_decisions_list.append((tuple, subgroup, element_index))
        return possible_decisions_list

    def list_choices_to_make(self):
        """
        Returns a list of choices left,
        as triples of tuple, subgroup, and a set of element indices to choose from.
        Intended for use in for loops.
        """
        choices_left = []
        for tuple, possible_subgroup_indices in enumerate(self.subgroups_possible_indices_tuples):
            for subgroup, possible_element_indices in possible_subgroup_indices.items():
                choices_left.append((tuple,subgroup, possible_element_indices))
        return choices_left

    def copy(self, copy_id=""):
        """
        Creates a (deep) copy of a node
        """
        copy_node = PossibleSubgroupsNode(None,1, id = copy_id)
        copy_node.subgroups_possible_indices_tuples = copy.deepcopy(self.subgroups_possible_indices_tuples)
        copy_node.subgroups_chosen_indices_tuples = copy.deepcopy(self.subgroups_chosen_indices_tuples)
        copy_node.groups_dataframe = self.groups_dataframe
        return copy_node

    def __repr__(self):
        return f"Node {self.id}"

    def __str__(self):
        return (f"[Node {self.id} <- {self.subgroups_chosen_indices_tuples} <- {self.subgroups_possible_indices_tuples}; "
                f"Solution: {self.solution}; internal_distance = {self.internal_distance}]")

    #################################

    def is_leaf(self):
        """
        Returns if this node is a leaf.
        In other words, it checks if all the indices were chosen in this node.
        """
        return np.all(
            np.asarray([list(tuple.values())
                for tuple in self.subgroups_chosen_indices_tuples])
            != -1)
    def is_end_of_branch(self):
        """
        Returns if this node is at the end of its branch.
        In other words, it checks if there is no choice left to be made.
        """
        return self.list_possible_decisions() == []
    def is_root(self):
        """
        Checks if a node is the root of the tree.
        """
        return self.id is ROOT_ID

    def has_better_distance_than(self, target_node):
        """
        Compares the distance between this node and a target one and
        returns if the this node's distance is strictly smaller.
        """
        if self.internal_distance < 0:
            return False
        if target_node.internal_distance < 0:
            return True
        return self.internal_distance < target_node.internal_distance

    def discard_possible_index(self, element_index, subgroup_id):
        """
        Removes the choice of an index in all the tuples of this node.
        """
        for tuple_index, _ in enumerate(self.subgroups_possible_indices_tuples):
            self.discard_decision((tuple_index, subgroup_id, element_index))

    #factoriser les deux?
    def discard_decision(self, decision):
        """
        Removes a possible decision from this node.
        (that is, an index choice linked to a given tuple and group)
        """
        tuple_index, group_id, element_index = decision
        self.subgroups_possible_indices_tuples[tuple_index][group_id].discard(element_index)

    def decide_index_for_subgroup_in_tuple(self,
                chosen_element_index,
                subgroup_id, tuple_index,
                groups_dataframe,
                new_node_id =""):
        """
        Creates and return a new node based on the decision of
        a given index in a given tuple and group in this node.
        """
        subgroup_id_is_index = subgroup_id not in self.subgroups_possible_indices_tuples[tuple_index]
        if subgroup_id_is_index:
            subgroup_id = list(
                self.subgroups_possible_indices_tuples[tuple_index].keys()
            )[subgroup_id]

        new_node = self.copy(copy_id=new_node_id)
        new_node.subgroups_possible_indices_tuples[tuple_index][subgroup_id] = set()
        new_node.subgroups_chosen_indices_tuples[tuple_index][subgroup_id] = chosen_element_index
        new_node.indices_decision = (tuple_index, subgroup_id, chosen_element_index)
        new_node.internal_distance = -1
        new_node.solution = None
        new_node.discard_possible_index(chosen_element_index, subgroup_id)

        if new_node.is_leaf():
            new_node.internal_distance = metrics.compute_distance_between_subgroups(
                new_node.subgroups_chosen_indices_tuples,
                groups_dataframe#base_dataframe
            )
            new_node.solution = new_node.subgroups_chosen_indices_tuples
        return new_node
