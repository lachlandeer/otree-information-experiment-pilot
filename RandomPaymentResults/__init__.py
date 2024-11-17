
from otree.api import *
c = cu

doc = ''
class C(BaseConstants):
    NAME_IN_URL = 'End'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    pass

class DisqualifiedStage01Results(Page):
    def vars_for_template(player: Player):
        participant = player.participant
        return {
            'disqualified_stage_1': participant.vars['disqualified_task_1'],
            'disqualified_stage_2': participant.vars['disqualified_task_2'],
            'selected_app': participant.vars['selected_app'],
            'selected_round': participant.vars['selected_round'],
            'random_payment': participant.vars['random_payment']
        }

    def is_displayed(player):
        return player.round_number == 1 and player.participant.vars.get('disqualified_task_1', True)

class DisqualifiedStage02Results(Page):
    def vars_for_template(player: Player):
        participant = player.participant
        return {
            'disqualified_stage_1': participant.vars['disqualified_task_1'],
            'disqualified_stage_2': participant.vars['disqualified_task_2'],
            'selected_app': participant.vars['selected_app'],
            'selected_round': participant.vars['selected_round'],
            'random_payment': participant.vars['random_payment']
        }

    def is_displayed(player):
        return player.round_number == 1 and player.participant.vars.get('disqualified_task_2', True)

class Results(Page):
    def vars_for_template(player: Player):
        participant = player.participant
        return {
            # 'disqualified_stage_1': participant.vars['disqualified_task_1'],
            # 'disqualified_stage_2': participant.vars['disqualified_task_2'],
            'selected_app': participant.vars['selected_app'],
            'selected_round': participant.vars['selected_round'],
            'target_value': participant.vars['target_value'],
            'guess': participant.vars['guess'],
            'random_payment': participant.vars['random_payment']
        }
    
    def is_displayed(player):
        return player.round_number == 1 and player.participant.vars.get('disqualified_task_1', False) and player.participant.vars.get('disqualified_task_2', False)

page_sequence = [
    DisqualifiedStage01Results,
    DisqualifiedStage02Results,
    Results
    ]
