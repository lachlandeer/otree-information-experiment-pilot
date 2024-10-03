
from otree.api import *
c = cu

doc = '\nTBA'
class C(BaseConstants):
    NAME_IN_URL = 'asset_indiv_no_game'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 5
    GUESS_MAX = 100
    ENDOWMENT = 100
    MEAN_ASSET_VALUE = 100
    PAYOFF_SCALER = 500

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass

def select_random_payment(num_rounds_indiv: int, num_rounds_live: int):
    import random
    selected_app = random.choice(['asset_indiv_no_game', 'asset_live_game', 'bonus'])
    selected_round = random.randint(1, 
                                    # since bonus and no_game are both five rounds this works 
                                    # though a bit hacky 
                                    num_rounds_indiv if selected_app == 'asset_indiv_no_game' else num_rounds_live)
    return selected_app, selected_round

def creating_round_order(group: Group):
    subsession = group.subsession
    if subsession.round_number == 1:
        for p in subsession.get_players():
            selected_app, selected_round = select_random_payment(num_rounds_indiv=C.NUM_ROUNDS, num_rounds_live=10)
            p.participant.vars['selected_app'] = selected_app
            p.participant.vars['selected_round'] = selected_round
            print(f'Random payment: selected app = {selected_app}; selected round = {selected_round}.')

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

def sample_value(mean_value=100, std_dev=10):
    import random
    import numpy as np
    from scipy.stats import norm
    value_range = np.linspace(mean_value - 50, mean_value + 50, 101)
    pdf_values = norm.pdf(value_range, mean_value, std_dev)
    random_number = random.choices(value_range, pdf_values)[0]
    return random_number

def get_values():
    asset_value = int(sample_value())
    signals = [int(sample_value(mean_value=asset_value)) for _ in range(3)]
    task = {
        'asset_value': asset_value,
        'signal_1': signals[0],
        'signal_2': signals[1],
        'signal_3': signals[2]
    }
    return task

class Instructions(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

class AssetValueIllustration(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

class ThreeSignalsIllustration(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

class Example(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

class CreateTaskOrder(WaitPage):
    after_all_players_arrive = creating_round_order

    @staticmethod
    def is_displayed(player: Player):
        return True

class Guess(Page):
    form_model = 'player'
    form_fields = ['weight_signal_1', 'weight_signal_2', 'weight_signal_3', 'weight_signal_4']

    @staticmethod
    def vars_for_template(player: Player):
        task = get_values()
        player.signal_1 = task['signal_1']
        player.signal_2 = task['signal_2']
        player.signal_3 = task['signal_3']
        player.signal_4 = C.MEAN_ASSET_VALUE
        player.asset_value = task['asset_value']
        return task
    
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
        # compute earnings in each round
        target_value = player.asset_value
        guess = 1/100 * (player.signal_1 * player.weight_signal_1 + player.signal_2 * player.weight_signal_2 + player.signal_3 * player.weight_signal_3 + player.signal_4 * player.weight_signal_4)
        earnings = C.PAYOFF_SCALER - (guess - target_value)**2
        player.earnings = round(earnings, 2)
        player.target_value = target_value
        player.guess = guess
        
    @staticmethod
    def error_message(player: Player, values):
        allocated_tokens = values['weight_signal_1'] + values['weight_signal_2'] + values['weight_signal_3'] + values['weight_signal_4']
        if allocated_tokens != 100.0:
            return 'The allocation of tokens to information must add up to 100'
    
    @staticmethod
    def is_displayed(player: Player):
        return True

class Results(Page):
    form_model = 'player'

    @staticmethod
    def vars_for_template(player: Player):
        pass
    
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        participant = player.participant
        if participant.vars['selected_app'] == 'asset_indiv_no_game':
            if player.round_number == participant.vars['selected_round']:
                player.participant.vars['random_payment'] = player.earnings
    
    @staticmethod
    def is_displayed(player: Player):
        return True

class NextRoundSoon(Page):
    form_model = 'player'
    timeout_seconds = 15
    timer_text = 'Time until the next task:'

    @staticmethod
    def is_displayed(player: Player):
        return True

page_sequence = [Instructions, 
                 AssetValueIllustration, 
                 ThreeSignalsIllustration, 
                 Example, 
                 # this line below selects payment for the whole experiment
                 CreateTaskOrder,
                 Guess, 
                 Results, 
                 NextRoundSoon
                 ]