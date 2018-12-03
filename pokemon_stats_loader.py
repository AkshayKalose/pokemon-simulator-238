import pandas, collections, gc

class PokemonStatsLoader(object):
    def __init__(self):
        self.df = pandas.read_csv('./data/pokemon_stats.csv')
        self.df = self.df[self.df.pokemon_id <= 151]
        self.data = collections.defaultdict(dict)
        for _, r in self.df.iterrows():
            self.data[r['pokemon_id']][r['stat_id']] = r['base_stat']
        del self.df
        gc.collect()
        self.df = pandas.DataFrame()

    def getBaseStats(self, pokemon_id):
        return self.data[pokemon_id]

    def getStats(self, pokemon_id, pokemon_level):
        #TODO: Currently disregards IV, and EV
        stats = dict(self.getBaseStats(pokemon_id))
        if pokemon_level != 100:
            raise Exception('TODO: Implement calculating stats')
        stats[1] = 110 + 2 * stats[1]
        stats[2] = 5 + 2 * stats[2]
        stats[3] = 5 + 2 * stats[3]
        stats[4] = 5 + 2 * stats[4]
        stats[5] = 5 + 2 * stats[5]
        stats[6] = 5 + 2 * stats[6]
        return stats
