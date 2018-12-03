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
        return agent.getState()['team'][agent.getState()['current_active_pokemon']]

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
        raise Exception('move_target not implemented.' + str(target_id) + " " + str(move_id))

    def performMove(self, game, from_pokemon, to_pokemon, move, move_index):
        # TODO: Implement pokemon move state to reduce PP
        self.getMoveTarget(move['identifier'], move['target_id'])
        move_damage_class = move['damage_class_id']
        power = 0 if move['power'] == None else move['power']
        damage_to_inflict = (( (2 * from_pokemon['level'] / 5 + 2) * power * self.getStat(from_pokemon,move_damage_class) / self.getStat(to_pokemon, move_damage_class + 1)) / 50 + 2)
        modifier = 1
        for t in to_pokemon['type']:
            modifier *= self.type_efficacy_loader.getTypeEfficacy(move['type_id'], t)
        damage_to_inflict *= modifier
        to_pokemon['current_hp'] = max(to_pokemon['current_hp'] - damage_to_inflict, 0)
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
