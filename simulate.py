from pokemon_loader import PokemonLoader
from moves_loader import MovesLoader
from type_efficacy_loader import TypeEfficacyLoader

from random_agent import RandomAgent
from minimax_agent import MinimaxAgent
from minimax_pruning_agent import MinimaxPruningAgent
from baseline_agent import BaselineAgent
from human_agent import HumanAgent

from game import Game

moves_loader = MovesLoader()
pokemon_loader = PokemonLoader(moves_loader)
type_efficacy_loader = TypeEfficacyLoader()

counter = {'player': 0, 'opponent': 0, 'timeout': 0}
while counter['player'] + counter['opponent'] < 100:
    print counter
    # player = MinimaxAgent('player', pokemon_loader.getRandomTeam(), 1)
    # player = MinimaxPruningAgent('player', pokemon_loader.getRandomTeam(), 1)
    player = BaselineAgent('player', pokemon_loader.getRandomTeam())
    # player = HumanAgent('player', pokemon_loader.getRandomTeam(), moves_loader)
    # player = RandomAgent('player', pokemon_loader.getRandomTeam())
    # opponent = BaselineAgent('opponent', pokemon_loader.getRandomTeam())
    # opponent = RandomAgent('opponent', pokemon_loader.getRandomTeam())
    opponent = HumanAgent('opponent', pokemon_loader.getRandomTeam(), moves_loader)
    game_obj = Game(pokemon_loader, moves_loader, type_efficacy_loader, player, opponent)
    counter[game_obj.run()] += 1

print counter
