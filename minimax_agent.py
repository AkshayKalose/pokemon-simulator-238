from agent import Agent
import random

class MinimaxAgent(Agent):
    def __init__(self, name, team, depth):
        self.depth = depth
        super(MinimaxAgent, self).__init__(name, team)

    def getAction(self, game):
        def recurse(state, agent, depth):
            if state.isGameOver() or depth == 0:
                return self.evaluationFunction(state)
            candidates = [
                (recurse(
                    state.generateSuccessor(agent, action),
                    'opponent' if agent == 'player' else 'player',
                    depth - 1 if agent == 'opponent' else depth # TODO: Assumes Minimax Agent is Always Player
                ), action)
                for action in state.getLegalActions(agent)
            ]
            if agent == 'player':
                maximum = max(candidates)
                # print maximum
                if depth == self.depth:
                    # print candidates
                    return maximum
                else:
                    return maximum[0]
            else:
                return min(candidates)[0]
        _, action = recurse(game, 'player', self.depth)
        # print _, action
        return action

    def evaluationFunction(self, game):
        # TODO: Include status effects
        # TODO: make this into a float instead of int?
        result = float(game.agentCurrentHP(game.player)) / game.agentTotalHP(game.player) - 3 * float(game.agentCurrentHP(game.opponent)) / game.agentTotalHP(game.opponent)
        if not game.isGameOver():
            opponent_ailment = game.agentCurrentPokemon(game.opponent)['ailment']
            if opponent_ailment[0] in ['sleep', 'paralysis'] and opponent_ailment[1] == 2:
                result /= 1.1
        return result
