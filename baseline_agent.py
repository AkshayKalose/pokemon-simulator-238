from agent import Agent

class BaselineAgent(Agent):
    def getAction(self, game):
        if self.name == 'player':
            from_pokemon = game.player.getState()['team'][game.player.getState()['current_active_pokemon']]
            to_pokemon = game.opponent.getState()['team'][game.opponent.getState()['current_active_pokemon']]
        else:
            from_pokemon = game.opponent.getState()['team'][game.opponent.getState()['current_active_pokemon']]
            to_pokemon = game.player.getState()['team'][game.player.getState()['current_active_pokemon']]

        legal_actions = game.getLegalActions(self.name)
        if len(legal_actions) == 1:
            return legal_actions[0]

        from_move_id = None
        best_damage = -1
        for legal_action in legal_actions:
            move_id = from_pokemon['moves'][legal_action]
            move = game.moves_loader.getMove(move_id)
            power = 0 if move['power'] == None else move['power']
            # damage_to_inflict = (( (2 * from_pokemon['level'] / 5 + 2) * power * from_pokemon['stats'][move['damage_class_id']] / to_pokemon['stats'][move['damage_class_id'] + 1]) / 50 + 2)
            modifier = 1
            for t in to_pokemon['type']:
                modifier *= game.type_efficacy_loader.getTypeEfficacy(move['type_id'], t)
            # damage_to_inflict *= modifier
            # print damage_to_inflict
            # print best_damage
            if power * modifier > best_damage:
                from_move_id = move_id
                best_damage = power * modifier
        # print best_damage
        return from_pokemon['moves'].index(from_move_id)
