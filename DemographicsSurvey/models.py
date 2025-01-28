from otree.api import *
import csv
import os

author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'DemographicsSurvey'
    players_per_group = None
    num_rounds = 1
    
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

    # Load countries from CSV
    COUNTRY_CHOICES = []
    #root_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    csv_path = os.path.join('_static', 'data', 'countries.csv')
    
    with open(csv_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        COUNTRY_CHOICES = [(row['code'], row['name']) for row in reader]


    csv_path = os.path.join(os.path.dirname(__file__), 'countries.csv')

class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    prolific_id = models.StringField(label='<b>Please enter your Prolific ID:</b>')
    comments = models.LongStringField(label='Please leave any comments in the box below.', blank=True)
    strategy = models.LongStringField(label='What influenced your choices?', blank=False)

    gender = models.IntegerField(
        choices=[[2, 'Female'], [1, 'Male'], [4, 'Prefer not to say'], [3, 'Other']],
        widget=widgets.RadioSelect,
        label='<b>Select your gender.</b>'
    )
    gender_other = models.StringField(blank=True)

    age = models.StringField(
        choices=Constants.AGE_CATEGORIES,
        label="<b>Select your age group:</b>",
        widget=widgets.RadioSelect
    )

    ethnicity = models.StringField(
        choices=Constants.ETHNICITY_GLOBAL_CHOICES,
        label="<b>How would you describe your ethnicity?</b>",
        blank=True,
        widget=widgets.RadioSelect
    )
    ethnicity_other = models.StringField(blank=True, label="If 'Other,' describe your ethnicity:")

    education = models.IntegerField(
        label="<b>What is the highest degree you have completed or are pursuing?</b>",
        choices=[
            [1, 'High school or lower'],
            [2, 'Bachelor degree'],
            [3, 'Master degree'],
            [4, 'PhD degree'],
            [5, 'MBA degree'],
            [6, 'Other'],
            [7, 'Prefer not to say.']
        ],
        widget=widgets.RadioSelect
    )

    # Replace CountryField with StringField
    residence = models.StringField(
        choices=Constants.COUNTRY_CHOICES,
        label="<b>In which country/region do you currently reside?</b>",
        blank=False
    )
    
    nationality = models.StringField(
        choices=Constants.COUNTRY_CHOICES,
        label="<b>In which country/region were you born?</b>",
        blank=False
    )