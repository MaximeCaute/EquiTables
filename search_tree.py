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
    ########### Constructors and representation

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

    ########## Search functions

    def make_decision_from_current_node(self, decision):
        """
        Creates a new node based on the decision of an element
        from the current node, and moves to this new node.
        """
        new_node = self.current_node.create_new_node_from_decision(
                decision,
                self.base_dataframe,
                new_node_id = self.num_nodes
        )
        self.add_node(new_node, self.current_node)
        self.current_node = new_node

    def step_forward(self, local_heuristic):
        """
        Moves down to a new node according to a local heuristic
        """
        chosen_element_index, group_id, tuple_index, _ = local_heuristic(
                self.current_node
        )
        self.make_decision_from_current_node(
            (tuple_index, group_id, chosen_element_index)
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

    ######### Solution retrieval functions

    def get_current_solution(self):
        """
        Return the solution computed at the current node.
        """
        return self.current_node.solution

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


class PossibleSubgroupsNode():
    """
    Nodes of the tree.
    """

    ########### Constructors and representation

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

    ############# Iteration functions

    def list_possible_decisions(self):
        """
        Returns a list of possible decisions,
        as triples of tuple, subgroup, and element index.
        Intended for use in for loops
        """
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

    ############# Properties

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

    ############# Decision functions

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
        (that is, an index choice linked to a given tuple and group).
        """
        tuple_index, group_id, element_index = self.validate_decision(
            decision,
            check_element_index = False
        )
        self.subgroups_possible_indices_tuples[tuple_index][group_id].discard(
            element_index
        )

    def create_new_node_from_decision(
            self,
            decision,
            groups_dataframe,
            new_node_id =""
        ):
        """
        Creates and return a new node based on a decision
        (a tuple index, a group id and an element_index) in this node.
        """
        tuple_index, group_id, element_index = self.validate_decision(decision)

        new_node = self.copy(copy_id=new_node_id)
        new_node.subgroups_possible_indices_tuples[tuple_index][group_id] = set()
        new_node.subgroups_chosen_indices_tuples[tuple_index][group_id] = element_index
        new_node.indices_decision = (tuple_index, group_id, element_index)
        new_node.internal_distance = -1
        new_node.solution = None
        new_node.discard_possible_index(element_index, group_id)

        if new_node.is_leaf():
            new_node.internal_distance = metrics.compute_distance_between_subgroups(
                new_node.subgroups_chosen_indices_tuples,
                groups_dataframe
            )
            new_node.solution = new_node.subgroups_chosen_indices_tuples
        return new_node

    #################################### Type & Values checking ################
    #Should do with tuple, but as we have self... wait for tuple class
    def validate_group_id(self,group_id):
        """
        Ensures the group id is valid in the given node.
        If it is already a valid id, it is directly returned.
        If it is an integer (i.e. an index), it is used as such.
        All other cases raise an Error.
        """
        if isinstance(group_id, int):
            group_index = group_id
            group_ids = list(
                self.subgroups_possible_indices_tuples[0].keys()
            )

            group_indices = range(len(group_ids))
            if group_index not in group_indices:
                raise ValueError(f"Tried to interpret {group_index} as a group index, but valid indices are {groups_indices}!")

            return group_ids[group_index]

        if not isinstance(group_id, str):
            raise TypeError(f"Groups id should be of type int or str, not {type(group_id)}!")

        if group_id in self.subgroups_possible_indices_tuples[0]:
            return group_id

        raise ValueError(f"Wrong group id:{group_id}!")

    def validate_tuple_index(self, tuple_index: int):
        """
        Ensures a tuple index is valid in the given node.
        """
        valid_tuple_indices = range(len(self.subgroups_possible_indices_tuples))
        if tuple_index in valid_tuple_indices:
            return tuple_index
        raise ValueError(f"Invalid tuple index: {tuple_index}! Should be in {valid_tuple_indices}")

    def validate_decision(self, decision, check_element_index = True):
        """
        Ensures the decision is valid in the given node.
        Fixes the group id if necessary.
        """
        if len(decision) != 3:
            raise TypeError("Decision should only have three elements!")
        tuple_index, group_id, element_index = decision
        tuple_index = self.validate_tuple_index(tuple_index)
        group_id = self.validate_group_id(group_id)

        valid_element_indices = self.subgroups_possible_indices_tuples[tuple_index][group_id]
        if check_element_index and element_index not in valid_element_indices:
            raise ValueError(f"Wrong element index! Is {element_index} and should be in {valid_element_indices}!")

        return tuple_index, group_id, element_index
