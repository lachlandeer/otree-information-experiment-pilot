from otree.api import *

doc = 'Cognitive Reflection Test (CRT-7) - Frederick (2005) + Toplak, West & Stanovich (2014)'

class Constants(BaseConstants):
    name_in_url = 'CognitiveReflectionTask'
    players_per_group = None
    num_rounds = 1

    CORRECT_ANSWERS = {
        'crt_bat_ball': 5,
        'crt_widgets': 5,
        'crt_lily_pads': 47,
        'crt_barrel': 4,
        'crt_marks': 29,
        'crt_pig': 20,
        'crt_stocks': 3,  # 3 = "has lost money"
    }


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # Item 1: Bat and Ball (Frederick, 2005)
    crt_bat_ball = models.IntegerField(
        label=(
            'A bat and a ball cost £1.10 in total. '
            'The bat costs £1.00 more than the ball. '
            'How much does the ball cost? <b>(in pence)</b>'
        )
    )
    # Item 2: Widgets (Frederick, 2005)
    crt_widgets = models.IntegerField(
        label=(
            'If it takes 5 machines 5 minutes to make 5 widgets, '
            'how long would it take 100 machines to make 100 widgets? '
            '<b>(in minutes)</b>'
        )
    )
    # Item 3: Lily Pads (Frederick, 2005)
    crt_lily_pads = models.IntegerField(
        label=(
            'In a lake, there is a patch of lily pads. Every day, the patch doubles in size. '
            'If it takes 48 days for the patch to cover the entire lake, '
            'how long would it take for the patch to cover half of the lake? '
            '<b>(in days)</b>'
        )
    )
    # Item 4: Barrel (Toplak et al., 2014)
    crt_barrel = models.IntegerField(
        label=(
            'If John can drink one barrel of water in 6 days, '
            'and Mary can drink one barrel of water in 12 days, '
            'how long would it take them to drink one barrel of water together? '
            '<b>(in days)</b>'
        )
    )
    # Item 5: Marks (Toplak et al., 2014)
    crt_marks = models.IntegerField(
        label=(
            'Jerry received both the 15th highest and the 15th lowest mark in the class. '
            'How many students are in the class?'
        )
    )
    # Item 6: Pig (Toplak et al., 2014)
    crt_pig = models.IntegerField(
        label=(
            'A man buys a pig for £60, sells it for £70, '
            'buys it back for £80, and sells it finally for £90. '
            'How much has he made? <b>(in £)</b>'
        )
    )
    # Item 7: Stocks (Toplak et al., 2014) — multiple choice
    crt_stocks = models.IntegerField(
        label=(
            'Simon decided to invest £8,000 in the stock market one day early in 2008. '
            'Six months after he invested, on July 17, the stocks he had purchased were down 50%. '
            'Fortunately for Simon, from July 17 to October 17, the stocks he had purchased went up 75%. '
            'At this point, Simon has:'
        ),
        choices=[
            [1, 'broken even in the stock market'],
            [2, 'is ahead of where he began'],
            [3, 'has lost money'],
        ],
        widget=widgets.RadioSelect
    )

    # Computed score
    crt_score = models.IntegerField(initial=0)


class CRTPage1(Page):
    form_model = 'player'
    form_fields = ['crt_bat_ball', 'crt_widgets', 'crt_lily_pads', 'crt_barrel']

    def get_template_name(self):
        return 'CognitiveReflectionTask.html'


class CRTPage2(Page):
    form_model = 'player'
    form_fields = ['crt_marks', 'crt_pig', 'crt_stocks']

    def get_template_name(self):
        return 'CognitiveReflectionTask.html'

    def before_next_page(player, timeout_happened):
        score = 0
        for field, correct in Constants.CORRECT_ANSWERS.items():
            if getattr(player, field) == correct:
                score += 1
        player.crt_score = score


page_sequence = [CRTPage1, CRTPage2]
