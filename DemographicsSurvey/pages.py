from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Survey(Page):
    # timeout_seconds = 200

    form_model = 'player'
    form_fields = [ 'gender', 
                    'gender_other', 
                    'age', 
                    'ethnicity', 
                    'ethnicity_other', 
                    'education', 
                    'residence',
                    'nationality',
                    'prolific_id' 
                    # 'ideology', 
                    # 'individualism_1', 
                    # 'individualism_2',
                    # 'cognitive1', 
                    # 'cognitive2', 
                    # 'cognitive3',
                    # 'seat_number'
                    ]

    # in case a participant chooses "Others" as gender or ethnicity but fails to specify
    def error_message(self, values):
        missing = []
        if values['gender'] == 3 and values['gender_other'] is None:
            missing.append('gender')
        if values['ethnicity'] == 5 and values['ethnicity_other'] is None:
            missing.append('ethnicity')
        # if values['party'] == 4 and values['party_other'] is None:
        #     missing.append('political identification')
        if len(missing) > 0:
            if len(missing) == 1:
                msg = 'Please specify your ' + missing[0] + '.'
            if len(missing) == 2:
                msg = 'Please specify your ' + missing[0] + ' and ' + missing[1] + '.'
            # else:
            #     msg = 'Please specify your ' + missing[0] + ', ' + missing[1] + ' and ' + missing[2] + '.'
            return msg

    # bot code when timeout auto complete the value

    # def before_next_page(self):
    #     if self.timeout_happened:
    #         self.player.participant.vars['is_dropout'] = True
    #         self.player.gender = 1
    #         self.player.age = 25
    #         self.player.ethnicity = 2
    #         self.player.education = 3
    #         self.player.residence = 'NZ'
    #         self.player.individualism_1 = 50
    #         self.player.hometown = 'NZ'
    #         self.player.individualism_2 = 50
    #         self.player.party = 3
    #         self.player.ideology = 3
    #         self.player.prolific_id = '123456'

class Comments(Page):
    form_model = 'player'

    form_fields = [ 'comments']

class Strategy(Page):
    def is_displayed(player):
        return player.round_number == 1 and player.participant.vars.get('disqualified_task_1', False)

    form_model = 'player'

    form_fields = [ 'strategy']

page_sequence = [Survey, Strategy, Comments]
