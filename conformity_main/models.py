from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as c,
    currency_range,
)
import random

author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'predict_ball_color'
    players_per_group = None
    num_rounds = 1
    payoff_correct = c(50)
    payoff_incorrect = c(5)
    # Hint A (Peer Predictions) depends on true color of the ball drawn
    blue_history = ['blue', 'red', 'red', 'red', 'blue', 'red']  # group 3 in conformity_peer session
    red_history = ['blue', 'red', 'red', 'blue', 'red', 'red']  # group 6 in conformity_peer session
    a1 = 1
    a2 = 1
    a3 = 2


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # whether the participant consent or not
    consent = models.BooleanField(
        choices=[[True, 'I consent; begin the study'],
                 [False, 'I do not consent; I do not wish to participate']],
        widget=widgets.RadioSelect,
    )

    # whether the participant uses a mobile device or not
    # is_mobile = models.IntegerField(initial=0)
    user_agent_str = models.StringField(blank=True)


    is_dropout = models.BooleanField(initial=False)  # set to True if fail to pass the quiz twice

    pass_quiz1 = models.BooleanField(initial=False)  # pass quiz in first attempt
    pass_quiz2 = models.BooleanField(initial=False)  # pass quiz in second attempt
    quiz_attempts = models.IntegerField(initial=0)   # track number of quiz attempts

    q1_1 = models.IntegerField(
        choices=[[1, 'You will see 6 peer predictions from Study X in a chain of colored circles.'],
                 [2, 'You will see a chain of 6 empty circles.']],
        widget=widgets.RadioSelect,
        label='1. Which of the following is true about your Peer Predictions?'
    )
    q1_2 = models.IntegerField(
        choices=[[1, 'You will see 6 peer predictions from Study X in a chain of colored circles.'],
                 [2, 'You will see a chain of 6 empty circles.']],
        widget=widgets.RadioSelect,
        label='1. Which of the following is true about your Peer Predictions?'
    )
    q2_1 = models.IntegerField(
        choices=[[1, 'The computer will show you a color that sometimes—but not always—reflects the actual color of the drawn ball.'],
                 [2, 'The computer will show you a color that always reflects the actual color of the drawn ball.']],
        widget=widgets.RadioSelect,
        label='2. Which of the following is true about Computer Prediction with a success rate lower than 100%?'
    )
    q2_2 = models.IntegerField(
        choices=[[1, 'The computer will show you a color that sometimes—but not always—reflects the actual color of the drawn ball.'],
                 [2, 'The computer will show you a color that always reflects the actual color of the drawn ball.']],
        widget=widgets.RadioSelect,
        label='2. Which of the following is true about Computer Prediction with a success rate lower than 100%?'
    )
    q3_1 = models.IntegerField(
        choices=[[1, 'Peer Predictions will be delivered to you as you preferred. You are glad that you clicked “Computer” for all scenarios including Scenario 2.'],
                 [2, 'Computer Prediction with 55% success rate will be delivered to you based on your choice. You regret you clicked “Computer” for this scenario because you actually prefer Peer Predictions.']],
        widget=widgets.RadioSelect,
        label='3. Suppose that you clicked “Computer” for all 11 scenarios. But when Computer Prediction has a 55% success rate, you would rather see Peer Predictions. Which of the following best describes your situation if Scenario 2 is selected?'
    )
    q3_2 = models.IntegerField(
        choices=[[1, 'Peer Predictions will be delivered to you as you preferred. You are glad that you clicked “Computer” for all scenarios including Scenario 2.'],
                 [2, 'Computer Prediction with 55% success rate will be delivered to you based on your choice. You regret you clicked “Computer” for this scenario because you actually prefer Peer Predictions.']],
        widget=widgets.RadioSelect,
        label='3. Suppose that you clicked “Computer” for all 11 scenarios. But when Computer Prediction has a 55% success rate, you would rather see Peer Predictions. Which of the following best describes your situation if Scenario 2 is selected?'
    )
    true_color_blue = models.BooleanField()
    tp_A = models.IntegerField(min=1, max=11, blank=True)
    tp_B = models.IntegerField(min=1, max=11, blank=True)
    a1 = models.BooleanField(
        choices=[[True, 'Peer'], [False, 'Computer']], widget=widgets.RadioSelectHorizontal,
    )
    a2 = models.BooleanField(
        choices=[[True, 'Peer'], [False, 'Computer']], widget=widgets.RadioSelectHorizontal,
    )
    a3 = models.BooleanField(
        choices=[[True, 'Peer'], [False, 'Computer']], widget=widgets.RadioSelectHorizontal,
    )
    a4 = models.BooleanField(
        choices=[[True, 'Peer'], [False, 'Computer']], widget=widgets.RadioSelectHorizontal,
    )
    a5 = models.BooleanField(
        choices=[[True, 'Peer'], [False, 'Computer']], widget=widgets.RadioSelectHorizontal,
    )
    a6 = models.BooleanField(
        choices=[[True, 'Peer'], [False, 'Computer']], widget=widgets.RadioSelectHorizontal,
    )
    a7 = models.BooleanField(
        choices=[[True, 'Peer'], [False, 'Computer']], widget=widgets.RadioSelectHorizontal,
    )
    a8 = models.BooleanField(
        choices=[[True, 'Peer'], [False, 'Computer']], widget=widgets.RadioSelectHorizontal,
    )
    a9 = models.BooleanField(
        choices=[[True, 'Peer'], [False, 'Computer']], widget=widgets.RadioSelectHorizontal,
    )
    a10 = models.BooleanField(
        choices=[[True, 'Peer'], [False, 'Computer']], widget=widgets.RadioSelectHorizontal,
    )
    a11 = models.BooleanField(
        choices=[[True, 'Peer'], [False, 'Computer']], widget=widgets.RadioSelectHorizontal,
    )
    # whether there's inconsistency between a1-a11 and turning point
    inconsistent = models.IntegerField(initial=0)
    # randomly chosen scenario by computer
    scenario = models.IntegerField()
    # whether player's realized advisor is A or not
    advisor_A = models.BooleanField()
    # hint of advisor B, could be blue or red
    hint_B = models.StringField()
    # whether player guess the color to be blue or not
    guess_blue = models.BooleanField()