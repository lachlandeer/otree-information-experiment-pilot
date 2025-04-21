from otree.api import *
import random

c = cu

doc = ""

class C(BaseConstants):
    NAME_IN_URL = 'BonusProblem'
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

    # Shuffled display signals
    display_signal_1 = models.FloatField()
    display_signal_2 = models.FloatField()
    display_signal_3 = models.FloatField()

    # Position tracking
    signal_1_position = models.IntegerField()
    signal_2_position = models.IntegerField()
    signal_3_position = models.IntegerField()
    players_signal_position = models.IntegerField()

    # Recipient type treatment
    recipient_type = models.StringField(choices=['Individualist', 'Collectivist'])

    # Allocations
    weight_signal_1 = models.FloatField(initial=0, label='', max=C.GUESS_MAX, min=0)
    weight_signal_2 = models.FloatField(initial=0, label='', max=C.GUESS_MAX, min=0)
    weight_signal_3 = models.FloatField(initial=0, label='', max=C.GUESS_MAX, min=0)
    weight_signal_4 = models.FloatField(initial=0, label='', max=C.GUESS_MAX, min=0)


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
    def before_next_page(player: Player, timeout_happened):
        all_tasks = load_bonus_tasks_from_csv()
        selected_tasks = random.sample(all_tasks, 5)
        player.participant.vars['bonus_tasks'] = selected_tasks

        # Assign recipient type ONCE
        if player.round_number == 1:
            player.participant.vars['recipient_type'] = random.choice(['Individualist', 'Collectivist'])


class Example(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1


class BonusTask(Page):
    form_model = 'player'
    form_fields = ['weight_signal_1', 'weight_signal_2', 'weight_signal_3', 'weight_signal_4']

    @staticmethod
    def vars_for_template(player: Player):
        task = player.participant.vars['bonus_tasks'][player.round_number - 1]

        # Save original signals
        player.signal_1 = task['signal_1']
        player.signal_2 = task['signal_2']
        player.signal_3 = task['signal_3']
        player.signal_4 = C.MEAN_ASSET_VALUE

        # Shuffle signal display order
        signal_items = [
            ('signal_1', player.signal_1),
            ('signal_2', player.signal_2),
            ('signal_3', player.signal_3),
        ]
        random.shuffle(signal_items)

        player.display_signal_1 = signal_items[0][1]
        player.display_signal_2 = signal_items[1][1]
        player.display_signal_3 = signal_items[2][1]

        for idx, (label, _) in enumerate(signal_items, start=1):
            setattr(player, f'{label}_position', idx)
            if label == 'signal_1':
                player.players_signal_position = idx

        # Load assigned treatment
        player.recipient_type = player.participant.vars['recipient_type']

        return {
            'signal_1': player.display_signal_1,
            'signal_2': player.display_signal_2,
            'signal_3': player.display_signal_3,
            'signal_4': C.MEAN_ASSET_VALUE,
            'players_signal_position': player.players_signal_position,
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
        return {
            'signal_1': player.display_signal_1,
            'signal_2': player.display_signal_2,
            'signal_3': player.display_signal_3,
            'signal_4': C.MEAN_ASSET_VALUE,
            'weights': [
                player.weight_signal_1,
                player.weight_signal_2,
                player.weight_signal_3,
                player.weight_signal_4
            ],
            'recipient_type': player.recipient_type,
        }

page_sequence = [Instructions, 
                 #Example, 
                 BonusTask, 
                 Results
                 ]