from otree.api import Currency as c, currency_range
# pyrefly: ignore [missing-import]
from ._builtin import Page, WaitPage
# pyrefly: ignore [missing-import]
from .models import Constants
import random


class ConsentForm(Page):
    form_model = 'player'
    form_fields = ['consent']


class GoodBye(Page):
    def is_displayed(self):
        return not self.player.consent


# class DropMobile(Page):
#     def is_displayed(self):
#         return self.player.is_mobile == 1
#         # disable mobile detection
#         # return false


class Screen0(Page):
    form_model = 'player'
    form_fields = ['user_agent_str']

    # def error_message(self, values):
    #     if values['is_mobile'] == 1:
    #         return "Sorry, this study doesn't allow mobile devices. Please re-open the study link with a desktop or laptop computer."


class Screen1(Page):
    pass


class Screen2(Page):
    pass
    # form_model = 'player'
    # form_fields = ['q1_1']


class Screen3(Page):
    pass
    # def is_displayed(self):
    #     return not self.player.is_dropout
    # form_model = 'player'
    # form_fields = ['q2_1']


class Screen4(Page):
    pass
    # def is_displayed(self):
    #     return not self.player.is_dropout
    # form_model = 'player'
    # form_fields = ['q3_1']


class Screen5(Page):
    pass


class Quiz1(Page):
    form_model = 'player'
    form_fields = ['q1_1', 'q2_1', 'q3_1']

    def error_message(self, values):
        player = self.player
        player.quiz_attempts += 1

        errors = []
        if values['q1_1'] != Constants.a1:
            errors.append("Question 1 is incorrect (Hint: Review how Peer Predictions are displayed).")
        if values['q2_1'] != Constants.a2:
            errors.append("Question 2 is incorrect (Hint: Review the accuracy rate of the computer's prediction).")
        if values['q3_1'] != Constants.a3:
            errors.append("Question 3 is incorrect (Hint: Review how your turning point determines which advisor is implemented).")

        if errors:
            return "Please check the following errors: " + " ".join(errors)

    # whether the player has passed the quiz for the first time
    def before_next_page(self):
        player = self.player
        player.pass_quiz1 = True


class Quiz2(Page):
    # if player has passed quiz for the first time, no need to show this page
    def is_displayed(self):
        return not self.player.pass_quiz1

    form_model = 'player'
    form_fields = ['q1_2', 'q2_2', 'q3_2']

    def js_vars(self):
        player = self.player
        return dict(
            a1=str(player.q1_1-1),
            a2=str(player.q2_1-1),
            a3=str(player.q3_1-1)
        )

    # whether player has passed the quiz for the second time
    def before_next_page(self):
        player = self.player
        if player.q1_2 == Constants.a1 and player.q2_2 == Constants.a2 and player.q3_2 == Constants.a3:
            player.pass_quiz2 = True
        else:
            player.is_dropout = True


class Drop(Page):
    def is_displayed(self):
        return self.player.is_dropout


class ChooseAdvisor(Page):
    form_model = 'player'
    form_fields = ['a1', 'a2', 'a3', 'a4', 'a5', 'a6', 'a7', 'a8', 'a9', 'a10', 'a11', 'tp_A', 'tp_B']

    # ensure at least one of turning points is filled and they are consistent with a1-a11
    def error_message(self, values):
        fields = ['a1', 'a2', 'a3', 'a4', 'a5', 'a6', 'a7', 'a8', 'a9', 'a10', 'a11']
        tp_A = 0 if values['tp_A'] is None else values['tp_A']

        if values['tp_A'] is None and values['tp_B'] is None:
            return "Please input the two scenario numbers to complete the two sentences at the bottom of the page."

        # check consistency between tables and sentences
        for a in fields:
            if (int(a[1:]) <= tp_A and values[a] is False) or (int(a[1:]) > tp_A and values[a] is True):
                self.player.inconsistent = self.player.inconsistent + 1
                return "Please make sure that the radio buttons you clicked are consistent with the two scenario numbers you input."

    def before_next_page(self):
        try:
            tp_A = self.player.tp_A
        except TypeError:  # it was NULL
            self.player.tp_A = 0

        # draw ball
        self.player.true_color_blue = bool(random.getrandbits(1))

        # pick a random scenario
        scenario = random.choice(range(1, 12))
        self.player.scenario = scenario

        if self.player.tp_A == 11:
            self.player.advisor_A = True
        elif self.player.tp_A == 0:
            self.player.advisor_A = False
        else:
            self.player.advisor_A = (scenario <= self.player.tp_A)

        # calculate accuracy of advisor B's hint
        accuracy = 0.5 + (scenario - 1) * 0.05

        # determine hint of advisor B under realized accuracy
        if self.player.true_color_blue:
            true_color = 'blue'
            wrong_color = 'red'
        else:
            true_color = 'red'
            wrong_color = 'blue'
        # self.player.hint_B = 'blue'
        self.player.hint_B = random.choices([wrong_color, true_color],
                                            weights=[1 - accuracy, accuracy])[0]


class ChooseColor(Page):
    form_model = 'player'
    form_fields = ['guess_blue']

    def vars_for_template(self):
        # if realized advisor is B, randomly draw a ball according to accuracy and show
        accuracy = 50 + (self.player.scenario - 1) * 5
        if self.player.advisor_A:
            advisor = 'Peer Predictions'
        else:
            advisor = 'Computer Prediction'
        return dict(
            advisor=advisor,
            hint=self.player.hint_B,
            accuracy=accuracy,
        )

    def js_vars(self):
        # if realized advisor is A, send peer decision (list of strings)
        if self.player.advisor_A:
            # if true color of the ball drawn is blue, send corresponding history
            if self.player.true_color_blue:
                return dict(
                    advisor='A',
                    hint=Constants.blue_history,
                )
            else:
                return dict(
                    advisor='A',
                    hint=Constants.red_history,
                )
        # if realized advisor is B, send color (string) of the ball
        else:
            return dict(
                advisor='B',
                hint=self.player.hint_B,
            )

    # calculate payoff
    def before_next_page(self):
        # set payoff
        if self.player.guess_blue == self.player.true_color_blue:
            self.player.payoff = Constants.payoff_correct
            self.participant.vars['part1_payoff'] = Constants.payoff_correct
        else:
            self.player.payoff = Constants.payoff_incorrect
            self.participant.vars['part1_payoff'] = Constants.payoff_incorrect


# page_sequence = [Screen0, GoodBye, Screen1, Screen2, Screen2a, Screen3, Screen3a, Screen4, Screen4a, Drop, Screen5,
#                  ChooseAdvisor, ChooseColor]

page_sequence = [Screen0, Screen1, Screen2, Screen3, Screen4, Screen5, Quiz1,
                 ChooseAdvisor, ChooseColor]

# page_sequence = [Screen0, Quiz1, Quiz2, Drop, ChooseAdvisor, ChooseColor]
