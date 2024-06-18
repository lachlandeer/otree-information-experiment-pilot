
from otree.api import *
c = cu

doc = '\nTBA'
class C(BaseConstants):
    NAME_IN_URL = 'asset_live_game'
    PLAYERS_PER_GROUP = 3
    NUM_ROUNDS = 1
    GUESS_MAX = 100
    ENDOWMENT = 100
    MEAN_ASSET_VALUE = 100
    PAYOFF_SCALER = 500
    TASKS = (1, 2)
    N_TASKS = 2
    INSTRUCTIONS_TEMPLATE = 'asset_live_game/instructions.html'

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    sum_guess = models.FloatField()
    signal_1 = models.FloatField()
    signal_2 = models.FloatField()
    signal_3 = models.FloatField()
    asset_value = models.FloatField()
    signal_1_owner = models.StringField()
    signal_2_owner = models.StringField()
    signal_3_owner = models.StringField()
def creating_rounds(group: Group):
    session = group.session
    subsession = group.subsession
    import random
    
    #player = group.player
    
    #randomize the task order
    if subsession.round_number == 1:
        for g in subsession.get_groups():
            round_numbers = list(range(1, C.N_TASKS+1))
            random.shuffle(round_numbers)
    
            # do the full assignment, but will only play the first round        
            for p in group.get_players():
                p.participant.vars['task_rounds'] = dict(zip(C.TASKS, round_numbers))
                print("Matching Rounds to Tasks")
                print(p.participant.vars['task_rounds'])

def set_earnings(group: Group):
    players = group.get_players()
    guesses = [p.guess for p in players]
    
    #print(guesses)
    
    group.sum_guess = sum(guesses)
    #group.avg_guess = group.sum_guess / C.PLAYERS_PER_GROUP
    #print(group.avg_guess)
    
    # not correct, but here for simplicity for the moment
    # are we sure its the average of OTHERS actions?
    # means each player has a different target value
    #group.target_value = 0.5*group.asset_value + 0.5*group.avg_guess
    
    #print(group.target_value)
    
    for p in players:
        p.peer_price = (group.sum_guess - p.guess) / (C.PLAYERS_PER_GROUP - 1)
        p.target_value = 0.5*group.asset_value + 0.5*p.peer_price
    
        p.earnings = C.PAYOFF_SCALER - (p.guess - p.target_value)**2
    
        p.earnings = round(p.earnings, 2)
        #player.target_value = target_value
    
def get_values(group: Group):
    player = group.get_player_by_id(1)
    
    # tasks
    # Nested dictionary having same keys
    tasks = { 
               1: {'task': 1, 
                           'asset_value': 102,
                           'signal_1': {
                               'player': "Player 1",
                               'value': 111
                           },
                           'signal_2': {
                               'player': "Player 2",
                               'value': 125
                           },
    
                           'signal_3': {
                               'player': "Player 3",
                               'value': 121
                           }
                          },
               2: {'task': 2, 
                           'asset_value': 97,
                           'signal_1': {
                               'player': "Player 1",
                               'value': 114
                           },
                           'signal_2': {
                               'player': "Player 2",
                               'value': 98
                           },
    
                           'signal_3': {
                               'player': "Player 3",
                               'value': 118
                           }
                          }
              }
    
    # get the task for this round -- after randomizing
    print("The round is:")
    print(group.round_number)
    
    #print("We will play the following task:")
    #player.participant.vars['task_rounds'][player.round_number]
    task_index = player.participant.vars['task_rounds'][group.round_number]
    #print(task_index)
    #this_task = tasks[group.round_number]
    this_task = tasks[task_index]
    #print(this_task)
    
    return(this_task)

def order_signals(group: Group):
    import random
    
    task = get_values(group)
    
    signals = {k: v for k, v in task.items() if k.startswith('signal')}
    
    # random signal order
    keys_to_reorder = list(signals.items())
    random.shuffle(keys_to_reorder)
    signals_shuffled = dict(keys_to_reorder)
    
    # rename signals for display
    new_key = ["signal_1", "signal_2", "signal_3"]
    task_ordered = dict(zip(new_key, list(signals_shuffled.values())))
    
    # add the asset value back in with the shuffled signals
    task_ordered['asset_value'] = task['asset_value']
    
    #print("This is the signal order")
    #print(task_ordered)
    
    group.signal_1       = task_ordered['signal_1']['value']
    group.signal_1_owner = task_ordered['signal_1']['player']
    group.signal_2       = task_ordered['signal_2']['value']
    group.signal_2_owner = task_ordered['signal_2']['player']
    group.signal_3       = task_ordered['signal_3']['value']
    group.signal_3_owner = task_ordered['signal_3']['player']
    #group.signal_4 = C.MEAN_ASSET_VALUE
    group.asset_value    = task['asset_value']

