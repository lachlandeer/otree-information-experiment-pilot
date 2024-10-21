
from otree.api import *
import csv
import random
c = cu

doc = '\nTBA'
class C(BaseConstants):
    NAME_IN_URL = 'asset_live_game'
    PLAYERS_PER_GROUP = 3
    NUM_ROUNDS = 10
    GUESS_MAX = 100
    ENDOWMENT = 100
    MEAN_ASSET_VALUE = 100
    PAYOFF_SCALER = 500
    FAILED_PAYMENT = 200

    # Correct answers for the attention check questions
    CORRECT_ANSWERS = {
        'question_2': 'Equally Informative',  
        'question_1': '90',  
    }

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    condition = models.IntegerField()
    asset_value = models.IntegerField()
    signal_1 = models.IntegerField()
    signal_2 = models.IntegerField()
    signal_3 = models.IntegerField()
    signal_1_owner = models.IntegerField()
    signal_2_owner = models.IntegerField()
    signal_3_owner = models.IntegerField()
    signal_1_owner_individualism = models.StringField()
    signal_2_owner_individualism = models.StringField()
    signal_3_owner_individualism = models.StringField()
    sum_guess = models.FloatField()

def select_random_payment(num_rounds_bonus: int, num_rounds_live: int):
    import random
    selected_app = random.choice(['bonus', 
                                  'asset_live_game'
                                  ]
                                )
    selected_round = random.randint(1, 
                                    num_rounds_bonus if selected_app == 'bonus' else 
                                    num_rounds_live
                                    )
    return selected_app, selected_round

def creating_round_order(group: Group):
    subsession = group.subsession
    if subsession.round_number == 1:
        for p in subsession.get_players():
            selected_app, selected_round = select_random_payment(num_rounds_bonus=5, num_rounds_live=C.NUM_ROUNDS)
            p.participant.vars['selected_app'] = selected_app
            p.participant.vars['selected_round'] = selected_round
            print(f'Random payment: selected app = {selected_app}; selected round = {selected_round}.')

def set_condition(group: Group):
    # condition = 1 if SSS - signals with no ownership
    # condition = 2 if SSS - effect of ownership
    # condition = 3 if people see the cultural background of other players
    import random
    group.condition = random.randint(1, 3)
    for player in group.get_players():
        player.participant.vars['condition'] = group.condition

# def sample_value(mean_value=100, std_dev=10):
#     # this draws a asset value from a distribution
#     import random
#     import numpy as np
#     from scipy.stats import norm
#     value_range = np.linspace(mean_value - 50, mean_value + 50, 101)
#     pdf_values = norm.pdf(value_range, mean_value, std_dev)
#     random_number = random.choices(value_range, pdf_values)[0]
#     return random_number
def load_values_from_csv():
    # Adjust this path to where your CSV file is located
    file_path = '_static/data/asset_live_game.csv'
    
    with open(file_path, mode='r') as file:
        csv_reader = csv.DictReader(file)
        values = []
        for row in csv_reader:
            values.append({
                'round': int(row['task']),
                'asset_value': int(row['value']),
                'signal_1': int(row['signal_1']),
                'signal_2': int(row['signal_2']),
                'signal_3': int(row['signal_3']),
            })
    return values

def get_values(group: Group):
    import random
    import csv
    # Load CSV values and shuffle them at the group level
    csv_values = load_values_from_csv()

    # Shuffle the values for the group (every group gets a unique shuffled sequence)
    random.shuffle(csv_values)
    
    # Select the values for the current round based on the round number
    current_round_values = csv_values[group.round_number - 1]

    # Assign values to the group
    group.asset_value = current_round_values['asset_value']
    group.signal_1 = current_round_values['signal_1']
    group.signal_2 = current_round_values['signal_2']
    group.signal_3 = current_round_values['signal_3']
    
    # Shuffle player IDs for signal ownership
    player_id_list = list(range(1, 4))  # Assuming 3 players in the group
    random.shuffle(player_id_list)
    
    # Assign signals and ownership to players
    for signal_id, player_id in enumerate(player_id_list):
        player = group.get_player_by_id(player_id)
        player.signal = [group.signal_1, group.signal_2, group.signal_3][signal_id]
        
        if signal_id == 0:
            group.signal_1_owner = player_id
            group.signal_1_owner_individualism = player.participant.vars['Individualism']
        elif signal_id == 1:
            group.signal_2_owner = player_id
            group.signal_2_owner_individualism = player.participant.vars['Individualism']
        elif signal_id == 2:
            group.signal_3_owner = player_id
            group.signal_3_owner_individualism = player.participant.vars['Individualism']
        
        # Assign asset and signal values to players
        player.asset_value = group.asset_value
        player.signal_1 = group.signal_1
        player.signal_2 = group.signal_2
        player.signal_3 = group.signal_3
        player.signal_4 = 100  # Signal 4 is always 100


