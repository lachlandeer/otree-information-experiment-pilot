from otree.api import *
c = cu

doc = ''
class Constants(BaseConstants):
    name_in_url = 'CollectivismSurvey'
    players_per_group = None
    num_rounds = 1
    CHOICES = [[1, '1'], [2, '2'], [3, '3'], [4, '4'], [5, '5'], [6, '6'], [7, '7']]


class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    own_thing = models.IntegerField(
        choices=Constants.CHOICES, 
        label='I often do "my own thing"', 
        widget=widgets.RadioSelect
    )
    life_independent = models.IntegerField(
        choices=Constants.CHOICES, 
        label="One should live one's life independently of others", 
        widget=widgets.RadioSelect
    )
    privacy = models.IntegerField(
        choices=Constants.CHOICES, 
        label='I like my privacy', 
        widget=widgets.RadioSelect
    )
    direct = models.IntegerField(
        choices=Constants.CHOICES, 
        label='I prefer to be direct and forthright when discussing with people', 
        widget=widgets.RadioSelect
    )
    unique = models.IntegerField(
        choices=Constants.CHOICES, 
        label='I am a unique individual', 
        widget=widgets.RadioSelect
    )
    own_doing = models.IntegerField(
        choices=Constants.CHOICES, 
        label='What happens to me is my own doing', 
        widget=widgets.RadioSelect
    )
    succeed_abilities = models.IntegerField(
        choices=Constants.CHOICES, 
        label='When I succeed, it is usually because of my abilities', 
        widget=widgets.RadioSelect
    )
    unique_different = models.IntegerField(
        choices=Constants.CHOICES, 
        label='I enjoy being unique and different from others in many ways', 
        widget=widgets.RadioSelect
    )
    annoys_me = models.IntegerField(
        choices=Constants.CHOICES, 
        label='It annoys me when other people perform better than I do', 
        widget=widgets.RadioSelect
    )
    competition_law = models.IntegerField(
        choices=Constants.CHOICES, 
        label='Competition is the law of nature', 
        widget=widgets.RadioSelect
    )
    tense_aroused = models.IntegerField(
        choices=Constants.CHOICES, 
        label='When another person does better than I do, I get tense and aroused', 
        widget=widgets.RadioSelect
    )
    competition_good = models.IntegerField(
        choices=Constants.CHOICES, 
        label='Without competition, it is not possible to have a good society', 
        widget=widgets.RadioSelect
    )
    winning_everything = models.IntegerField(
        choices=Constants.CHOICES, 
        label='Winning is everything', 
        widget=widgets.RadioSelect
    )
    job_better = models.IntegerField(
        choices=Constants.CHOICES, 
        label='I must do my job better than others', 
        widget=widgets.RadioSelect
    )
    enjoy_competition = models.IntegerField(
        choices=Constants.CHOICES, 
        label='I enjoy working in situations involving competition with others', 
        widget=widgets.RadioSelect
    )
    not_about_winning = models.IntegerField(
        choices=Constants.CHOICES, 
        label="Some people emphasize winning; I'm not one of them", 
        widget=widgets.RadioSelect
    )
    well_being = models.IntegerField(
        choices=Constants.CHOICES, 
        label='The well-being of my co-workers is important to me', 
        widget=widgets.RadioSelect
    )
    coworker_proud = models.IntegerField(
        choices=Constants.CHOICES, 
        label='If a co-worker gets a prize, I would feel proud', 
        widget=widgets.RadioSelect
    )
    relative_help = models.IntegerField(
        choices=Constants.CHOICES, 
        label='If a relative were in financial difficulty, I would help within my means', 
        widget=widgets.RadioSelect
    )
    harmony_group = models.IntegerField(
        choices=Constants.CHOICES, 
        label='It is important to maintain harmony within my group', 
        widget=widgets.RadioSelect
    )
    sharing_neighbors = models.IntegerField(
        choices=Constants.CHOICES, 
        label='I like sharing little things with my neighbors', 
        widget=widgets.RadioSelect
    )
    cooperation_feel_good = models.IntegerField(
        choices=Constants.CHOICES, 
        label='I feel good when I cooperate with others', 
        widget=widgets.RadioSelect
    )
    happiness_depends = models.IntegerField(
        choices=Constants.CHOICES, 
        label='My happiness depends very much on the happiness of those around me', 
        widget=widgets.RadioSelect
    )
    pleasure_time = models.IntegerField(
        choices=Constants.CHOICES, 
        label='To me, pleasure is spending time with others', 
        widget=widgets.RadioSelect
    )
    family_sacrifice = models.IntegerField(
        choices=Constants.CHOICES, 
        label='I would sacrifice an activity that I enjoy very much if my family did not approve of it', 
        widget=widgets.RadioSelect
    )
    please_family = models.IntegerField(
        choices=Constants.CHOICES, 
        label='I would do what would please my family, even if I detested that activity', 
        widget=widgets.RadioSelect
    )
    consult_family = models.IntegerField(
        choices=Constants.CHOICES, 
        label='Before taking a major trip, I consult with most members of my family and many friends', 
        widget=widgets.RadioSelect
    )
    self_interest_sacrifice = models.IntegerField(
        choices=Constants.CHOICES, 
        label='I usually sacrifice my self-interest for the benefit of my group', 
        widget=widgets.RadioSelect
    )
    duty_before_pleasure = models.IntegerField(
        choices=Constants.CHOICES, 
        label='Children should be taught to place duty before pleasure', 
        widget=widgets.RadioSelect
    )
    hate_disagree = models.IntegerField(
        choices=Constants.CHOICES, 
        label='I hate to disagree with others in my group', 
        widget=widgets.RadioSelect
    )
    keep_parents = models.IntegerField(
        choices=Constants.CHOICES, 
        label='We should keep our aging parents with us at home', 
        widget=widgets.RadioSelect
    )
    honored_parents = models.IntegerField(
        choices=Constants.CHOICES, 
        label='Children should feel honored if their parents receive a distinguished award', 
        widget=widgets.RadioSelect
    )

