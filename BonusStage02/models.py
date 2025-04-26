# extended_bonus_task/models.py
from otree.api import *

class C(BaseConstants):
    NAME_IN_URL = 'BonusStage02'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 5
    GUESS_MAX = 100
    ENDOWMENT = 100
    MEAN_ASSET_VALUE = 100

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    # Original signal values
    signal_1 = models.FloatField()
    signal_2 = models.FloatField()
    signal_3 = models.FloatField()
    signal_4 = models.FloatField()

    # Displayed signal values (after shuffling)
    display_signal_1 = models.FloatField()
    display_signal_2 = models.FloatField()
    display_signal_3 = models.FloatField()

    # Layout
    players_signal_position = models.IntegerField()
    bonus_recipient = models.StringField()
    recipient_type = models.StringField()

    # Token allocations
    weight_signal_1 = models.FloatField()
    weight_signal_2 = models.FloatField()
    weight_signal_3 = models.FloatField()
    weight_signal_4 = models.FloatField()
