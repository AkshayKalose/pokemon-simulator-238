import random, math
from agent import Agent

class QLearningAgent(Agent):
    def __init__(self, name, team, Q, learn):
        self.Q = Q
        self.previousState = None
        self.previousAction = None
        self.epsilon = 0.10
        self.alpha = 0.05
        self.gamma = 0.95
        self.end_reward = 100000
        self.learn = learn
        super(QLearningAgent, self).__init__(name, team)

    def normalizePlayerOpponent(self, game):
        if self.name == "player":
            return (game.player, game.opponent)
        else:
            return (game.opponent, game.player)


    def getRLState(self, game):
        # TODO: Extract values for our custom state.
        player, opponent = self.normalizePlayerOpponent(game)

        player_type = game.agentCurrentPokemon(player)['type']
        opponent_type = game.agentCurrentPokemon(opponent)['type']

        # print "player_type", player_type
        # print "opponent_type", opponent_type
        state = {
            'player_hp_bucket': self.numberToBucket(game.agentCurrentHP(player), game.agentTotalHP(player), 10),
            'opponent_hp_bucket': self.numberToBucket(game.agentCurrentHP(opponent), game.agentTotalHP(opponent), 10),
            'player_current_index': player.getState()['current_active_pokemon'],
            'opponent_current_index': opponent.getState()['current_active_pokemon'],
            'player_type_one': player_type[0],
            'player_type_two': player_type[1] if len(player_type) > 1 else None,
            'opponent_type_one': opponent_type[0],
            'opponent_type_two': opponent_type[1] if len(opponent_type) > 1 else None,
        }

        return (
            state['player_hp_bucket'],
            state['opponent_hp_bucket'],
            state['player_current_index'],
            state['opponent_current_index'],
            state['player_type_one'],
            state['player_type_two'],
            state['opponent_type_one'],
            state['opponent_type_two'],
        )

    def getIndexOfFeature(self, feature):
        return ['player_hp_bucket', 'opponent_hp_bucket', 'player_current_index', 'opponent_current_index', 'player_type_one', 'player_type_two', 'opponent_type_one', 'opponent_type_two'].index(feature)

    def numberToBucket(self, number, max, buckets):
        if number == max:
            return buckets - 1
        threshold = float(max) / buckets
        bucket = math.floor(float(number) / threshold)
        return bucket

    def getScore(self, state):
        return state[self.getIndexOfFeature('player_hp_bucket')] - state[self.getIndexOfFeature('opponent_hp_bucket')]

    def getReward(self, game):
        # Calculate reward based on previous state and current game state
        winner = game.isGameOver()
        if winner != False:
            return self.end_reward if winner == self.name else -self.end_reward
        # TODO: Intermediary rewards?
        result = self.getScore(self.getRLState(game)) - self.getScore(self.previousState) if self.previousState is not None else 0
        return result

    def legalActionsToMoveIds(self, game):
        player, _ = self.normalizePlayerOpponent(game)
        result = []
        for a in game.getLegalActions(self.name):
            if a == -1:
                result.append(165) # Struggle
            else:
                # print "moves: ", game.agentCurrentPokemon(player)['moves']
                # print "index: ", a
                result.append(game.agentCurrentPokemon(player)['moves'][a])
        return result

    def moveIdToLegalAction(self, game, move_id):
        if move_id == 165:
            return -1
        player, _ = self.normalizePlayerOpponent(game)
        return game.agentCurrentPokemon(player)['moves'].index(move_id)

    def getAction(self, game):
        if self.learn:
            legal_actions = self.legalActionsToMoveIds(game)
            ### Start Q Update
            s = self.previousState
            a = self.previousAction
            sp = self.getRLState(game)
            r = self.getReward(game)
            if s is not None:
                self.Q[(s, a)] += self.alpha * (r + self.gamma * (max([self.Q[(sp, ap)] for ap in legal_actions])) - self.Q[(s, a)])
            ### End Q Update
            s = sp
            eps = random.uniform(0, 1)
            if eps <= self.epsilon:
                chosen_action = random.choice(legal_actions)
            else:
                max_actions = []
                best_Q_value = float('-inf')
                for action in legal_actions:
                    # print s
                    # print action
                    Q_value = self.Q[(s, action)]
                    if Q_value > best_Q_value:
                        best_Q_value = Q_value
                        max_actions = []
                        max_actions.append(action)
                    elif Q_value == best_Q_value:
                        max_actions.append(action)
                chosen_action = random.choice(max_actions)
            self.previousState = s
            self.previousAction = chosen_action
            # print self.name
            return self.moveIdToLegalAction(game, chosen_action)
        else:
            legal_actions = self.legalActionsToMoveIds(game)
            s = self.getRLState(game)
            max_actions = []
            best_Q_value = float('-inf')
            for action in legal_actions:
                # print s
                # print action
                Q_value = self.Q[(s, action)]
                if Q_value > best_Q_value:
                    best_Q_value = Q_value
                    max_actions = []
                    max_actions.append(action)
                elif Q_value == best_Q_value:
                    max_actions.append(action)
            chosen_action = random.choice(max_actions)
            return self.moveIdToLegalAction(game, chosen_action)