class Player(BasePlayer):
    weight_signal_1 = models.FloatField(initial=0, label='', max=C.GUESS_MAX, min=0)
    weight_signal_2 = models.FloatField(initial=0, label='', max=C.GUESS_MAX, min=0)
    weight_signal_3 = models.FloatField(initial=0, label='', max=C.GUESS_MAX, min=0)
    weight_signal_4 = models.FloatField(initial=0, label='', max=C.GUESS_MAX, min=0)
    guess = models.FloatField()
    signal_1 = models.FloatField()
    signal_2 = models.FloatField()
    signal_3 = models.FloatField()
    signal_4 = models.FloatField()
    target_value = models.FloatField()
    asset_value = models.FloatField()
    earnings = models.FloatField()
    peer_price = models.FloatField()

class ChoosingTask(WaitPage):
    after_all_players_arrive = creating_rounds

class SetSignals(WaitPage):
    after_all_players_arrive = order_signals

class Guess(Page):
    form_model = 'player'
    form_fields = ['weight_signal_4', 'weight_signal_1', 'weight_signal_2', 'weight_signal_3']

    @staticmethod
    def vars_for_template(player: Player):
        group = player.group
        
        #task = get_values(group)
        
        #signals = {k: v for k, v in task.items() if k.startswith('signal')}
        #task = order_signals(group)
        
        # rename signals for display
        # new_key = ["signal_1", "signal_2", "signal_3"]
        # task_ordered = dict(zip(new_key, list([group.signal_1, group.signal_2, group.signal_3])))
        task_ordered = {
            "signal_1": group.signal_1,
            "signal_2": group.signal_2,
            "signal_3": group.signal_3
        }
        
        print(task_ordered)

        all_players_data = []
        for p in group.get_players():
            signal_value = None
            signal_owner = None
            if group.signal_1_owner == f"Player {p.id_in_group}":
                signal_value = group.signal_1
                signal_owner = "signal_1"
            elif group.signal_2_owner == f"Player {p.id_in_group}":
                signal_value = group.signal_2
                signal_owner = "signal_2"
            elif group.signal_3_owner == f"Player {p.id_in_group}":
                signal_value = group.signal_3
                signal_owner = "signal_3"

            if p.id_in_group == 1:
                player.signal_1 = signal_value
            elif p.id_in_group == 2:
                player.signal_2 = signal_value
            elif p.id_in_group == 3:
                player.signal_3 = signal_value

            all_players_data.append({
                'id': p.id_in_group,
                'individualism': p.participant.vars['Individualism'],
                'uncertainty': p.participant.vars['Uncertainty'],
                'is_me': p.id_in_group == player.id_in_group,
                'signal_value': signal_value,
                'signal_owner': signal_owner
            })
        
        player.signal_4 = C.MEAN_ASSET_VALUE
        player.asset_value = group.asset_value
        
        print(f'Signal 1 owner: {group.signal_1_owner}')
        print(f'Signal 2 owner: {group.signal_2_owner}')
        print(f'Signal 3 owner: {group.signal_3_owner}')

        return {
            'task_ordered': task_ordered,
            'all_players_data': all_players_data,
            'show_icons': True # control whether to display the icons
        }

    @staticmethod
    def js_vars(player: Player):
        
        return dict(
            signal1 = player.signal_1,
            signal2 = player.signal_2,
            signal3 = player.signal_3,
            signal4 = 100
        )

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        # compute guess
        
        guess = 1/100 *(player.signal_4 * player.weight_signal_4 + player.signal_1 * player.weight_signal_1 + player.signal_2 * player.weight_signal_2 + player.signal_3 * player.weight_signal_3)
        
        print("Guess is")
        print(guess)
        
        player.guess = guess
        
    @staticmethod
    def error_message(player: Player, values):
        
        allocated_tokens = values['weight_signal_1'] + values['weight_signal_2'] + values['weight_signal_3'] + values['weight_signal_4']
        
        print(allocated_tokens)
        
        if allocated_tokens != 100.0:
            return 'The allocation of tokens to information must add up to 100'

class ResultsWaitPage(WaitPage):
    after_all_players_arrive = set_earnings

class Results(Page):
    form_model = 'player'
    timeout_seconds = 15
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        participant = player.participant
        import random
        
        # if it's the last round -- we have to pay a random round
        if player.round_number == C.NUM_ROUNDS:
            random_round = random.randint(1, C.NUM_ROUNDS)
        
            participant.vars['selected_round'] = random_round
            #participant.selected_round = random_round
            player_in_selected_round = player.in_round(random_round)
            player.payoff = player_in_selected_round.earnings

class NextRoundSoon(Page):
    form_model = 'player'
    timeout_seconds = 15
    timer_text = 'Time until the next task:'
    @staticmethod
    def is_displayed(player: Player):
        
        return True
    @staticmethod
    def vars_for_template(player: Player):
        participant = player.participant
        
        if player.round_number == C.NUM_ROUNDS:
            payment_round = participant.vars['selected_round']
            return {'payment': payment_round}
        else:
            return dict()
page_sequence = [ChoosingTask, SetSignals, Guess, ResultsWaitPage, Results, NextRoundSoon]