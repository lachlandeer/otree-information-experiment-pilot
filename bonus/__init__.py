from otree.api import *
c = cu

doc = ''
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
    bonus = models.FloatField()
    weight_signal_1 = models.FloatField(initial=0, label='', max=C.GUESS_MAX, min=0)
    weight_signal_2 = models.FloatField(initial=0, label='', max=C.GUESS_MAX, min=0)
    weight_signal_3 = models.FloatField(initial=0, label='', max=C.GUESS_MAX, min=0)
    weight_signal_4 = models.FloatField(initial=0, label='', max=C.GUESS_MAX, min=0)

class Instructions(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

class Example(Page):
    @staticmethod
    def vars_for_template(player: Player):
        return {
            'condition': player.participant.vars['condition']
        }

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        import random
        bonus_task_idx = random.sample(range(1, 11), 5)
        bonus_task_list = []
        for task_idx in bonus_task_idx:
            task = 'task_' + str(task_idx)
            bonus_task_list.append(task)
        player.participant.vars['bonus_tasks'] = bonus_task_list
        # bonus_tasks: ['task_1', 'task_3', 'task_8', 'task_5', 'task_2']

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

class BonusTask(Page):
    form_model = 'player'
    form_fields = ['weight_signal_1', 'weight_signal_2', 'weight_signal_3', 'weight_signal_4']

    @staticmethod
    def vars_for_template(player: Player):
        round_num = player.round_number
        bonus_tasks = player.participant.vars['bonus_tasks']
        task = player.participant.vars[bonus_tasks[round_num - 1]]
        return task
    
    @staticmethod
    def error_message(player: Player, values):
        
        allocated_tokens = values['weight_signal_1'] + values['weight_signal_2'] + values['weight_signal_3'] + values['weight_signal_4']
        
        print(allocated_tokens)
        
        if allocated_tokens != 100.0:
            return 'The allocation of tokens to information must add up to 100'

    @staticmethod
    def is_displayed(player: Player):
        return True
    
class Results(Page):
    form_model = 'player'
    timeout_seconds = 15

    @staticmethod
    def vars_for_template(player: Player):
        round_num = player.round_number
        bonus_tasks = player.participant.vars['bonus_tasks']
        task = player.participant.vars[bonus_tasks[round_num - 1]]
        player.bonus = 1000 - ((player.weight_signal_1 - task['signal_1_avg_peer_weight'])**2 + (player.weight_signal_2 - task['signal_2_avg_peer_weight'])**2 + (player.weight_signal_3 - task['signal_3_avg_peer_weight'])**2 + (player.weight_signal_4 - task['signal_4_avg_peer_weight'])**2)
        return task

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        # check random payment
        participant = player.participant
        # if participant.vars['selected_app'] == 'asset_live_game':
        #     if player.round_number == participant.vars['selected_round']:
        #         player.participant.vars['random_payment'] = player.earnings
    
    @staticmethod
    def is_displayed(player: Player):
        return True

page_sequence = [Instructions, Example, BonusTask, Results]