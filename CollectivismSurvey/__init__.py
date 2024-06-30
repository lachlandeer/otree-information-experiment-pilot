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
    direct = models.IntegerField(choices=[[1, '1'], [2, '2'], [3, '3'], [4, '4'], [5, '5'], [6, '6'], [7, '7']], label='I prefer to be direct and forthright when discussing with people', widget=widgets.RadioSelect)
    unique = models.IntegerField(choices=[[1, '1'], [2, '2'], [3, '3'], [4, '4'], [5, '5'], [6, '6'], [7, '7']], label='I am a unique individual', widget=widgets.RadioSelect)
    own_doing = models.IntegerField(choices=[[1, '1'], [2, '2'], [3, '3'], [4, '4'], [5, '5'], [6, '6'], [7, '7']], label='What happens to me is my own doing', widget=widgets.RadioSelect)
    succeed_abilities = models.IntegerField(choices=[[1, '1'], [2, '2'], [3, '3'], [4, '4'], [5, '5'], [6, '6'], [7, '7']], label='When I succeed, it is usually because of my abilities', widget=widgets.RadioSelect)
    unique_different = models.IntegerField(choices=[[1, '1'], [2, '2'], [3, '3'], [4, '4'], [5, '5'], [6, '6'], [7, '7']], label='I enjoy being unique and different from others in many ways', widget=widgets.RadioSelect)
    
    annoys_me = models.IntegerField(choices=[[1, '1'], [2, '2'], [3, '3'], [4, '4'], [5, '5'], [6, '6'], [7, '7']], label='It annoys me when other people perform better than I do', widget=widgets.RadioSelect)
    competition_law = models.IntegerField(choices=[[1, '1'], [2, '2'], [3, '3'], [4, '4'], [5, '5'], [6, '6'], [7, '7']], label='Competition is the law of nature', widget=widgets.RadioSelect)
    tense_aroused = models.IntegerField(choices=[[1, '1'], [2, '2'], [3, '3'], [4, '4'], [5, '5'], [6, '6'], [7, '7']], label='When another person does better than I do, I get tense and aroused', widget=widgets.RadioSelect)
    competition_good = models.IntegerField(choices=[[1, '1'], [2, '2'], [3, '3'], [4, '4'], [5, '5'], [6, '6'], [7, '7']], label='Without competition, it is not possible to have a good society', widget=widgets.RadioSelect)
    winning_everything = models.IntegerField(choices=[[1, '1'], [2, '2'], [3, '3'], [4, '4'], [5, '5'], [6, '6'], [7, '7']], label='Winning is everything', widget=widgets.RadioSelect)
    job_better = models.IntegerField(choices=[[1, '1'], [2, '2'], [3, '3'], [4, '4'], [5, '5'], [6, '6'], [7, '7']], label='I must do my job better than others', widget=widgets.RadioSelect)
    enjoy_competition = models.IntegerField(choices=[[1, '1'], [2, '2'], [3, '3'], [4, '4'], [5, '5'], [6, '6'], [7, '7']], label='I enjoy working in situations involving competition with others', widget=widgets.RadioSelect)
    not_about_winning = models.IntegerField(choices=[[1, '1'], [2, '2'], [3, '3'], [4, '4'], [5, '5'], [6, '6'], [7, '7']], label='Some people emphasize winning; I\'m not one of them', widget=widgets.RadioSelect)

    well_being = models.IntegerField(choices=[[1, '1'], [2, '2'], [3, '3'], [4, '4'], [5, '5'], [6, '6'], [7, '7']], label='The well-being of my co-workers is important to me', widget=widgets.RadioSelect)
    coworker_proud = models.IntegerField(choices=[[1, '1'], [2, '2'], [3, '3'], [4, '4'], [5, '5'], [6, '6'], [7, '7']], label='If a co-worker gets a prize, I would feel proud', widget=widgets.RadioSelect)
    relative_help = models.IntegerField(choices=[[1, '1'], [2, '2'], [3, '3'], [4, '4'], [5, '5'], [6, '6'], [7, '7']], label='If a relative were in financial difficulty, I would help within my means', widget=widgets.RadioSelect)
    harmony_group = models.IntegerField(choices=[[1, '1'], [2, '2'], [3, '3'], [4, '4'], [5, '5'], [6, '6'], [7, '7']], label='It is important to maintain harmony within my group', widget=widgets.RadioSelect)
    sharing_neighbors = models.IntegerField(choices=[[1, '1'], [2, '2'], [3, '3'], [4, '4'], [5, '5'], [6, '6'], [7, '7']], label='I like sharing little things with my neighbors', widget=widgets.RadioSelect)
    cooperation_feel_good = models.IntegerField(choices=[[1, '1'], [2, '2'], [3, '3'], [4, '4'], [5, '5'], [6, '6'], [7, '7']], label='I feel good when I cooperate with others', widget=widgets.RadioSelect)
    happiness_depends = models.IntegerField(choices=[[1, '1'], [2, '2'], [3, '3'], [4, '4'], [5, '5'], [6, '6'], [7, '7']], label='My happiness depends very much on the happiness of those around me', widget=widgets.RadioSelect)
    pleasure_time = models.IntegerField(choices=[[1, '1'], [2, '2'], [3, '3'], [4, '4'], [5, '5'], [6, '6'], [7, '7']], label='To me, pleasure is spending time with others', widget=widgets.RadioSelect)
    
    family_sacrifice = models.IntegerField(choices=[[1, '1'], [2, '2'], [3, '3'], [4, '4'], [5, '5'], [6, '6'], [7, '7']], label='I would sacrifice an activity that I enjoy very much if my family did not approve of it', widget=widgets.RadioSelect)
    please_family = models.IntegerField(choices=[[1, '1'], [2, '2'], [3, '3'], [4, '4'], [5, '5'], [6, '6'], [7, '7']], label='I would do what would please my family, even if I detested that activity', widget=widgets.RadioSelect)
    consult_family = models.IntegerField(choices=[[1, '1'], [2, '2'], [3, '3'], [4, '4'], [5, '5'], [6, '6'], [7, '7']], label='Before taking a major trip, I consult with most members of my family and many friends', widget=widgets.RadioSelect)
    self_interest_sacrifice = models.IntegerField(choices=[[1, '1'], [2, '2'], [3, '3'], [4, '4'], [5, '5'], [6, '6'], [7, '7']], label='I usually sacrifice my self-interest for the benefit of my group', widget=widgets.RadioSelect)
    duty_before_pleasure = models.IntegerField(choices=[[1, '1'], [2, '2'], [3, '3'], [4, '4'], [5, '5'], [6, '6'], [7, '7']], label='Children should be taught to place duty before pleasure', widget=widgets.RadioSelect)
    hate_disagree = models.IntegerField(choices=[[1, '1'], [2, '2'], [3, '3'], [4, '4'], [5, '5'], [6, '6'], [7, '7']], label='I hate to disagree with others in my group', widget=widgets.RadioSelect)
    keep_parents = models.IntegerField(choices=[[1, '1'], [2, '2'], [3, '3'], [4, '4'], [5, '5'], [6, '6'], [7, '7']], label='We should keep our aging parents with us at home', widget=widgets.RadioSelect)
    honored_parents = models.IntegerField(choices=[[1, '1'], [2, '2'], [3, '3'], [4, '4'], [5, '5'], [6, '6'], [7, '7']], label='Children should feel honored if their parents receive a distinguished award', widget=widgets.RadioSelect)

class CollectivismPage01(Page):
    form_model = 'player'
    
    def get_form_fields(self):
        form_fields = [
            'own_thing', 'life_independent', 'privacy', 'direct', 'unique', 'own_doing', 'succeed_abilities', 'unique_different',
            'annoys_me', 'competition_law', 'tense_aroused', 'competition_good', 'winning_everything', 'job_better', 'enjoy_competition', 'not_about_winning',
            'well_being', 'coworker_proud', 'relative_help', 'harmony_group', 'sharing_neighbors', 'cooperation_feel_good', 'happiness_depends', 'pleasure_time',
            'family_sacrifice', 'please_family', 'consult_family', 'self_interest_sacrifice', 'duty_before_pleasure', 'hate_disagree', 'keep_parents', 'honored_parents'
        ]
        import random
        random.shuffle(form_fields)
        return form_fields

page_sequence = [CollectivismPage01]