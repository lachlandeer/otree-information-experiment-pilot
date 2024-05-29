
from otree.api import *
c = cu

doc = ''
class C(BaseConstants):
    NAME_IN_URL = 'GroupPreferenceElicitation'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
class Subsession(BaseSubsession):
    pass
class Group(BaseGroup):
    pass
class Player(BasePlayer):
    Individualism = models.StringField(choices=[['Individualist', 'Statement A'], ['Collectivist', 'Statement B']], initial='False', label='', widget=widgets.RadioSelectHorizontal)
    Uncertainty = models.StringField(choices=[['Avoider', 'Statement A'], ['Seeker', 'Statement B']], label='', widget=widgets.RadioSelectHorizontal)
class Collectivism_vs_Individualism(Page):
    form_model = 'player'
    form_fields = ['Individualism']
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        participant = player.participant
        participant.vars['Individualism'] = player.Individualism
class UncertaintyAvoidance(Page):
    form_model = 'player'
    form_fields = ['Uncertainty']
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        participant = player.participant
        participant.vars['Uncertainty'] = player.Uncertainty
class Results(Page):
    form_model = 'player'
    timeout_seconds = 60
    timer_text = 'Time before next task'
page_sequence = [Collectivism_vs_Individualism, UncertaintyAvoidance, Results]