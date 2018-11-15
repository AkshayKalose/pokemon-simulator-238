import pandas, collections, gc

class MovesLoader(object):
    def __init__(self):
        self.df = pandas.read_csv('./data/moves.csv')
        self.df = self.df[self.df.generation_id == 1]
        self.data = collections.defaultdict(dict)
        for _, r in self.df.iterrows():
            self.data[int(r['id'])] = {
                'type_id': int(r['type_id']),
                'power': None if pandas.isnull(r['power']) else int(r['power']),
                'pp': int(r['pp']),
                'accuracy': None if pandas.isnull(r['accuracy']) else int(r['accuracy']), #TODO: what does it mean for accuracy to be null?
                'priority': int(r['priority']),
                'target_id': int(r['target_id']),
                'damage_class_id': int(r['damage_class_id']),
                'effect_id': int(r['effect_id']),
                'effect_chance': None if pandas.isnull(r['effect_chance']) else int(r['effect_chance'])
            }
        del self.df
        gc.collect()
        self.df = pandas.DataFrame()

    def getMove(self, move_id):
        return dict(self.data[move_id])