# class CollectivismPage01(Page):
#     form_model = 'player'
    
#     def get_form_fields(self):
#         form_fields = [
#             'own_thing', 'life_independent', 'privacy', 'direct', 'unique', 'own_doing', 'succeed_abilities', 'unique_different',
#             'annoys_me', 'competition_law', 'tense_aroused', 'competition_good', 'winning_everything', 'job_better', 'enjoy_competition', 'not_about_winning',
#             'well_being', 'coworker_proud', 'relative_help', 'harmony_group', 'sharing_neighbors', 'cooperation_feel_good', 'happiness_depends', 'pleasure_time',
#             'family_sacrifice', 'please_family', 'consult_family', 'self_interest_sacrifice', 'duty_before_pleasure', 'hate_disagree', 'keep_parents', 'honored_parents'
#         ]
#         import random
#         random.shuffle(form_fields)
#         return form_fields
# page_sequence = [CollectivismPage01]

class Page1(Page):
    form_model = 'player'
    form_fields = [
        'job_better',
        'unique_different',
        'annoys_me',
        'own_doing',
        'life_independent'
    ]
    def get_template_name(self):
        return 'CollectivismSurvey.html'  # Reference your template


class Page2(Page):
    form_model = 'player'
    form_fields = [
        'direct',
        'not_about_winning',
        'enjoy_competition',
        'privacy',
        'own_thing'
    ]
    def get_template_name(self):
        return 'CollectivismSurvey.html'  # Reference your template


class Page3(Page):
    form_model = 'player'
    form_fields = [
        'competition_good',
        'winning_everything',
        'tense_aroused',
        'competition_law',
        'unique',
        'succeed_abilities'
    ]
    def get_template_name(self):
        return 'CollectivismSurvey.html'  # Reference your template


class Page4(Page):
    form_model = 'player'
    form_fields = [
        'hate_disagree',
        'coworker_proud',
        'duty_before_pleasure',
        'relative_help',
        'consult_family'
    ]
    def get_template_name(self):
        return 'CollectivismSurvey.html'  # Reference your template


class Page5(Page):
    form_model = 'player'
    form_fields = [
        'honored_parents',
        'cooperation_feel_good',
        'self_interest_sacrifice',
        'keep_parents',
        'well_being'
    ]
    def get_template_name(self):
        return 'CollectivismSurvey.html'  # Reference your template


class Page6(Page):
    form_model = 'player'
    form_fields = [
        'happiness_depends',
        'family_sacrifice',
        'harmony_group',
        'pleasure_time',
        'sharing_neighbors',
        'please_family'
    ]
    def get_template_name(self):
        return 'CollectivismSurvey.html'  # Reference your template


page_sequence = [Page1, Page2, Page3, Page4, Page5, Page6]

