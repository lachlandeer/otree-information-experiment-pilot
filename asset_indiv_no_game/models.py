from otree.api import *

class Constants(BaseConstants):
    name_in_url = 'asset_indiv_no_game'
    players_per_group = None  # Ensure this is uppercase
    num_rounds = 2
    GUESS_MAX = 100
    ENDOWMENT = 100
    MEAN_ASSET_VALUE = 100
    PAYOFF_SCALER = 500

    # Correct answers for the attention check questions
    CORRECT_ANSWERS = {
        'question_1': '80',  
        'question_2': '101',  
        'question_3': '78',
    }

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    # Attention check questions
    question_1 = models.StringField(
        label="Suppose that V is determined by the computer to be 80. Which estimate of the Target Value will give you the highest earning?",
        choices=['80', '85', '90', '95'],
        widget=widgets.RadioSelect
    )
    
    question_2 = models.StringField(
        label="Which of the following four numbers is most likely to be selected as V?",
        choices=['85', '90', '101', '110'],
        widget=widgets.RadioSelect
    )

    question_3 = models.StringField(
        label="Suppose that V is selected to be 80. Which of the following four numbers is most likely to appear as a signal?",
        choices=['70', '78', '85', '90'],
        widget=widgets.RadioSelect
    )

    # Game-related fields
    weight_signal_1 = models.FloatField(initial=0, label='', max=Constants.GUESS_MAX, min=0)
    weight_signal_2 = models.FloatField(initial=0, label='', max=Constants.GUESS_MAX, min=0)
    weight_signal_3 = models.FloatField(initial=0, label='', max=Constants.GUESS_MAX, min=0)
    weight_signal_4 = models.FloatField(initial=0, label='', max=Constants.GUESS_MAX, min=0)
    guess = models.FloatField()
    signal_1 = models.FloatField()
    signal_2 = models.FloatField()
    signal_3 = models.FloatField()
    signal_4 = models.FloatField()
    target_value = models.FloatField()
    asset_value = models.FloatField()
    earnings = models.FloatField()
    is_payment_round = models.BooleanField(initial=False)

# Utility functions
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

def creating_round_order(group: Group):
    subsession = group.subsession
    if subsession.round_number == 1:
        for p in subsession.get_players():
            selected_app, selected_round = select_random_payment(num_rounds_indiv=Constants.num_rounds, num_rounds_live=10)
            p.participant.vars['selected_app'] = selected_app
            p.participant.vars['selected_round'] = selected_round
            print(f'Random payment: selected app = {selected_app}; selected round = {selected_round}.')

def select_random_payment(num_rounds_indiv: int, num_rounds_live: int):
    import random
    selected_app = random.choice(['asset_indiv_no_game', 'asset_live_game', 'bonus'])
    selected_round = random.randint(1, num_rounds_indiv if selected_app == 'asset_indiv_no_game' else num_rounds_live)
    return selected_app, selected_round
