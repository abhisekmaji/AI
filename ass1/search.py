# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """
    REVERSE_PUSH = False

    @staticmethod
    def reverse_push():
        SearchProblem.REVERSE_PUSH = not SearchProblem.REVERSE_PUSH

    @staticmethod
    def print_push():
        print(SearchProblem.REVERSE_PUSH)

    @staticmethod
    def get_push():
        return SearchProblem.REVERSE_PUSH

    def get_expanded(self):
        return self.__expanded

    def inc_expanded(self):
        self.__expanded+=1

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    
    InitialState = problem.getStartState()
    if problem.isGoalState(InitialState):
        return []
    Frontier = util.Stack()
    # FrontierList = []
    Explored = []
    # (actions,nodes) in Frontier    
    Frontier.push(([] , InitialState))
    """
    FrontierList.append(InitialState)
    while not Frontier.isEmpty():
        actions, curState = Frontier.pop()
        FrontierList.remove(curState)
        Explored.append(curState)
        for childState, action, cost in problem.getSuccessors(curState):
            newAction = actions + [action]
            if (childState not in Explored) or (childState not in FrontierList):
                if problem.isGoalState(childState):
                    return newAction
                Frontier.push((newAction,childState))
                FrontierList.append(childState)
    """
    while not Frontier.isEmpty():
        actions , currentState = Frontier.pop()
        # checking if the current state is in the explored set or not
        if currentState not in Explored:
            Explored.append(currentState)
            # check if goal state or not 
            if problem.isGoalState(currentState):
                return actions
            # push the child nodes in the frontier.
            for childState, action, cost in problem.getSuccessors(currentState):
                if childState not in Explored:
                    newAction = actions + [action]
                    Frontier.push((newAction, childState))
    
    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"

    InitialState = problem.getStartState()
    if problem.isGoalState(InitialState):
        return []
    
    Frontier = util.Queue()
    # (actions,nodes) in Frontier    
    Frontier.push(([] , InitialState))
    Explored = []    
    #FrontierList = []
    #FrontierList.append(InitialState)
    """while not Frontier.isEmpty():
        actions, curState = Frontier.pop()
        FrontierList.remove(curState)
        if problem.isGoalState(curState):
            return actions
        Explored.append(curState)
        for childState, action, cost in problem.getSuccessors(curState):
            newAction = actions + [action]
            if childState not in (FrontierList or Explored):
                #if problem.isGoalState(childState):
                #    return newAction
                
                Frontier.push((newAction,childState))
                FrontierList.append(childState)
    """
    while not Frontier.isEmpty():
        actions , currentState = Frontier.pop()
        #checking if the current state is in the explored set or not 
        if currentState not in Explored:
            Explored.append(currentState)
            # check if goal state or not 
            if problem.isGoalState(currentState):
                return actions
            # push the child nodes in the frontier.
            for childState, action, cost in problem.getSuccessors(currentState):
                if childState not in Explored:
                    newAction = actions + [action]
                    Frontier.push((newAction, childState))
    
    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"

    InitialState = problem.getStartState()
    if problem.isGoalState(InitialState):
        return []

    Frontier = util.PriorityQueue()
    #(( action to current node , coordinate/node , cost to current node),priority)
    Frontier.push(([], InitialState, 0), 0)
    Explored = []
    while not Frontier.isEmpty():
        actions, currentState, prevCost = Frontier.pop()
        # checking the current state is not in the frontier.
        if currentState not in Explored:
            Explored.append(currentState)
            # check if goal state or not 
            if problem.isGoalState(currentState):
                return actions
            # push the child nodes in the frontier.
            for childState, action, cost in problem.getSuccessors(currentState):
                if childState not in Explored:    
                    newCostTochildState = prevCost + cost
                    newAction = actions + [action]
                    Frontier.push((newAction, childState, newCostTochildState),newCostTochildState)
    
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"

    InitialState = problem.getStartState()
    if problem.isGoalState(InitialState):
        return []

    Frontier = util.PriorityQueue()
    #(( action to current node , coordinate/node , cost to current node),priority)
    Frontier.push(([], InitialState, 0), 0)
    Explored = []
    while not Frontier.isEmpty():
        actions, currentState, prevCost = Frontier.pop()
        # checking if the current state is in expored state
        if currentState not in Explored:
            Explored.append(currentState)
            # check if goal state or not 
            if problem.isGoalState(currentState):
                return actions
            # push the child nodes in the frontier.
            for childState, action, cost in problem.getSuccessors(currentState):                
                if childState not in Explored:    
                    newCostTochildState = prevCost + cost
                    heuristicCost = newCostTochildState + heuristic(childState,problem)
                    newAction = actions + [action]
                    Frontier.push((newAction, childState, newCostTochildState),heuristicCost)

                
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
reverse_push=SearchProblem.reverse_push
print_push=SearchProblem.print_push