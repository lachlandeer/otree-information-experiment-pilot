from otree.api import *
import csv
import os
from datetime import datetime

class Constants(BaseConstants):
    name_in_url = 'asset_indiv_no_game_duplicate'
    players_per_group = None  # Ensure this is uppercase
    num_rounds = 5
    GUESS_MAX = 100
    ENDOWMENT = 100
    MEAN_ASSET_VALUE = 100
    PAYOFF_SCALER = 500
    MAJORITY_PROBABILITY = 0.55
    TARGET_PER_CELL = 1  # Number of participants to target per condition cell
    OWNERS_ANONYMOUS_PROB = 0.2

    # FAILED_PAYMENT = 100

    # Correct answers for the attention check questions
    CORRECT_ANSWERS = {
        'question_2': '80',  
        'question_1': '101',  
        'question_3': '78',
    }

class Subsession(BaseSubsession):
    owners_anonymous_individualist = models.IntegerField(initial=0)
    owners_anonymous_collectivist = models.IntegerField(initial=0)
    owners_with_type_individualist_majority = models.IntegerField(initial=0)
    owners_with_type_individualist_minority = models.IntegerField(initial=0)
    owners_with_type_collectivist_majority = models.IntegerField(initial=0)
    owners_with_type_collectivist_minority = models.IntegerField(initial=0)

    def creating_session(self):
        import random

        csv_values = load_values_from_csv()

        for p in self.get_players():
            player_values = csv_values.copy()
            random.shuffle(player_values)
            p.participant.vars['shuffled_values'] = player_values

        t = Constants.TARGET_PER_CELL
        self.session.vars['assignment_targets'] = {
            'owners_anonymous_Individualist': t // 2,
            'owners_anonymous_Collectivist': t // 2,
            ('owners_with_type', 'Individualist', 'Majority'): t,
            ('owners_with_type', 'Individualist', 'Minority'): t,
            ('owners_with_type', 'Collectivist', 'Majority'): t,
            ('owners_with_type', 'Collectivist', 'Minority'): t,
        }
        self.session.vars['assignment_counts'] = {
            key: 0 for key in self.session.vars['assignment_targets']
        }


# class Subsession(BaseSubsession):
#     def creating_session(self):
#         import random
#         # Load the CSV values once for the entire session
#         csv_values = load_values_from_csv()

#         for p in self.get_players():
#             # Shuffle once for the player at the start of the session
#             player_values = csv_values.copy()
#             random.shuffle(player_values)

#             # Store shuffled values for all rounds in participant vars
#             p.participant.vars['shuffled_values'] = player_values

def load_values_from_csv():
    import csv
    file_path = '_static/data/asset_indiv_no_game.csv'  # Adjust the path as needed
    with open(file_path, mode='r') as file:
        csv_reader = csv.DictReader(file)
        values = []
        for row in csv_reader:
            values.append({
                'round': int(row['task']),
                'asset_value': float(row['value']),
                'signal_1': float(row['signal_1']),
                'signal_2': float(row['signal_2']),
                'signal_3': float(row['signal_3'])
                #'signal_4': float(row['signal_4']),
            })
    return values

def save_assignment_counts(subsession):
    counts = subsession.session.vars['assignment_counts']

    subsession.owners_anonymous_individualist = counts['owners_anonymous_Individualist']
    subsession.owners_anonymous_collectivist = counts['owners_anonymous_Collectivist']
    subsession.owners_with_type_individualist_majority = counts[('owners_with_type', 'Individualist', 'Majority')]
    subsession.owners_with_type_individualist_minority = counts[('owners_with_type', 'Individualist', 'Minority')]
    subsession.owners_with_type_collectivist_majority = counts[('owners_with_type', 'Collectivist', 'Majority')]
    subsession.owners_with_type_collectivist_minority = counts[('owners_with_type', 'Collectivist', 'Minority')]

    print("=== Final assignment counts (saved to Subsession) ===")
    for cell, count in counts.items():
        print(f"{cell}: {count}")

def export_assignment_counts_to_csv(session):
    counts = session.vars['assignment_counts']

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    session_code = session.code
    filename = f"_static/data/assignment_counts_{session_code}_{timestamp}.csv"

    os.makedirs(os.path.dirname(filename), exist_ok=True)

    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Cell', 'Count'])

        for cell, count in counts.items():
            if isinstance(cell, tuple):
                cell_name = " | ".join(cell)
            else:
                cell_name = cell
            writer.writerow([cell_name, count])

    print(f"Assignment counts exported to {filename}")

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    # Attention check questions
    question_2 = models.StringField(
        label="Suppose that V is determined by the computer to be 80. Which estimate of the Target Value will give you the highest earning?",
        choices=['80', '85', '90', '95'],
        widget=widgets.RadioSelect
    )
    
    question_1 = models.StringField(
        label="Which of the following four numbers is most likely to be selected as V?",
        choices=['85', '90', '101', '110'],
        widget=widgets.RadioSelect
    )

    question_3 = models.StringField(
        label="Suppose that V is selected to be 80. Which of the following four numbers is most likely to appear as a signal?",
        choices=['70', '78', '85', '90'],
        widget=widgets.RadioSelect
    )
    # new fields for your treatments:
    treatment = models.StringField()
    majority_status = models.StringField()
    individualism = models.StringField()

    # Game-related fields
    weight_signal_1 = models.IntegerField(label='', max=Constants.GUESS_MAX, min=0)
    weight_signal_2 = models.IntegerField(label='', max=Constants.GUESS_MAX, min=0)
    weight_signal_3 = models.IntegerField(label='', max=Constants.GUESS_MAX, min=0)
    weight_signal_4 = models.IntegerField(label='', max=Constants.GUESS_MAX, min=0)
    guess = models.FloatField()
    signal_1 = models.FloatField()
    signal_2 = models.FloatField()
    signal_3 = models.FloatField()
    signal_4 = models.FloatField()
    target_value = models.FloatField()
    asset_value = models.FloatField()
    earnings = models.FloatField()
    is_payment_round = models.BooleanField(initial=False)


# def creating_round_order(player: Player):
#     subsession = player.subsession

#     # Ensure this only runs in the first round
#     if subsession.round_number == 1:
#         # Select a random payment app and round for this player
#         selected_app, selected_round = select_random_payment(num_rounds_indiv=Constants.num_rounds, num_rounds_live=10)
        
#         # Store the selected app and round in the player's participant variables
#         player.participant.vars['selected_app'] = selected_app
#         player.participant.vars['selected_round'] = selected_round

#         # Optional: Debugging output to track selected app and round
#         print(f'Player {player.id_in_subsession}: selected app = {selected_app}; selected round = {selected_round}.')

# def creating_round_order(group: Group):
#     subsession = group.subsession
#     if subsession.round_number == 1:
#         for p in subsession.get_players():
#             selected_app, selected_round = select_random_payment(num_rounds_indiv=Constants.num_rounds, num_rounds_live=10)
#             p.participant.vars['selected_app'] = selected_app
#             p.participant.vars['selected_round'] = selected_round
#             print(f'Random payment: selected app = {selected_app}; selected round = {selected_round}.')

