from otree.api import *

# from otree.api import (
#     models,
#     widgets,
#     BaseConstants,
#     BaseSubsession,
#     BaseGroup,
#     BasePlayer,
#     Currency as c,
#     currency_range,
# )
# from django_countries.fields import CountryField

author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'DemographicsSurvey'
    players_per_group = None
    num_rounds = 1
    
    # Define age categories
    AGE_CATEGORIES = [
        ('18-24', '18-24'),
        ('25-34', '25-34'),
        ('35-44', '35-44'),
        ('45-54', '45-54'),
        ('55-64', '55-64'),
        ('65+', '65+'),
    ]
    ETHNICITY_GLOBAL_CHOICES = [
        ('African', 'African'),
        ('East Asian', 'East Asian'),
        ('South Asian', 'South Asian'),
        ('Southeast Asian', 'Southeast Asian'),
        ('Middle Eastern', 'Middle Eastern'),
        ('Hispanic or Latino', 'Hispanic or Latino'),
        ('European', 'European'),
        ('Indigenous', 'Indigenous'),
        ('Mixed or Multiple Ethnic Groups', 'Mixed or Multiple Ethnic Groups'),
        ('Prefer not to say', 'Prefer not to say'),
        ('Other', 'Other'),
    ]


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    
    prolific_id = models.StringField(label='<b>Please enter your Prolific ID:</b>')
    comments = models.LongStringField(label='Please leave any comments you would like to share with us in the box below.', blank=True)
    strategy = models.LongStringField(label='What influenced your choices when deciding how to allocate the 100 tokens across the four pieces of information?', blank=False)

    gender = models.IntegerField(
        choices=[[2, 'Female'],
                 [1, 'Male'],
                 [4, 'I prefer not to say'],
                 [3, 'Other (fill in the blank)']
                 ],
        widget=widgets.RadioSelect,
        label='<b>Select your gender.</b>'
    )
    gender_other = models.StringField(
        blank=True,
    )
    # age = models.IntegerField(
    #     min=18,
    #     max=100,
    #     label='<b>Please enter your age.</b>'
    # )
    # Age selection as a categorical field
    age = models.StringField(
        choices=Constants.AGE_CATEGORIES,
        label="<b>Select your age group:</b>",
        widget=widgets.RadioSelect  # This displays the options as radio buttons
    )

    ethnicity = models.StringField(
        choices=Constants.ETHNICITY_GLOBAL_CHOICES,
        label="<b>How would you describe your ethnicity?</b>",
        blank=True,  # This allows for an unselected default option
        blank_text="Select your ethnicity",  # Custom default placeholder
        widget=widgets.RadioSelect
    )
    
    # Optional field for open-ended response
    ethnicity_other = models.StringField(
        blank=True,
        label="If you selected 'Other,' please describe your ethnicity:",
    )
    # ethnicity = models.IntegerField(
    #     choices=[[1, 'Asian, Asian-American'],
    #              [2, 'Black, African, African-American'],
    #              [3, 'Hispanic, Latino'],
    #              [4, 'White, European, European-American'],
    #              [5, 'I prefer not to say'],
    #              [6, 'Other (fill in the blank)']
    #              ],
    #     widget=widgets.RadioSelect,
    #     label='<b>Select your ethnic background.</b>'
    # )
    # ethnicity_other = models.StringField(
    #     blank=True,
    # )
    education = models.IntegerField(
        label="<b>What is the highest academic degree you have completed.</b> <br> If you are currently actively pursuing one, please select that academic degree.",
        choices=[
            [1, 'High school or lower'],
            [2, 'Bachelor degree'],
            [3, 'Master degree'],
            [4, 'PhD degree'],
            [5, 'MBA degree'],
            [6, 'Other'],
            [7, 'I prefer not to say.']
        ],
        widget=widgets.RadioSelect
    )

    residence = models.StringField(label="In which country/region do you currently reside?")
    # residence = CountryField(
    #     blank_label='(select country)',
    # )

    # individualism_1 = models.IntegerField(
    #     min=1,
    #     max=100,
    # )
    nationality = models.StringField(label="In which country/region were you born?")
    # hometown = CountryField(
    #     blank_label='(select country)',
    # )

    # individualism_2 = models.IntegerField(
    #     min=1,
    #     max=100,
    # )

    # party = models.IntegerField(
    #     choices=[[1, 'Democratic'],
    #              [2, 'Republican'],
    #              [3, 'Independent'],
    #              [4, 'Other (fill in the blank)']],
    #     widget=widgets.RadioSelect,
    #     label='Do you usually think of yourself as a Republican, a Democrat, an Independent, or something else?'
    # )
    # party_other = models.StringField(
    #     blank=True,
    # )
    # ideology = models.IntegerField(
    #     choices=[[1, 'Strongly Liberal'],
    #              [2, 'Somewhat Liberal'],
    #              [3, 'Moderate'],
    #              [4, 'Somewhat Conservative'],
    #              [5, 'Strongly Conservative']],
    #     widget=widgets.RadioSelect,
    #     label='On social issues you are:'
    # )
    # cognitive1 = models.IntegerField(label='')
    # cognitive2 = models.IntegerField(label='')
    # cognitive3 = models.IntegerField(label='')

    # # mturk_id = models.StringField(label='Please enter your Mechanical Turk ID:')
    # seat_number = models.IntegerField(label='Please enter your seat number (the number can be found on your desk).')
