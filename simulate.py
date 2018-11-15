from game import Game

game_obj = Game()

counter = {'player': 0, 'opponent': 0}
while counter['player'] + counter['opponent'] < 10:
    game_state = game_obj.getRandomGame()
    while game_obj.isGameOver(game_state) == False:
        game_obj.playTurn(game_state)
    counter[game_obj.isGameOver(game_state)] += 1

print counter
