"""
In search.py, you will implement generic search algorithms
"""

import util


class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def get_start_state(self):
        """
        Returns the start state for the search problem
        """
        util.raiseNotDefined()

    def is_goal_state(self, state):
        """
        state: Search state

        Returns True if and only if the state is a valid goal state
        """
        util.raiseNotDefined()

    def get_successors(self, state):
        """
        state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        util.raiseNotDefined()

    def get_cost_of_actions(self, actions):
        """
        actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        util.raiseNotDefined()


def general_search_algorithm(problem, data_structure):
    frontier = data_structure()
    start_state = problem.get_start_state()
    frontier.push(start_state)
    came_from = dict()
    came_from[start_state] = None, None

    while not frontier.isEmpty():
        current_state = frontier.pop()

        if problem.is_goal_state(current_state):
            return get_path_to_start_state(current_state, came_from, start_state)

        for successor_state, successor_move, _ in problem.get_successors(current_state):
            if successor_state not in came_from:
                frontier.push(successor_state)
                came_from[successor_state] = current_state, successor_move


def get_path_to_start_state(state, came_from, start_state):
    moves = []
    while state != start_state:
        moves.append(came_from[state][1])
        state = came_from[state][0]
    return list(reversed(moves))


def depth_first_search(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches
    the goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:
    """
    return general_search_algorithm(problem, util.Stack)


def breadth_first_search(problem):
    """
    Search the shallowest nodes in the search tree first.
    """
    return general_search_algorithm(problem, util.Queue)


def general_priority_search(problem, heuristic=lambda state, problem: 0):
    frontier = util.PriorityQueue()
    start_state = problem.get_start_state()
    frontier.push(start_state, 0)
    came_from, cost_so_far, explored = {}, {}, set()
    came_from[start_state] = None, None
    cost_so_far[start_state] = 0

    while not frontier.isEmpty():
        current_state = frontier.pop()

        if current_state not in explored:
            explored.add(current_state)

            if problem.is_goal_state(current_state):
                print(current_state)
                return get_path_to_start_state(current_state, came_from, start_state)

            for successor in problem.get_successors(current_state):
                successor_state, successor_move, successor_cost = successor
                new_cost = cost_so_far[current_state] + successor_cost
                if successor_state not in cost_so_far or new_cost < cost_so_far[start_state]:
                    cost_so_far[successor_state] = new_cost
                    priority = new_cost + heuristic(successor_state, problem)
                    frontier.push(successor_state, priority)
                    came_from[successor_state] = current_state, successor_move


def uniform_cost_search(problem):
    """
    Search the node of least total cost first.
    """
    "*** YOUR CODE HERE ***"
    return general_priority_search(problem)


def null_heuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def a_star_search(problem, heuristic=null_heuristic):
    """
    Search the node that has the lowest combined cost and heuristic first.
    """
    "*** YOUR CODE HERE ***"
    return general_priority_search(problem, heuristic)


# Abbreviations
bfs = breadth_first_search
dfs = depth_first_search
astar = a_star_search
ucs = uniform_cost_search
