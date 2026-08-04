
from otree.api import *
c = cu

doc = ''
class C(BaseConstants):
    NAME_IN_URL = 'Introduction'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    consent = models.BooleanField(
        choices=[
            [True, "I give my consent to participate in this study, and I have read and acknowledge the information above."],
            [False, "I do not give my consent to participate in this study."]
        ],
        label="",
        widget=widgets.RadioSelect
    )

class Consent(Page):
    form_model = 'player'
    form_fields = ['consent']

class NoConsent(Page):
    @staticmethod
    def is_displayed(player):
        return not player.consent

class Introduction(Page):
    @staticmethod
    def is_displayed(player):
        return player.consent

page_sequence = [Consent, NoConsent, Introduction]