# def get_values(group: Group):
#     # this draws signals given the asset value
#     import random
#     group.asset_value = int(sample_value())
#     signals = [int(sample_value(mean_value=group.asset_value)) for _ in range(3)]
#     player_id_list = list(range(1, 4))
#     random.shuffle(player_id_list)
#     group.signal_1 = signals[0]
#     group.signal_2 = signals[1]
#     group.signal_3 = signals[2]
#     for signal_id, player_id in enumerate(player_id_list):
#         player = group.get_player_by_id(player_id)
#         player.signal = signals[signal_id]
#         if signal_id == 0:
#             group.signal_1_owner = player_id
#             group.signal_1_owner_individualism = player.participant.vars['Individualism']
#         elif signal_id == 1:
#             group.signal_2_owner = player_id
#             group.signal_2_owner_individualism = player.participant.vars['Individualism']
#         elif signal_id == 2:
#             group.signal_3_owner = player_id
#             group.signal_3_owner_individualism = player.participant.vars['Individualism']
#         player.asset_value = group.asset_value
#         player.signal_1 = signals[0]
#         player.signal_2 = signals[1]
#         player.signal_3 = signals[2]
#         player.signal_4 = 100

def creating_rounds(group: Group):
    get_values(group)

def set_earnings(group: Group):
    players = group.get_players()
    guesses = [p.guess for p in players]
    group.sum_guess = sum(guesses)
    sum_signal_1_weights = sum([p.weight_signal_1 for p in players])
    sum_signal_2_weights = sum([p.weight_signal_2 for p in players])
    sum_signal_3_weights = sum([p.weight_signal_3 for p in players])
    sum_signal_4_weights = sum([p.weight_signal_4 for p in players])
    for p in players:
        p.peer_price = (group.sum_guess - p.guess) / (C.PLAYERS_PER_GROUP - 1)
        p.target_value = 0.5 * group.asset_value + 0.5 * p.peer_price
        p.earnings = C.PAYOFF_SCALER - (p.guess - p.target_value)**2
        p.earnings = round(p.earnings, 2)
        # save record
        task = {
            'round_num': group.round_number,
            'condition': p.participant.vars['condition'],
            'player_id': p.id_in_group,
            'signal': p.signal,
            'signal_1': group.signal_1,
            'signal_1_owner': group.signal_1_owner,
            'signal_1_owner_individualism': group.signal_1_owner_individualism,
            'signal_1_weight': p.weight_signal_1,
            'signal_1_avg_peer_weight': (sum_signal_1_weights - p.weight_signal_1) / 2,
            'signal_2': group.signal_2,
            'signal_2_owner': group.signal_2_owner,
            'signal_2_owner_individualism': group.signal_2_owner_individualism,
            'signal_2_weight': p.weight_signal_2,
            'signal_2_avg_peer_weight': (sum_signal_2_weights - p.weight_signal_2) / 2,
            'signal_3': group.signal_3,
            'signal_3_owner': group.signal_3_owner,
            'signal_3_owner_individualism': group.signal_3_owner_individualism,
            'signal_3_weight': p.weight_signal_3,
            'signal_3_avg_peer_weight': (sum_signal_3_weights - p.weight_signal_3) / 2,
            'signal_4_avg_peer_weight': (sum_signal_4_weights - p.weight_signal_4) / 2
        }
        task_idx = 'task_' + str(group.round_number)
        p.participant.vars[task_idx] = task
        # print(task_idx + ':')
        # print(task)

class Player(BasePlayer):
    # Attention check questions
    question_2 = models.StringField(
        label="How informative is your signal about V compared to that of other participants'?",
        choices=['Less Informative', 'Equally Informative', 'More Informative'],
        widget=widgets.RadioSelect
    )
    
    question_1 = models.StringField(
        label="Suppose that V is determined by the computer to be 80 and the average peer estimate is 100. Which estimate of the Target Value will give you the highest earning?",
        choices=['80', '85', '90', '95'],
        widget=widgets.RadioSelect
    )
    # decision task relevant info
    signal = models.IntegerField()
    weight_signal_1 = models.FloatField(initial=0, label='', max=C.GUESS_MAX, min=0)
    weight_signal_2 = models.FloatField(initial=0, label='', max=C.GUESS_MAX, min=0)
    weight_signal_3 = models.FloatField(initial=0, label='', max=C.GUESS_MAX, min=0)
    weight_signal_4 = models.FloatField(initial=0, label='', max=C.GUESS_MAX, min=0)
    guess = models.FloatField()
    signal_1 = models.IntegerField()
    signal_2 = models.IntegerField()
    signal_3 = models.IntegerField()
    signal_4 = models.IntegerField()
    target_value = models.FloatField()
    asset_value = models.FloatField()
    earnings = models.FloatField()
    peer_price = models.FloatField()

