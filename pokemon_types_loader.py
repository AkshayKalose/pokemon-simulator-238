import pandas, collections, gc

class PokemonTypesLoader(object):
    def __init__(self):
        self.df = pandas.read_csv('./data/pokemon_types.csv')
        self.df = self.df[self.df.pokemon_id <= 151]
        self.data = collections.defaultdict(list)
        for _, r in self.df.iterrows():
            self.data[r['pokemon_id']].append(r['type_id'])
        del self.df
        gc.collect()
        self.df = pandas.DataFrame()

    def getTypes(self, pokemon_id):
        return self.data[pokemon_id]
