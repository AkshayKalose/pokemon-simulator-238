from pokemon_loader import PokemonLoader
from moves_loader import MovesLoader
from type_efficacy_loader import TypeEfficacyLoader
import random

class Game(object):
    def __init__(self):
        self.pokemon_loader = PokemonLoader()
        self.moves_loader = MovesLoader()
        self.type_efficacy_loader = TypeEfficacyLoader()

    def getRandomGame(self):
        game = {
            'player': {
                'team': self.pokemon_loader.getRandomTeam()
            },
            'opponent': {
                'team': self.pokemon_loader.getRandomTeam()
            }
        }
        return game

    def isGameOver(self, game):
        total_hp = 0
        for pokemon in game['player']['team']:
            total_hp += pokemon['stats'][1]
        if total_hp == 0:
            return 'opponent'
        total_hp = 0
        for pokemon in game['opponent']['team']:
            total_hp += pokemon['stats'][1]
        if total_hp == 0:
            return 'player'
        return False

    def performMove(self, game, from_pokemon, to_pokemon, player_strategy):
        # Pick a random move
        # TODO: update player strategy
        if player_strategy:
            from_move_id = from_pokemon['moves'][0]
            best_damage = 0
            for move_id in from_pokemon['moves']:
                move = self.moves_loader.getMove(move_id)
                power = 0 if move['power'] == None else move['power']
                # damage_to_inflict = (( (2 * from_pokemon['level'] / 5 + 2) * power * from_pokemon['stats'][move['damage_class_id']] / to_pokemon['stats'][move['damage_class_id'] + 1]) / 50 + 2)
                modifier = 1
                for t in to_pokemon['type']:
                    modifier *= self.type_efficacy_loader.getTypeEfficacy(move['type_id'], t)
                # damage_to_inflict *= modifier
                # print damage_to_inflict
                if power * modifier > best_damage:
                    from_move_id = move_id
                    best_damage = power * modifier
        else:
            from_move_id = from_pokemon['moves'][random.randint(0, len(from_pokemon['moves']) - 1)]
        from_move = self.moves_loader.getMove(from_move_id)
        move_damage_class = from_move['damage_class_id']
        power = 0 if from_move['power'] == None else from_move['power']
        damage_to_inflict = (( (2 * from_pokemon['level'] / 5 + 2) * power * from_pokemon['stats'][move_damage_class] / to_pokemon['stats'][move_damage_class + 1]) / 50 + 2)
        modifier = 1
        for t in to_pokemon['type']:
            modifier *= self.type_efficacy_loader.getTypeEfficacy(from_move['type_id'], t)
        damage_to_inflict *= modifier
        to_pokemon['stats'][1] = max(to_pokemon['stats'][1] - damage_to_inflict, 0)

    def playTurn(self, game):
        # Get active Pokemon
        player_pokemon = None
        for p in game['player']['team']:
            if p['stats'][1] > 0:
                player_pokemon = p
                break
        opponent_pokemon = None
        for p in game['opponent']['team']:
            if p['stats'][1] > 0:
                opponent_pokemon = p
                break

        #TODO: some moves have special order(not reliant on speed?), if same random
        if player_pokemon['stats'][6] > opponent_pokemon['stats'][6]:
            self.performMove(game, player_pokemon, opponent_pokemon, True)
            self.performMove(game, opponent_pokemon, player_pokemon, False)
        elif player_pokemon['stats'][6] < opponent_pokemon['stats'][6]:
            self.performMove(game, opponent_pokemon, player_pokemon, False)
            self.performMove(game, player_pokemon, opponent_pokemon, True)
        else:
            if random.randint(0, 1) == 1:
                self.performMove(game, player_pokemon, opponent_pokemon, True)
                self.performMove(game, opponent_pokemon, player_pokemon, False)
            else:
                self.performMove(game, opponent_pokemon, player_pokemon, False)
                self.performMove(game, player_pokemon, opponent_pokemon, True)
