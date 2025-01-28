from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants

class Survey(Page):
    form_model = 'player'
    form_fields = [
        'gender',
        'gender_other',
        'age',
        'ethnicity',
        'ethnicity_other',
        'education',
        'prolific_id',
        'residence',  # This will use a custom widget
        'nationality',  # This will use a custom widget
    ]


    def error_message(self, values):
        missing = []
        if values['gender'] == 3 and not values['gender_other']:
            missing.append('gender')
        if values['ethnicity'] == 5 and not values['ethnicity_other']:
            missing.append('ethnicity')
        if missing:
            if len(missing) == 1:
                return f"Please specify your {missing[0]}."
            return f"Please specify your {missing[0]} and {missing[1]}."

    def before_next_page(self):
        # Add payment when participant completes the survey
        self.player.payoff += c(200)    

class Comments(Page):
    form_model = 'player'
    form_fields = ['comments']

class Strategy(Page):
    def is_displayed(player):
        return player.round_number == 1 and player.participant.vars.get('disqualified_task_1', False)

    form_model = 'player'
    form_fields = ['strategy']

page_sequence = [Survey, Strategy, Comments]

