import pandas, collections, gc

class PokemonMovesLoader(object):
    def __init__(self, moves_loader):
        self.df = pandas.read_csv('./data/pokemon_moves.csv')
        self.df = self.df[(self.df.pokemon_id <= 151) & (self.df.version_group_id == 1)]
        self.data = collections.defaultdict(list)
        for _, r in self.df.iterrows():
            self.data[int(r['pokemon_id'])].append(int(r['move_id']))
        del self.df
        gc.collect()
        self.df = pandas.DataFrame()
        self.unavailable_moves = set([120, 153]) # TODO: Implement these moves
        self.moves_loader = moves_loader

    def getPossibleMoves(self, pokemon_id):
        return [id for id in self.data[pokemon_id] if self.moves_loader.isMoveImplemented(id) and id not in self.unavailable_moves]
