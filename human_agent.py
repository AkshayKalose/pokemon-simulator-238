from agent import Agent
from gui import GUI

class HumanAgent(Agent):
    def __init__(self, name, team, moves_loader):
        self.gui = GUI()
        self.gui.waitUntilReady()
        self.moves_loader = moves_loader
        super(HumanAgent, self).__init__(name, team)

    def getAction(self, game):
        if self.name == 'player':
            player = game.player
            opponent = game.opponent
        else:
            player = game.opponent
            opponent = game.player
        player_pokemon = player.getState()['team'][player.getState()['current_active_pokemon']]
        opponent_pokemon = opponent.getState()['team'][opponent.getState()['current_active_pokemon']]
        self.gui.setPlayer(player_pokemon['identifier'], player_pokemon['current_hp'])
        self.gui.setOpponent(opponent_pokemon['identifier'], opponent_pokemon['current_hp'])

        for i, move_id in enumerate(player_pokemon['moves']):
            move = self.moves_loader.getMove(move_id)
            self.gui.setActionText(i, move['identifier'])

        return self.gui.getAction()
