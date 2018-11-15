import pandas, collections, gc

class TypeEfficacyLoader(object):
    def __init__(self):
        self.df = pandas.read_csv('./data/type_efficacy.csv')
        self.data = collections.defaultdict(dict)
        for _, r in self.df.iterrows():
            self.data[r['damage_type_id']][r['target_type_id']] = float(r['damage_factor']) / 100
        del self.df
        gc.collect()
        self.df = pandas.DataFrame()

    def getTypeEfficacy(self, damage_type_id, target_type_id):
        return self.data[damage_type_id][target_type_id]
