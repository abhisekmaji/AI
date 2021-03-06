# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"        
        
        ghostSum = 0
        for ghost in newGhostStates:
            posGhost = ghost.getPosition() 
            dist = util.manhattanDistance(newPos,posGhost)
            if dist>=2:
                ghostSum = ghostSum -1.0/dist
            else:
                return -99999999
                   
        foodList = newFood.asList()
        foodSum = 0
        for food in foodList:
            dist = util.manhattanDistance(newPos,food)
            if dist!=0:
                foodSum = foodSum + 1.0/dist        
        

        finalScore = successorGameState.getScore() + ghostSum + foodSum
        return finalScore

def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        
        
        action = self.maxValue(gameState,0,0)[1]
        util.raiseNotDefined()
        return action

        
    
    def maxValue(self, gameState, depth, agentIndex):
        
        v= [-9999999999,Directions.STOP]
        agentIndex = 0
        actionList = gameState.getLegalActions(agentIndex)
        
        if gameState.isWin() or depth>=self.depth or not actionList:
            v[0] = self.evaluationFunction(gameState)
            return v

        for action in actionList:
            successor = gameState.generateSuccessor(agentIndex, action)
            value = self.minValue(successor,depth,agentIndex+1)[0]
            if value>v[0]:
                v= (value,action)
        return v

    def minValue(self, gameState, depth, agentIndex):
        
        v=[9999999999,Directions.STOP]
        actionList = gameState.getLegalActions(agentIndex)

        if gameState.isLose() or depth>=self.depth or not actionList:
            v[0] = self.evaluationFunction(gameState)
            return v

        for action in actionList:
            successor = gameState.generateSuccessor(agentIndex, action)
            value = 0
            if agentIndex == (gameState.getNumAgents() - 1):
                value = self.maxValue(successor,depth+1,0)[0]
            else:
                value = self.minValue(successor,depth,agentIndex+1)[0]       
            if value< v[0]:
                v = [value,action]
        return v

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"

        alpha = -99999999999
        beta = 99999999999
        action = self.maxValue(gameState,0,0,alpha,beta)[1]
        util.raiseNotDefined()
        return action
        

    def maxValue(self, gameState, depth, agentIndex, alpha, beta):
        
        v= [-9999999999,Directions.STOP]
        agentIndex = 0
        actionList = gameState.getLegalActions(agentIndex)
        
        if gameState.isWin() or depth>=self.depth or not actionList:
            v[0] = self.evaluationFunction(gameState)
            return v

        for action in actionList:
            successor = gameState.generateSuccessor(agentIndex, action)
            value = self.minValue(successor,depth,agentIndex+1,alpha,beta)[0]
            if value>v[0]:
                v= (value,action)

            alpha = max(alpha , v[0])
            if v[0]>beta:
                return v
        return v

    def minValue(self, gameState, depth, agentIndex, alpha, beta):
        
        v=[9999999999,Directions.STOP]
        actionList = gameState.getLegalActions(agentIndex)
        
        if gameState.isLose() or depth>=self.depth or not actionList:
            v[0] = self.evaluationFunction(gameState)
            return v

        for action in actionList:
            successor = gameState.generateSuccessor(agentIndex, action)
            value = 0
            if agentIndex == (gameState.getNumAgents() - 1):
                value = self.maxValue(successor,depth+1,0,alpha,beta)[0]
            else:
                value = self.minValue(successor,depth,agentIndex+1,alpha,beta)[0]       
            if value<v[0]:
                v = [value,action]

            beta = min(beta,v[0])
            if v[0]<alpha:
                return v
        return v

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"

        action = self.maxValue(gameState,0,0)[1]
        util.raiseNotDefined()
        return action

            
    def maxValue(self, gameState, depth, agentIndex):
        
        v= [-9999999999,Directions.STOP]
        agentIndex = 0
        actionList = gameState.getLegalActions(agentIndex)
        
        if gameState.isWin() or depth>=self.depth or not actionList:
            v[0] = self.evaluationFunction(gameState)
            return v

        for action in actionList:
            successor = gameState.generateSuccessor(agentIndex, action)
            value = self.expectedValue(successor,depth,agentIndex+1)[0]
            if value>v[0]:
                v= (value,action)
        return v

    def expectedValue(self, gameState, depth, agentIndex):
        
        v=[0,None]
        actionList = gameState.getLegalActions(agentIndex)
        

        if gameState.isLose() or depth>=self.depth or not actionList:
            v[0] = self.evaluationFunction(gameState)
            return v
        
        probability = 1.0/len(actionList)
        for action in actionList:
            successor = gameState.generateSuccessor(agentIndex, action)
            value = 0
            if agentIndex == (gameState.getNumAgents() - 1):
                value = self.maxValue(successor,depth+1,0)[0]
            else:
                value = self.expectedValue(successor,depth,agentIndex+1)[0]       
            
            v[0] = v[0] + probability*value
        return v

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"

    curPos = currentGameState.getPacmanPosition()
    curFood = currentGameState.getFood()
    curGhostStates = currentGameState.getGhostStates()
    
    additionalScore = 0
    if currentGameState.isWin():
        additionalScore += 1000000
    if currentGameState.isLose():
        additionalScore -= 1000000 
    
    minFood = 999999999
    foodList = curFood.asList()
    for food in foodList:
        foodDist = util.manhattanDistance(curPos,food)
        if minFood>foodDist:
            minFood = foodDist
    
    minActiveGhost = 999999999
    minScaredGhost = 999999999
    countScared = 0
    for ghost in curGhostStates:
        posGhost = ghost.getPosition() 
        dist = util.manhattanDistance(curPos,posGhost)
        if not ghost.scaredTimer:          
            minActiveGhost = min(dist,minActiveGhost)
            if minActiveGhost<2:
                minFood = 9999999    
        else:
            countScared +=1
            minScaredGhost = min(dist,minScaredGhost)
    
    if countScared==0:
        minScaredGhost = 0

    foodLeft = len(foodList)
    capsulesLeft = len(currentGameState.getCapsules())

    finalScore = 10*currentGameState.getScore() +1.0/(minFood) -2*capsulesLeft -10*foodLeft +1.5*additionalScore
    util.raiseNotDefined()
    return finalScore
    

# Abbreviation
better = betterEvaluationFunction