class ConditionSetPage(WaitPage):
    after_all_players_arrive = set_condition
    
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

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

class AttentionCheck1(Page):
    form_model = 'player'
    form_fields = ['question_1', 'question_2']

    @staticmethod
    def before_next_page(player, timeout_happened):
        correct_answers = 0
        if player.question_1 == C.CORRECT_ANSWERS['question_1']:
            correct_answers += 1
        if player.question_2 == C.CORRECT_ANSWERS['question_2']:
            correct_answers += 1

        # If they get any question wrong, flag them for AttentionCheck2
        if correct_answers < 2:
            player.participant.vars['failed_attention_check_2'] = True
        else:
            # If they pass, clear any failure flag
            player.participant.vars['failed_attention_check_2'] = False

    @staticmethod
    def is_displayed(player):
        # Show AttentionCheck1 only in round 1
        return player.round_number == 1


class AttentionCheck2(Page):
    form_model = 'player'
    form_fields = ['question_1', 'question_2']

    @staticmethod
    def before_next_page(player, timeout_happened):
        correct_answers = 0
        if player.question_1 == C.CORRECT_ANSWERS['question_1']:
            correct_answers += 1
        if player.question_2 == C.CORRECT_ANSWERS['question_2']:
            correct_answers += 1

        # If participant fails AttentionCheck2, disqualify them
        if correct_answers < 2:
            player.participant.vars['disqualified_task_2'] = True
            player.participant.vars['random_payment'] = Constants.FAILED_PAYMENT
        else:
            # If they pass, clear any failure flag
            player.participant.vars['disqualified_task_2'] = False

    @staticmethod
    def is_displayed(player):
        # Show AttentionCheck2 only if participant failed AttentionCheck1
        return player.round_number == 1 and player.participant.vars.get('failed_attention_check_2', False)


class Disqualification(Page):
    @staticmethod
    def is_displayed(player):
        return player.round_number == 1 and player.participant.vars.get('disqualified_task_2', False)

    @staticmethod
    def vars_for_template(player):
        return {
            'disqualification_message': "You did not pass the attention check and cannot proceed."
        }

    @staticmethod
    def app_after_this_page(player, upcoming_apps):
        print('upcoming_apps is', upcoming_apps)
        if player.participant.vars.get('disqualified_task_2', True):
            return "CollectivismSurvey"


class ContinueStudy(Page):
    @staticmethod
    def is_displayed(player):
        return player.round_number == 1 and not player.participant.vars.get('disqualified_task_2', False)

class CreatePaymentSelector(WaitPage):
    after_all_players_arrive = creating_round_order

    @staticmethod
    def is_displayed(player: Player):
        return True

class ChoosingTask(WaitPage):
    after_all_players_arrive = creating_rounds
    
    @staticmethod
    def is_displayed(player: Player):
        return True

class Guess(Page):
    form_model = 'player'
    form_fields = ['weight_signal_1', 'weight_signal_2', 'weight_signal_3', 'weight_signal_4']

    @staticmethod
    def vars_for_template(player: Player):
        return {
            'condition': player.participant.vars['condition']
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
        guess = 1/100 * (player.signal_4 * player.weight_signal_4 + player.signal_1 * player.weight_signal_1 + player.signal_2 * player.weight_signal_2 + player.signal_3 * player.weight_signal_3)
        player.guess = guess
        
    @staticmethod
    def error_message(player: Player, values):
        
        allocated_tokens = values['weight_signal_1'] + values['weight_signal_2'] + values['weight_signal_3'] + values['weight_signal_4']
        
        print(allocated_tokens)
        
        if allocated_tokens != 100.0:
            return 'The allocation of tokens to information must add up to 100'
    
    @staticmethod
    def is_displayed(player: Player):
        return True

class ResultsWaitPage(WaitPage):
    after_all_players_arrive = set_earnings
    
    @staticmethod
    def is_displayed(player: Player):
        return True

class Results(Page):
    form_model = 'player'
    timeout_seconds = 15

    @staticmethod
    def vars_for_template(player: Player):
        return {
            'condition': player.participant.vars['condition']
        }
    
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        # check random payment
        participant = player.participant
        if participant.vars['selected_app'] == 'asset_live_game':
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

page_sequence = [
                 ConditionSetPage, 
                 #Instructions, 
                 #AssetValueIllustration, 
                 #ThreeSignalsIllustration, 
                 #Example, 
                 #AttentionCheck1,
                 #AttentionCheck2,
                 #Disqualification,
                 #ContinueStudy,
                 # this line below selects payment for the whole experiment if we don't use the 'no_live'
                 # which i have done for testing
                 # comment the line below out when we play the all games in sequence
                 CreatePaymentSelector,
                 ChoosingTask, 
                 Guess, 
                 ResultsWaitPage, 
                 Results, 
                 NextRoundSoon
                 ]