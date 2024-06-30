
from otree.api import *
c = cu

doc = ''
class C(BaseConstants):
    NAME_IN_URL = 'Ending'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    pass

class Results(Page):
    def vars_for_template(player: Player):
        participant = player.participant
        return {
            'selected_app': participant.vars['selected_app'],
            'selected_round': participant.vars['selected_round'],
            'random_payment': participant.vars['random_payment']
        }

page_sequence = [Results]
