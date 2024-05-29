
from otree.api import *
c = cu

doc = ''
class C(BaseConstants):
    NAME_IN_URL = 'CollectivismSurvey'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
class Subsession(BaseSubsession):
    pass
class Group(BaseGroup):
    pass
class Player(BasePlayer):
    own_thing = models.IntegerField(choices=[[1, '1'], [2, '2'], [3, '3'], [4, '4'], [5, '5'], [6, '6'], [7, '7']], label='I often do "my own thing"', widget=widgets.RadioSelect)
    life_independent = models.IntegerField(choices=[[1, '1'], [2, '2'], [3, '3'], [4, '4'], [5, '5'], [6, '6'], [7, '7']], label="One should live one's life independently of others", widget=widgets.RadioSelect)
    privacy = models.IntegerField(choices=[[1, '1'], [2, '2'], [3, '3'], [4, '4'], [5, '5'], [6, '6'], [7, '7']], label='I like my privacy', widget=widgets.RadioSelect)
    direct = models.IntegerField(choices=[[1, '1'], [2, '2'], [3, '3'], [4, '4'], [5, '5'], [6, '6'], [7, '7']], label='I prefer to be direct and forthright when\xa0discussing with people', widget=widgets.RadioSelect)
    unique = models.IntegerField(choices=[[1, '1'], [2, '2'], [3, '3'], [4, '4'], [5, '5'], [6, '6'], [7, '7']], label='I am a unique individual', widget=widgets.RadioSelect)
    own_doing = models.IntegerField(choices=[[1, '1'], [2, '2'], [3, '3'], [4, '4'], [5, '5'], [6, '6'], [7, '7']], label='What happens to me is my own doing', widget=widgets.RadioSelect)
    succeed_abilities = models.IntegerField(choices=[[1, '1'], [2, '2'], [3, '3'], [4, '4'], [5, '5'], [6, '6'], [7, '7']], label='When I succeed, it is usually because of\xa0my abilities', widget=widgets.RadioSelect)
    unique_different = models.IntegerField(choices=[[1, '1'], [2, '2'], [3, '3'], [4, '4'], [5, '5'], [6, '6'], [7, '7']], label='I enjoy being unique and different from others\xa0in many ways', widget=widgets.RadioSelect)
class CollectivismPage01(Page):
    form_model = 'player'
    form_fields = ['own_thing', 'life_independent', 'privacy', 'direct', 'unique', 'own_doing', 'succeed_abilities', 'unique_different']
page_sequence = [CollectivismPage01]