import pandas, collections, gc, json

class MovesLoader(object):
    def __init__(self):
        self.df = pandas.read_csv('./data/moves.csv')
        self.df = self.df[self.df.generation_id == 1]
        self.data = collections.defaultdict(dict)
        self.not_implemented_categories = set(['swagger', 'ohko', 'whole-field-effect', 'field-effect', 'force-switch', 'unique'])
        self.not_implemented_moves = set()
        for _, r in self.df.iterrows():
            id = int(r['id'])
            with open('./pokeapi/move/' + str(id) + '/index.json') as f:
                data = json.load(f)
                meta = data['meta']
                stat_changes = data['stat_changes']
                del data
            self.data[id] = {
                'identifier': r['identifier'],
                'type_id': int(r['type_id']),
                'power': None if pandas.isnull(r['power']) else int(r['power']),
                'pp': int(r['pp']),
                'accuracy': None if pandas.isnull(r['accuracy']) else int(r['accuracy']), #TODO: what does it mean for accuracy to be null?
                'priority': int(r['priority']),
                'target_id': int(r['target_id']),
                'damage_class_id': int(r['damage_class_id']),
                'effect_id': int(r['effect_id']),
                'effect_chance': None if pandas.isnull(r['effect_chance']) else int(r['effect_chance']),
                'meta': meta,
                'stat_changes': stat_changes
            }
            if meta['category']['name'] in self.not_implemented_categories:
                self.not_implemented_moves.add(id)
        del self.df
        gc.collect()
        self.df = pandas.DataFrame()

    def getMove(self, move_id):
        return self.data[move_id]

    def isMoveImplemented(self, move_id):
        return move_id not in self.not_implemented_moves
