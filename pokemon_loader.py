import pandas, gc, random
from pokemon_types_loader import PokemonTypesLoader
from pokemon_moves_loader import PokemonMovesLoader
from pokemon_stats_loader import PokemonStatsLoader
from moves_loader import MovesLoader

class PokemonLoader(object):
    def __init__(self, moves_loader):
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

        self.moves_loader = moves_loader
        self.pokemon_types_loader = PokemonTypesLoader()
        self.pokemon_moves_loader = PokemonMovesLoader(self.moves_loader)
        self.pokemon_stats_loader = PokemonStatsLoader()
        self.unavailable_ids = set([132])

    def getRandomPokemon(self):
        pokemon_id = None
        while True:
            pokemon_id = random.randint(1, 151)
            if pokemon_id not in self.unavailable_ids:
                break
        pokemon = dict(self.data[pokemon_id])
        pokemon['type'] = self.pokemon_types_loader.getTypes(pokemon['id'])
        pokemon['moves'] = []
        # while True:
        #     move = random.sample(self.pokemon_moves_loader.getPossibleMoves(pokemon['id']), 1)[0]
        #     if self.moves_loader.getMove(move)['power'] != None: #todo get actual move for power
        #         pokemon['moves'].append(move)
        #     if len(pokemon['moves']) == 4:
        #         break
        pokemon['moves'] = random.sample(self.pokemon_moves_loader.getPossibleMoves(pokemon['id']), min(len(self.pokemon_moves_loader.getPossibleMoves(pokemon['id'])), 4))
        pokemon['pp'] = [self.moves_loader.getMove(move_id)['pp'] for move_id in pokemon['moves']]
        pokemon['level'] = 100 #TODO: randomize?
        pokemon['stats'] = self.pokemon_stats_loader.getStats(pokemon['id'], pokemon['level'])
        pokemon['current_hp'] = pokemon['stats'][1]
        pokemon['stat_stages'] = dict([(i, 0) for i in range(1, 9)])
        pokemon['ailment'] = ['none', 0]
        return pokemon

    def getRandomTeam(self):
        #TODO: randomize size of team?
        team = []
        for _ in range(6):
            team.append(self.getRandomPokemon())
        return team
