import random, copy

class Game(object):
    def __init__(self, pokemon_loader, moves_loader, type_efficacy_loader, player, opponent):
        self.pokemon_loader = pokemon_loader
        self.moves_loader = moves_loader
        self.type_efficacy_loader = type_efficacy_loader
        self.player = player
        self.opponent = opponent

    def agentCurrentHP(self, agent):
        return sum([pokemon['current_hp'] for pokemon in agent.getState()['team']])

    def agentTotalHP(self, agent):
        return sum([pokemon['stats'][1] for pokemon in agent.getState()['team']])

    def agentCurrentPokemon(self, agent):
        index = agent.getState()['current_active_pokemon']
        return agent.getState()['team'][index] if index < 7 else None

    def isGameOver(self):
        if self.agentCurrentHP(self.player) == 0:
            return 'opponent'
        if self.agentCurrentHP(self.opponent) == 0:
            return 'player'
        return False

    def getStageMultiplier(self, stage):
        multiplier = None
        if stage == -6:
            multiplier = 25
        elif stage == -5:
            multiplier = 28
        elif stage == -4:
            multiplier = 33
        elif stage == -3:
            multiplier = 40
        elif stage == -2:
            multiplier = 50
        elif stage == -1:
            multiplier = 66
        elif stage == 0:
            multiplier = 100
        elif stage == 1:
            multiplier = 150
        elif stage == 2:
            multiplier = 200
        elif stage == 3:
            multiplier = 250
        elif stage == 4:
            multiplier = 300
        elif stage == 5:
            multiplier = 350
        elif stage == 6:
            multiplier = 400
        return float(multiplier) / 100

    def getStat(self, pokemon, stat_index):
        return float(pokemon['stats'][stat_index]) * self.getStageMultiplier(pokemon['stat_stages'][stat_index])

    def getState(self):
        return {
            'player': self.player.getState(),
            'opponent': self.opponent.getState()
        }

    def generateSuccessor(self, name, action):
        successor = Game(self.pokemon_loader, self.moves_loader, self.type_efficacy_loader, copy.deepcopy(self.player), copy.deepcopy(self.opponent))
        player_pokemon = successor.player.getState()['team'][successor.player.getState()['current_active_pokemon']]
        opponent_pokemon = successor.opponent.getState()['team'][successor.opponent.getState()['current_active_pokemon']]
        if name == 'player':
            move = successor.moves_loader.getMove(player_pokemon['moves'][action])
            successor.performMove(successor.getState(), player_pokemon, opponent_pokemon, move, action)
            if opponent_pokemon['current_hp'] == 0:
                successor.opponent.getState()['current_active_pokemon'] += 1
        else:
            move = successor.moves_loader.getMove(opponent_pokemon['moves'][action])
            successor.performMove(successor.getState(), opponent_pokemon, player_pokemon, move, action)
            if player_pokemon['current_hp'] == 0:
                successor.player.getState()['current_active_pokemon'] += 1

        # Ailment
        if name =='player':
            if player_pokemon['current_hp'] > 0 and player_pokemon['ailment'][0] != 'none':
                self.performAilment(player_pokemon)
                if player_pokemon['current_hp'] == 0:
                    successor.player.getState()['current_active_pokemon'] += 1
        else:
            if opponent_pokemon['current_hp'] > 0 and opponent_pokemon['ailment'][0] != 'none':
                self.performAilment(opponent_pokemon)
                if opponent_pokemon['current_hp'] == 0:
                    successor.opponent.getState()['current_active_pokemon'] += 1
        return successor

    def performTurn(self):
        # Get active Pokemon
        player_pokemon = self.agentCurrentPokemon(self.player)
        opponent_pokemon = self.agentCurrentPokemon(self.opponent)

        # -1 = Struggle, 0 - 3 = Perform a Move, 4 = Switch
        player_action = self.player.getAction(self)
        opponent_action = self.opponent.getAction(self)

        # TODO: Implement Switch (If so, be sure the update the pokemon before performing move)

        # Account for Struggle (When pokemon is out of PP):
        if player_action == -1:
            player_move = self.moves_loader.getMove(165)
        else:
            player_move = self.moves_loader.getMove(player_pokemon['moves'][player_action])

        if opponent_action == -1:
            opponent_move = self.moves_loader.getMove(165)
        else:
            opponent_move = self.moves_loader.getMove(opponent_pokemon['moves'][opponent_action])

        # ### DEBUG OUTPUT
        # player_moves = []
        # for i, m_id in enumerate(player_pokemon['moves']):
        #     move = self.moves_loader.getMove(m_id)
        #     player_moves.append('{}|{}'.format(move['identifier'], player_pokemon['pp'][i]))
        # opponent_moves = []
        # for i, m_id in enumerate(opponent_pokemon['moves']):
        #     move = self.moves_loader.getMove(m_id)
        #     opponent_moves.append('{}|{}'.format(move['identifier'], opponent_pokemon['pp'][i]))
        # print '{}({})({})({}) -> {} | {} <- {}({})({})({})'.format(player_pokemon['identifier'], player_pokemon['ailment'][0], int(player_pokemon['current_hp']), ', '.join(player_moves), player_move['identifier'], opponent_move['identifier'], opponent_pokemon['identifier'], opponent_pokemon['ailment'][0], int(opponent_pokemon['current_hp']), ', '.join(opponent_moves))
        # ### END DEBUG OUTPUT

        if player_move['priority'] > opponent_move['priority']:
            player_first = True
        elif player_move['priority'] < opponent_move['priority']:
            player_first = False
        else:
            if self.getStat(player_pokemon, 6) > self.getStat(opponent_pokemon, 6):
                player_first = True
            elif self.getStat(player_pokemon, 6) < self.getStat(opponent_pokemon, 6):
                player_first = False
            else:
                player_first = random.randint(0, 1)

        if player_first:
            self.performMove(self.getState(), player_pokemon, opponent_pokemon, player_move, player_action)
            if opponent_pokemon['current_hp'] > 0:
                self.performMove(self.getState(), opponent_pokemon, player_pokemon, opponent_move, opponent_action)
                if player_pokemon['current_hp'] == 0:
                    self.player.getState()['current_active_pokemon'] += 1
            else:
                self.opponent.getState()['current_active_pokemon'] += 1
        else:
            self.performMove(self.getState(), opponent_pokemon, player_pokemon, opponent_move, opponent_action)
            if player_pokemon['current_hp'] > 0:
                self.performMove(self.getState(), player_pokemon, opponent_pokemon, player_move, player_action)
                if opponent_pokemon['current_hp'] == 0:
                    self.opponent.getState()['current_active_pokemon'] += 1
            else:
                self.player.getState()['current_active_pokemon'] += 1

        # Ailment
        if player_pokemon['current_hp'] > 0 and player_pokemon['ailment'][0] != 'none':
            self.performAilment(player_pokemon)
            if player_pokemon['current_hp'] == 0:
                self.player.getState()['current_active_pokemon'] += 1
        if opponent_pokemon['current_hp'] > 0 and opponent_pokemon['ailment'][0] != 'none':
            self.performAilment(opponent_pokemon)
            if opponent_pokemon['current_hp'] == 0:
                self.opponent.getState()['current_active_pokemon'] += 1


    def performAilment(self, pokemon):
        ailment = pokemon['ailment'][0]
        if ailment in ['sleep', 'paralysis']:
            pass # Handle count decrement in performMove
        elif ailment == 'poison':
            pokemon['current_hp'] -= 1.0 / 16 * self.getStat(pokemon, 1)
            pokemon['current_hp'] = max(0, pokemon['current_hp'])

    def run(self):
        counter = 0
        while not self.isGameOver() and counter < 500:
            self.performTurn()
            counter += 1
        if not self.isGameOver():
            return 'timeout'
        else:
            return self.isGameOver()

    def getMoveTarget(self, move_id, target_id):
        # Returns 0 if move affects self, and 1 if move affects the other pokemon
        if target_id in set([3, 4, 5, 7, 13]):
            return 0
        elif target_id in set([1, 6, 8, 9, 10, 11]):
            return 1
        raise Exception('move_target({}) not implemented. Move: {}'.format(str(target_id), str(move_id)))

    def calculateDamage(self, from_pokemon, to_pokemon, move):
        move_damage_class = move['damage_class_id']
        power = 0 if move['power'] == None else move['power']
        damage_to_inflict = (( (2 * from_pokemon['level'] / 5 + 2) * power * self.getStat(from_pokemon,move_damage_class) / self.getStat(to_pokemon, move_damage_class + 1)) / 50 + 2)
        type_modifier = 1.0
        same_type_attack_bonus = 1.0
        for t in to_pokemon['type']:
            type_modifier *= self.type_efficacy_loader.getTypeEfficacy(move['type_id'], t)
            if move['type_id'] == t:
                same_type_attack_bonus = 1.5
        modifier = type_modifier * same_type_attack_bonus
        damage_to_inflict *= modifier
        return damage_to_inflict

    def statNameToIndex(self, name):
        if name == 'hp':
            return 1
        elif name == 'attack':
            return 2
        elif name == 'defense':
            return 3
        elif name == 'special-attack':
            return 4
        elif name == 'special-defense':
            return 5
        elif name == 'speed':
            return 6
        elif name == 'accuracy':
            return 7
        elif name == 'evasion':
            return 8
        raise Exception('Stat({}) does not have an index.'.format(name))

    def performMove(self, game, from_pokemon, to_pokemon, move, move_index):
        # Ailment
        if from_pokemon['ailment'][0] in ['sleep', 'paralysis']:
            from_pokemon['ailment'][1] -= 1
            if from_pokemon['ailment'][1] == 0:
                from_pokemon['ailment'][0] = 'none'
            return

        move_target = self.getMoveTarget(move['identifier'], move['target_id'])
        if move_target == 0:
            target_pokemon = from_pokemon
        else:
            # move_target == 1
            target_pokemon = to_pokemon

        move_category = move['meta']['category']['name']
        if move_category in ['damage', 'damage+lower', 'damage+ailment', 'damage+raise', 'damage+heal']:
            # Ignore stat changes and ailment
            damage_to_inflict = self.calculateDamage(from_pokemon, target_pokemon, move)
            target_pokemon['current_hp'] = max(target_pokemon['current_hp'] - damage_to_inflict, 0)
            if move_category == 'damage+heal':
                max_hp = self.getStat(from_pokemon, 1)
                from_pokemon['current_hp'] = min(from_pokemon['current_hp'] + float(int(move['meta']['drain'])) / 100 * max_hp, max_hp)
        elif move_category == 'ailment':
            ailment = move['meta']['ailment']['name']
            if ailment in ['sleep', 'poison', 'paralysis']:
                if target_pokemon['ailment'][0] == 'none':
                    target_pokemon['ailment'][0] = ailment
                    if ailment in ['sleep', 'paralysis']:
                        target_pokemon['ailment'][1] = 2
                else:
                    pass # Cannot change ailment of target pokemon
            else:
                pass # Ignore other ailments
        elif move_category == 'net-good-stats':
            for stat_change in move['stat_changes']:
                stat_index = self.statNameToIndex(stat_change['stat']['name'])
                new_stat_stage = target_pokemon['stat_stages'][stat_index] + stat_change['change']
                if new_stat_stage < -6:
                    new_stat_stage = -6
                elif new_stat_stage > 6:
                    new_stat_stage = 6
                target_pokemon['stat_stages'][stat_index] = new_stat_stage
        elif move_category == 'heal':
            max_hp = self.getStat(target_pokemon, 1)
            target_pokemon['current_hp'] = min(target_pokemon['current_hp'] + float(int(move['meta']['drain'])) / 100 * max_hp, max_hp)
        else:
            raise Exception('Move category({}) not implemented. Move: {}'.format(move_category, move['identifier']))

        if 0 <= move_index < 4: # Struggle doesn't have PP
            from_pokemon['pp'][move_index] -= 1

    def getLegalActions(self, name):
        # TODO: Switching Pokemon
        agent = self.player if name == 'player' else self.opponent
        current_pokemon = self.agentCurrentPokemon(agent)
        legal_actions = [i for i in range(len(current_pokemon['moves'])) if current_pokemon['pp'][i] > 0]
        if len(legal_actions) == 0:
            legal_actions.append(-1) # Struggle
        return legal_actions
