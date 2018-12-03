import pandas, collections, gc

class PokemonMovesLoader(object):
    def __init__(self):
        self.df = pandas.read_csv('./data/pokemon_moves.csv')
        self.df = self.df[(self.df.pokemon_id <= 151) & (self.df.version_group_id == 1)]
        self.data = collections.defaultdict(list)
        for _, r in self.df.iterrows():
            self.data[int(r['pokemon_id'])].append(int(r['move_id']))
        del self.df
        gc.collect()
        self.df = pandas.DataFrame()
        self.unavailable_moves = [114] # TODO: Implement these moves

    def getPossibleMoves(self, pokemon_id):
        possible_moves = list(self.data[pokemon_id])
        for unavailable_move in self.unavailable_moves:
            if unavailable_move in possible_moves:
                possible_moves.remove(unavailable_move)
        return possible_moves
