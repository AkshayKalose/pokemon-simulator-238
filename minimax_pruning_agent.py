from minimax_agent import MinimaxAgent
import random

class MinimaxPruningAgent(MinimaxAgent):
    def __init__(self, name, team, depth):
        self.depth = depth
        super(MinimaxPruningAgent, self).__init__(name, team, depth)

    def getAction(self, game):
        def recurse(state, agent, depth, alpha, beta):
            if state.isGameOver() or depth == 0:
                return self.evaluationFunction(state)
            if agent == 'player':
                value = (float('-inf'), 0)
                for action in state.getLegalActions(agent):
                    value = max(value, (recurse(
                        state.generateSuccessor(agent, action),
                        'opponent' if agent == 'player' else 'player',
                        depth - 1 if agent == 'opponent' else depth, # TODO: Assumes Minimax Agent is Always Player
                        alpha,
                        beta
                    ), action))
                    alpha = max(alpha, value[0])
                    if alpha >= beta:
                        break
                if depth == self.depth:
                    return value
                else:
                    return value[0]
            else:
                value = (float('inf'), 0)
                for action in state.getLegalActions(agent):
                    value = min(value, (recurse(
                        state.generateSuccessor(agent, action),
                        'opponent' if agent == 'player' else 'player',
                        depth - 1 if agent == 'opponent' else depth, # TODO: Assumes Minimax Agent is Always Player
                        alpha,
                        beta
                    ), action))
                    beta = min(beta, value[0])
                    if alpha >= beta:
                        break
                return value[0]

        _, action = recurse(game, 'player', self.depth, float('-inf'), float('inf'))
        return action
