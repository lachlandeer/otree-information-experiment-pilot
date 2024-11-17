from otree.api import *
from .models import *

class InstructionsCarousel(Page):
    template_name = 'asset_indiv_no_game/InstructionsCarousel.html'

    def is_displayed(self):
        # Use self.player instead of passing player as an argument
        #print(f'Instructions is_displayed called for round {self.player.round_number}')    
        return self.player.round_number == 1

# class AssetValueIllustration(Page):
#     def is_displayed(self):
#         return self.player.round_number == 1

# class ThreeSignalsIllustration(Page):
#     def is_displayed(self):
#         return self.player.round_number == 1

# class Example(Page):
#     def is_displayed(self):
#         return self.player.round_number == 1

class AttentionCheck1(Page):
    form_model = 'player'
    form_fields = ['question_1', 'question_2', 'question_3']

    def check_answers(self):
        """Helper method to check answers and return number correct"""
        correct_answers = 0
        for q in self.form_fields:
            if getattr(self.player, q) == Constants.CORRECT_ANSWERS[q]:
                correct_answers += 1
        return correct_answers

    def before_next_page(self):
        correct_answers = self.check_answers()
        # Store both the pass/fail status and the score
        self.player.participant.vars['attention_check_1_score'] = correct_answers
        self.player.participant.vars['failed_attention_check_1'] = correct_answers < 3

        if correct_answers == 3:
            self.player.participant.vars['disqualified_task_1'] = False

    def is_displayed(self):
        return self.round_number == 1

    def error_message(self, values):
        # Optional: Add error message if you want to prevent blank answers
        for field in self.form_fields:
            if not values[field]:
                return "Please answer all questions before proceeding."

class AttentionCheck2(Page):
    form_model = 'player'
    form_fields = ['question_1', 'question_2', 'question_3']

    def vars_for_template(self):
        # Get the first attention check answers and compare with correct answers
        prev_answers = {
            'q1_correct': self.player.in_round(1).question_1 == Constants.CORRECT_ANSWERS['question_1'],
            'q2_correct': self.player.in_round(1).question_2 == Constants.CORRECT_ANSWERS['question_2'],
            'q3_correct': self.player.in_round(1).question_3 == Constants.CORRECT_ANSWERS['question_3'],
        }
        
        return {
            'previous_answers': prev_answers
        }

    def before_next_page(self):
        correct_answers = 0
        for q in self.form_fields:
            if getattr(self.player, q) == Constants.CORRECT_ANSWERS[q]:
                correct_answers += 1

        if correct_answers < 3:
            self.player.participant.vars['disqualified_task_1'] = True
            self.player.participant.vars['random_payment'] = Constants.FAILED_PAYMENT
        else:
            self.player.participant.vars['disqualified_task_1'] = False

    def is_displayed(self):
        return (self.round_number == 1 and 
                self.player.participant.vars.get('failed_attention_check_1', False))

class Disqualification(Page):
    def is_displayed(self):
        return (self.round_number == 1 and 
                self.player.participant.vars.get('disqualified_task_1', False))

    def vars_for_template(self):
        # Enhanced feedback based on performance
        ac1_score = self.player.participant.vars.get('attention_check_1_score', 0)
        ac2_score = self.player.participant.vars.get('attention_check_2_score', 0)
        
        return {
            'disqualification_message': (
                "You did not pass the attention checks and cannot proceed with this task. "
                "Please proceed to the next part of the study."
            ),
            'first_check_score': ac1_score,
            'second_check_score': ac2_score,
        }

    def app_after_this_page(player, upcoming_apps):
        if player.participant.vars.get('disqualified_task_1', True):
            return "GroupPreferenceElicitation"

class ContinueStudy(Page):
    def before_next_page(self):
        if self.round_number == 1:
            creating_round_order(self.player)
    
    def is_displayed(self):
        return (self.round_number == 1 and 
                not self.player.participant.vars.get('disqualified_task_1', False))

# class CreateTaskOrder(WaitPage):
#     def after_all_players_arrive(self):
#         # Loop through all players and call creating_round_order for each
#         for player in self.group.get_players():
#             creating_round_order(player)
#     # after_all_players_arrive = creating_round_order

#     def is_displayed(self):
#         return True

class Guess(Page):
    timeout_seconds = 10*60
    form_model = 'player'
    form_fields = ['weight_signal_1', 'weight_signal_2', 'weight_signal_3', 'weight_signal_4']

    def vars_for_template(self):
        # Retrieve shuffled values for the current round
        shuffled_values = self.player.participant.vars['shuffled_values']
        current_round_values = shuffled_values[self.round_number - 1]

        # Assign shuffled values to the player for the current round
        self.player.signal_1 = current_round_values['signal_1']
        self.player.signal_2 = current_round_values['signal_2']
        self.player.signal_3 = current_round_values['signal_3']
        self.player.signal_4 = 100  # Always set signal_4 to 100
        self.player.asset_value = current_round_values['asset_value']

        # Return the values to the template (optional, if needed for display)
        return {
            'signal_1': self.player.signal_1,
            'signal_2': self.player.signal_2,
            'signal_3': self.player.signal_3,
            'signal_4': self.player.signal_4,  # Always 100
            'asset_value': self.player.asset_value
        }
    # def vars_for_template(self):
    #     task = get_values()
    #     self.player.signal_1 = task['signal_1']
    #     self.player.signal_2 = task['signal_2']
    #     self.player.signal_3 = task['signal_3']
    #     self.player.signal_4 = Constants.MEAN_ASSET_VALUE
    #     self.player.asset_value = task['asset_value']
    #     return task
    
    def js_vars(self):
        return dict(
            signal1=self.player.signal_1,
            signal2=self.player.signal_2,
            signal3=self.player.signal_3,
            signal4=100
        )

    def before_next_page(self):
        target_value = self.player.asset_value
        guess = 1/100 * (self.player.signal_1 * self.player.weight_signal_1 +
                         self.player.signal_2 * self.player.weight_signal_2 +
                         self.player.signal_3 * self.player.weight_signal_3 +
                         self.player.signal_4 * self.player.weight_signal_4)
        earnings = Constants.PAYOFF_SCALER - (guess - target_value) ** 2
        self.player.earnings = round(earnings, 2)
        self.player.target_value = target_value
        self.player.guess = guess

    def error_message(self, values):
        allocated_tokens = (values['weight_signal_1'] + values['weight_signal_2'] +
                            values['weight_signal_3'] + values['weight_signal_4'])
        if allocated_tokens != 100.0:
            return 'The allocation of tokens to information must add up to 100.'

class Results(Page):
    form_model = 'player'

    def before_next_page(self):
        if self.player.participant.vars['selected_app'] == 'asset_indiv_no_game':
            if self.player.round_number == self.player.participant.vars['selected_round']:
                self.player.participant.vars['random_payment'] = self.player.earnings
                self.player.participant.vars['guess'] = self.player.guess
                self.player.participant.vars['target_value'] = self.player.target_value

class NextRoundSoon(Page):
    form_model = 'player'
    timeout_seconds = 15
    timer_text = 'Time until the next task:'

    def is_displayed(self):
        return True

page_sequence = [
    # Instructions,
    # AssetValueIllustration, 
    # ThreeSignalsIllustration, 
    # Example, 
    InstructionsCarousel,
    AttentionCheck1,
    AttentionCheck2,
    Disqualification,
    ContinueStudy,
    #CreateTaskOrder,
    Guess,
    Results #,
    #NextRoundSoon
]