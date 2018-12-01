import random
from agent import Agent

class RandomAgent(Agent):
    def getAction(self, game):
        return random.choice(game.getLegalActions(self.name))
