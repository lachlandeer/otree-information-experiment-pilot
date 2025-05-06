from otree.api import *
import random

c = cu

doc = ""

class C(BaseConstants):
    NAME_IN_URL = 'Task02'
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


class Player(BasePlayer):
    # Raw signals from CSV
    signal_1 = models.FloatField()
    signal_2 = models.FloatField()
    signal_3 = models.FloatField()
    signal_4 = models.FloatField()

    # position tracking of signals
    display_signal_1 = models.FloatField()
    display_signal_2 = models.FloatField()
    display_signal_3 = models.FloatField()

    # Recipient type treatment
    recipient_type = models.StringField(choices=['Individualist', 'Collectivist'])

    # Allocations
    weight_signal_1 = models.FloatField(label='', max=C.GUESS_MAX, min=0)
    weight_signal_2 = models.FloatField(label='', max=C.GUESS_MAX, min=0)
    weight_signal_3 = models.FloatField(label='', max=C.GUESS_MAX, min=0)
    weight_signal_4 = models.FloatField(label='', max=C.GUESS_MAX, min=0)

    is_bonus_payment_round = models.BooleanField(initial=False)


def load_bonus_tasks_from_csv():
    import csv
    file_path = '_static/data/bonus_stage_01.csv'
    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file)
        tasks = []
        for row in reader:
            tasks.append({
                'task': int(row['task']),
                'signal_1': float(row['signal_1']),
                'signal_2': float(row['signal_2']),
                'signal_3': float(row['signal_3'])#,
                #'signal_4': float(row['signal_4']),
            })
        return tasks


class Instructions(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

    @staticmethod
    def before_next_page(player: Player, timeout_happened=False):
        all_tasks = load_bonus_tasks_from_csv()
        selected_tasks = random.sample(all_tasks, 5)
        player.participant.vars['bonus_tasks'] = selected_tasks

        if player.round_number == 1:
            # Retrieve player's own type
            own_type = player.participant.vars['Individualism']  # 'Individualist' or 'Collectivist'

            # Assign recipient type with 55-45 probability
            if own_type == 'Individualist':
                player.participant.vars['recipient_type'] = (
                    'Individualist' if random.random() < 0.55 else 'Collectivist'
                )
            else:  # own_type == 'Collectivist'
                player.participant.vars['recipient_type'] = (
                    'Collectivist' if random.random() < 0.55 else 'Individualist'
                )

            # 🎯 Select a bonus payment round NOW
            player.participant.vars['bonus_payment_round'] = random.randint(1, C.NUM_ROUNDS)

            # Debugging
            print(
                f"Player {player.id_in_subsession}: own_type = {own_type}, "
                f"recipient_type = {player.participant.vars['recipient_type']}, "
                f"bonus_payment_round = {player.participant.vars['bonus_payment_round']}"
            )

    # @staticmethod
    # def before_next_page(player: Player, timeout_happened=False):
    #     all_tasks = load_bonus_tasks_from_csv()
    #     selected_tasks = random.sample(all_tasks, 5)
    #     player.participant.vars['bonus_tasks'] = selected_tasks

    #     # Assign recipient type ONCE
    #     if player.round_number == 1:
    #         player.participant.vars['recipient_type'] = random.choice(['Individualist', 'Collectivist'])
            
    #         # 🎯 Select a bonus payment round NOW
    #         player.participant.vars['bonus_payment_round'] = random.randint(1, C.NUM_ROUNDS)

    #         # Debugging
    #         print(f"Player {player.id_in_subsession}: bonus payment round = {player.participant.vars['bonus_payment_round']}")



class Example(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1
    
    @staticmethod
    def vars_for_template(player: Player):
        return {
            'recipient_type': player.participant.vars['recipient_type'],
            'uncertainty_type': player.participant.vars['Uncertainty'],
        }


class BonusTask(Page):
    timeout_seconds = 2*60
    form_model = 'player'
    form_fields = ['weight_signal_1', 'weight_signal_2', 'weight_signal_3', 'weight_signal_4']

    @staticmethod
    def vars_for_template(player: Player):
        task = player.participant.vars['bonus_tasks'][player.round_number - 1]

        # Assign real signals
        player.signal_1 = task['signal_1']
        player.signal_2 = task['signal_2']
        player.signal_3 = task['signal_3']
        player.signal_4 = C.MEAN_ASSET_VALUE

        # Map signal numbers to their real values
        signal_values = {
            1: player.signal_1,
            2: player.signal_2,
            3: player.signal_3,
        }

        # Shuffle the display order of signals (just 1, 2, 3, NOT values)
        shuffled_signal_numbers = [1, 2, 3]
        random.shuffle(shuffled_signal_numbers)

        # Save the shuffled positions
        player.display_signal_1 = shuffled_signal_numbers[0]
        player.display_signal_2 = shuffled_signal_numbers[1]
        player.display_signal_3 = shuffled_signal_numbers[2]

        # Map display positions to real signal values
        position_map = {
            player.display_signal_1: (signal_values[1], 'weight_signal_1'),
            player.display_signal_2: (signal_values[2], 'weight_signal_2'),
            player.display_signal_3: (signal_values[3], 'weight_signal_3'),
        }

        # Create members list for rendering
        members = [
            ('Signal 1', position_map[1][0], 'weight_signal_1'),
            ('Signal 2', position_map[2][0], 'weight_signal_2'),
            ('Signal 3', position_map[3][0], 'weight_signal_3'),
        ]

        # Load assigned treatment
        player.recipient_type = player.participant.vars['recipient_type']

        return {
            'members': members,
            'mean_asset_value': C.MEAN_ASSET_VALUE,
            'recipient_type': player.recipient_type,
        }


    @staticmethod
    def error_message(player: Player, values):
        total = sum([values[f'weight_signal_{i}'] for i in range(1, 5)])
        if total != 100.0:
            return 'The allocation of tokens to information must add up to 100'


class Results(Page):
    @staticmethod
    def vars_for_template(player: Player):
        signal_values = {
            1: player.signal_1,
            2: player.signal_2,
            3: player.signal_3,
        }

        members = [
            ('Signal 1', signal_values[player.display_signal_1], player.weight_signal_1),
            ('Signal 2', signal_values[player.display_signal_2], player.weight_signal_2),
            ('Signal 3', signal_values[player.display_signal_3], player.weight_signal_3),
        ]

        return {
            'members': members,
            'mean_asset_value': C.MEAN_ASSET_VALUE,
            'recipient_type': player.recipient_type,
            'weight_signal_4': player.weight_signal_4,
        }
    
    @staticmethod
    def before_next_page(player: Player, timeout_happened=False):
        payment_round = player.participant.vars.get('bonus_payment_round')
        player.is_bonus_payment_round = (player.round_number == payment_round)



page_sequence = [Instructions, 
                 Example, 
                 BonusTask, 
                 Results
                 ]