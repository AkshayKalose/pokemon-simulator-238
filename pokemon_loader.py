import pandas, gc, random
from pokemon_types_loader import PokemonTypesLoader
from pokemon_moves_loader import PokemonMovesLoader
from pokemon_stats_loader import PokemonStatsLoader
from moves_loader import MovesLoader

class PokemonLoader(object):
    def __init__(self):
        self.df = pandas.read_csv('./data/pokemon.csv')
        self.df = self.df[self.df.id <= 151]
        self.data = {}
        for _, r in self.df.iterrows():
            self.data[int(r['id'])] = {
                'id': int(r['id']),
                'identifier': r['identifier']
            }
        del self.df
        gc.collect()
        self.df = pandas.DataFrame()

        self.pokemon_types_loader = PokemonTypesLoader()
        self.pokemon_moves_loader = PokemonMovesLoader()
        self.pokemon_stats_loader = PokemonStatsLoader()
        self.moves_loader = MovesLoader()

    def getRandomPokemon(self):
        pokemon = dict(self.data[random.randint(1, 151)])
        pokemon['type'] = self.pokemon_types_loader.getTypes(pokemon['id'])
        pokemon['moves'] = []
        # while True:
        #     move = random.sample(self.pokemon_moves_loader.getPossibleMoves(pokemon['id']), 1)[0]
        #     if self.moves_loader.getMove(move)['power'] != None: #todo get actual move for power
        #         pokemon['moves'].append(move)
        #     if len(pokemon['moves']) == 4:
        #         break
        pokemon['moves'] = random.sample(self.pokemon_moves_loader.getPossibleMoves(pokemon['id']), min(len(self.pokemon_moves_loader.getPossibleMoves(pokemon['id'])), 4))

        pokemon['level'] = 100 #TODO: randomize?
        pokemon['stats'] = self.pokemon_stats_loader.getStats(pokemon['id'], pokemon['level'])
        return pokemon

    def getRandomTeam(self):
        #TODO: randomize size of team?
        team = []
        for _ in range(6):
            team.append(self.getRandomPokemon())
        return team
