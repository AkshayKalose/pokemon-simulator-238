import copy

class Agent(object):
    def __init__(self, name, team):
        self.name = name
        self.state = {
            'current_active_pokemon': 0,
            'team': team
        }

    def getState(self):
        return self.state

    def getStateCopy(self):
        return copy.deepcopy(self.state)

    def getAction(self, gameState):
        pass
