
from otree.api import *
c = cu

doc = '\nTBA'
class C(BaseConstants):
    NAME_IN_URL = 'asset_indiv_no_game'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 2
    GUESS_MAX = 100
    ENDOWMENT = 100
    MEAN_ASSET_VALUE = 100
    PAYOFF_SCALER = 500
    TASKS = (1, 2)
    INSTRUCTIONS_TEMPLATE = 'asset_indiv_no_game/instructions.html'
class Subsession(BaseSubsession):
    pass
class Group(BaseGroup):
    pass
def creating_round_order(group: Group):
    session = group.session
    subsession = group.subsession
    import random
    if subsession.round_number == 1:
        for p in subsession.get_players():
            round_numbers = list(range(1, C.NUM_ROUNDS+1))
            random.shuffle(round_numbers)
            print(round_numbers)
            p.participant.vars['task_rounds'] = dict(zip(C.TASKS, round_numbers))
            print("Matching Rounds to Tasks")
            print(p.participant.vars['task_rounds'])
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
    is_payment_round = models.BooleanField(initial=False)
def get_values(player: Player):
    participant = player.participant
    #Nested dictionary having same keys
    tasks = { 
               1: {'task': 1, 
                           'asset_value': 102,
                           'signal_1': {
                               'player': "Signal 1",
                               'value': 111
                           },
                           'signal_2': {
                               'player': "Signal 2",
                               'value': 125
                           },
    
                           'signal_3': {
                               'player': "Signal 3",
                               'value': 121
                           }
                          },
               2: {'task': 2, 
                           'asset_value': 97,
                           'signal_1': {
                               'player': "Signal 1",
                               'value': 114
                           },
                           'signal_2': {
                               'player': "Signal 2",
                               'value': 98
                           },
    
                           'signal_3': {
                               'player': "Signal 3",
                               'value': 118
                           }
                          }
              }
    # get the task for this round
    print("The round is:")
    print(player.round_number)
    
    print("We will play the following task:")
    task_index = participant.vars['task_rounds'][player.round_number]
    print(task_index)
    this_task = tasks[task_index]
    print(this_task)
    
    return(this_task)
class CreateTaskOrder(WaitPage):
    after_all_players_arrive = creating_round_order
class Guess(Page):
    form_model = 'player'
    form_fields = ['weight_signal_4', 'weight_signal_1', 'weight_signal_2', 'weight_signal_3']
    @staticmethod
    def vars_for_template(player: Player):
        import random
        
        task = get_values(player)
        
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
        
        player.signal_1 = task_ordered['signal_1']['value']
        player.signal_2 = task_ordered['signal_2']['value']
        player.signal_3 = task_ordered['signal_3']['value']
        player.signal_4 = C.MEAN_ASSET_VALUE
        player.asset_value = task['asset_value']
        
        return task_ordered
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
        # compute earnings in eaach round
        target_value = get_values(player)['asset_value']
        
        guess = 1/100 *(player.signal_4 * player.weight_signal_4 + player.signal_1 * player.weight_signal_1 + player.signal_2 * player.weight_signal_2 + player.signal_3 * player.weight_signal_3)
        
        print("Guess is")
        print(guess)
        
        earnings = C.PAYOFF_SCALER - (guess - target_value)**2
        
        player.earnings = round(earnings, 2)
        
        player.target_value = target_value
        player.guess = guess
        
    @staticmethod
    def error_message(player: Player, values):
        
        allocated_tokens = values['weight_signal_1'] + values['weight_signal_2'] + values['weight_signal_3'] + values['weight_signal_4']
        
        print(allocated_tokens)
        
        if allocated_tokens != 100.0:
            return 'The allocation of tokens to information must add up to 100'
class Results(Page):
    form_model = 'player'
    @staticmethod
    def vars_for_template(player: Player):
        task = get_values(player)
        
        return task
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
page_sequence = [CreateTaskOrder, Guess, Results, NextRoundSoon]