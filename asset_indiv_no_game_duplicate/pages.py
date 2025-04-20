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
            #self.player.participant.vars['random_payment'] = Constants.FAILED_PAYMENT
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
            ),
            'first_check_score': ac1_score,
            'second_check_score': ac2_score,
        }

    def app_after_this_page(player, upcoming_apps):
        if player.participant.vars.get('disqualified_task_1', True):
            return "RandomPaymentResults"

class ContinueStudy(Page):
    # def before_next_page(self):
    #     if self.round_number == 1:
    #         creating_round_order(self.player)
    
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

# class AssignTreatments(Page):
#     def is_displayed(self):
#         return self.round_number == 1

#     def before_next_page(self):
#         import random

#         p = self.player

#         majority_prob = Constants.MAJORITY_PROBABILITY
#         treatments = ['owners_anonymous', 'owners_with_type']

#         p.treatment = random.choice(treatments)

#         if p.treatment == 'owners_with_type':
#             p.majority_status = 'Majority' if random.random() < majority_prob else 'Minority'
#         else:
#             p.majority_status = 'Not applicable'
        
#         if isinstance(p.treatment, (list, tuple)):
#             p.treatment = p.treatment[0]

#         if isinstance(p.majority_status, (list, tuple)):
#             p.majority_status = p.majority_status[0]

#         p.individualism = p.participant.vars.get('Individualism')
#         p.participant.vars['treatment'] = p.treatment
#         p.participant.vars['majority_status'] = p.majority_status

#         print(f'Participant {p.participant.code}: individualism = {p.individualism}, treatment = {p.treatment}, majority status = {p.majority_status}')

def try_with_type(individualism, counts, targets):
    import random
    if random.random() < 0.6:
        first = ('owners_with_type', individualism, 'Majority')
        second = ('owners_with_type', individualism, 'Minority')
    else:
        first = ('owners_with_type', individualism, 'Minority')
        second = ('owners_with_type', individualism, 'Majority')

    if counts[first] < targets[first]:
        return first
    elif counts[second] < targets[second]:
        return second
    return None

class AssignTreatments(Page):
    def is_displayed(self):
        return self.round_number == 1

    def before_next_page(self):
        import random

        p = self.player
        individualism = p.participant.vars['Individualism']
        counts = self.session.vars['assignment_counts']
        targets = self.session.vars['assignment_targets']

        assigned_cell = None

        # Decide treatment type first
        if random.random() < Constants.OWNERS_ANONYMOUS_PROB:
            anon_cell = f'owners_anonymous_{individualism}'
            if counts[anon_cell] < targets[anon_cell]:
                assigned_cell = anon_cell
            else:
                print(f'{anon_cell} full — rerouting to with_type')
                assigned_cell = try_with_type(individualism, counts, targets)
        else:
            assigned_cell = try_with_type(individualism, counts, targets)
            if assigned_cell is None:
                anon_cell = f'owners_anonymous_{individualism}'
                if counts[anon_cell] < targets[anon_cell]:
                    assigned_cell = anon_cell

        if assigned_cell is None:
            print(f'Participant {p.participant.code}: no open assignment cell, disqualified.')
            p.participant.vars['disqualified_task_1'] = True
            return

        # Assignment logic
        if isinstance(assigned_cell, str) and assigned_cell.startswith('owners_anonymous'):
            p.treatment = 'owners_anonymous'
            p.majority_status = 'Not applicable'
        else:
            p.treatment = 'owners_with_type'
            p.majority_status = assigned_cell[2]

        p.individualism = individualism
        p.participant.vars['treatment'] = p.treatment
        p.participant.vars['majority_status'] = p.majority_status
        p.participant.vars['disqualified_task_1'] = False

        counts[assigned_cell] += 1

        print(f'Participant {p.participant.code} assigned to: {assigned_cell}')
        print('Current assignment counts:')
        for cell, count in counts.items():
            print(f'  {cell}: {count}')


class Guess(Page):
    timeout_seconds = 120
    form_model = 'player'
    form_fields = ['weight_signal_1', 'weight_signal_2', 'weight_signal_3', 'weight_signal_4']

    def vars_for_template(self):
        import random

        individualism = self.player.participant.vars['Individualism']
        treatment = self.player.participant.vars['treatment']
        majority_status = self.player.participant.vars['majority_status']

        # Retrieve signals for current round
        shuffled_values = self.player.participant.vars['shuffled_values']
        current_round_values = shuffled_values[self.round_number - 1]

        self.player.signal_1 = current_round_values['signal_1']
        self.player.signal_2 = current_round_values['signal_2']
        self.player.signal_3 = current_round_values['signal_3']
        self.player.signal_4 = 100
        self.player.asset_value = current_round_values['asset_value']

        # Determine types for other members (only for 'owners_with_type' treatment)
        if treatment == 'owners_with_type':
            if majority_status == 'Majority':
                member2_type = individualism
                member3_type = 'Individualist' if individualism == 'Collectivist' else 'Collectivist'
            else:
                member2_type = 'Individualist' if individualism == 'Collectivist' else 'Collectivist'
                member3_type = individualism
        else:
            member2_type = None
            member3_type = None

        # Define the 3 visible members (in logical order)
        members = [
            {'role': 'You', 'signal': self.player.signal_1, 'weight_field': 'weight_signal_1', 'type': individualism},
            {'role': 'Member 2', 'signal': self.player.signal_2, 'weight_field': 'weight_signal_2', 'type': member2_type},
            {'role': 'Member 3', 'signal': self.player.signal_3, 'weight_field': 'weight_signal_3', 'type': member3_type},
        ]

        # Ensure tracking structure exists
        if 'member_order' not in self.participant.vars:
            self.participant.vars['member_order'] = {}
        if 'member_positions' not in self.participant.vars:
            self.participant.vars['member_positions'] = {}

        # Shuffle positions freshly each round
        random.shuffle(members)
        self.participant.vars['member_order'][self.round_number] = members

        # Save role-to-position mapping for export
        positions = {m['role']: i + 1 for i, m in enumerate(members)}
        self.participant.vars['member_positions'][self.round_number] = positions

        # Write identities to Player fields
        self.player.member_1_identity = members[0]['role']
        self.player.member_2_identity = members[1]['role']
        self.player.member_3_identity = members[2]['role']

        # Determine where each signal ended up
        for idx, m in enumerate(members):
            if m['weight_field'] == 'weight_signal_1':
                self.player.signal_1_position = idx + 1
                if m['role'] == 'You':
                    self.player.players_signal_position = idx + 1
            elif m['weight_field'] == 'weight_signal_2':
                self.player.signal_2_position = idx + 1
                if m['role'] == 'You':
                    self.player.players_signal_position = idx + 1
            elif m['weight_field'] == 'weight_signal_3':
                self.player.signal_3_position = idx + 1
                if m['role'] == 'You':
                    self.player.players_signal_position = idx + 1

        # Generate dynamic labels for table header
        member_labels = [
            f"Member {i+1} (me)" if m['role'] == 'You' else f"Member {i+1}"
            for i, m in enumerate(members)
        ]

        return {
            'individualism': individualism,
            'treatment': treatment,
            'majority_status': majority_status,
            'endowment': Constants.ENDOWMENT,
            'mean_asset_value': Constants.MEAN_ASSET_VALUE,
            'member_labels': member_labels,
            'member_signals': [m['signal'] for m in members],
            'member_types': [m['type'] for m in members],
            'weight_fields': [m['weight_field'] for m in members],
        }



    def js_vars(self):
        return dict(
            signal1=self.player.signal_1,
            signal2=self.player.signal_2,
            signal3=self.player.signal_3,
            signal4=100
        )

    def before_next_page(self):
        #target_value = self.player.asset_value
        guess = 1/100 * (
            self.player.signal_1 * self.player.weight_signal_1 +
            self.player.signal_2 * self.player.weight_signal_2 +
            self.player.signal_3 * self.player.weight_signal_3 +
            self.player.signal_4 * self.player.weight_signal_4
        )
        self.player.guess = guess

    def error_message(self, values):
        allocated_tokens = (
            values['weight_signal_1'] +
            values['weight_signal_2'] +
            values['weight_signal_3'] +
            values['weight_signal_4']
        )
        if allocated_tokens != 100.0:
            return 'The allocation of tokens to information must add up to 100.'



# class Guess(Page):
#     timeout_seconds = 1 * 60
#     form_model = 'player'
#     form_fields = ['weight_signal_1', 'weight_signal_2', 'weight_signal_3', 'weight_signal_4']

#     def vars_for_template(self):
#         individualism = self.player.participant.vars['Individualism']
#         treatment = self.player.participant.vars['treatment']
#         majority_status = self.player.participant.vars['majority_status']

#         # Retrieve shuffled values for the current round
#         shuffled_values = self.player.participant.vars['shuffled_values']
#         current_round_values = shuffled_values[self.round_number - 1]

#         # Assign signals to player variables
#         self.player.signal_1 = current_round_values['signal_1']
#         self.player.signal_2 = current_round_values['signal_2']
#         self.player.signal_3 = current_round_values['signal_3']
#         self.player.signal_4 = 100  # Always 100
#         self.player.asset_value = current_round_values['asset_value']

#         # Prepare variables for template (explicit, no loops!)
#         signals = {
#             'signal_1': self.player.signal_1,
#             'signal_2': self.player.signal_2,
#             'signal_3': self.player.signal_3,
#             'signal_4': self.player.signal_4,
#         }

#         # Determine opposite type
#         opposite_type = 'Collectivist' if individualism == 'Individualist' else 'Individualist'

#         # Prepare owner labels
#         owner_1 = 'Member 1 (me)'
#         owner_2 = 'Member 2'
#         owner_3 = 'Member 3'

#         # Prepare owner types and images
#         if treatment == 'owners_with_type':
#             show_owner_type_info = True

#             # Owner types
#             owner_type_1 = individualism
#             if majority_status == 'Majority':
#                 owner_type_2 = individualism
#             else:
#                 owner_type_2 = opposite_type
#             owner_type_3 = opposite_type

#             # Owner images
#             owner_image_1 = self.get_image_path(owner_type_1)
#             owner_image_2 = self.get_image_path(owner_type_2)
#             owner_image_3 = self.get_image_path(owner_type_3)

#         else:
#             show_owner_type_info = False
#             owner_type_1 = owner_type_2 = owner_type_3 = ''
#             owner_image_1 = owner_image_2 = owner_image_3 = ''

#         return {
#             **signals,
#             'owner_1': owner_1,
#             'owner_2': owner_2,
#             'owner_3': owner_3,
#             'owner_type_1': owner_type_1,
#             'owner_type_2': owner_type_2,
#             'owner_type_3': owner_type_3,
#             'owner_image_1': owner_image_1,
#             'owner_image_2': owner_image_2,
#             'owner_image_3': owner_image_3,
#             'show_owner_type_info': show_owner_type_info,
#             'individualism': individualism,
#             'treatment': treatment,
#             'majority_status': majority_status,
#             'num_rounds': Constants.num_rounds,
#             'endowment': Constants.ENDOWMENT,
#             'mean_asset_value': Constants.MEAN_ASSET_VALUE
#         }


#     def get_image_path(self, owner_type):
#         if owner_type == 'Individualist':
#             return 'data/person.png'
#         elif owner_type == 'Collectivist':
#             return 'data/people.png'
#         else:
#             return ''

#     def js_vars(self):
#         return dict(
#             signal1=self.player.signal_1,
#             signal2=self.player.signal_2,
#             signal3=self.player.signal_3,
#             signal4=100
#         )

#     def before_next_page(self):
#         target_value = self.player.asset_value
#         guess = 1 / 100 * (
#             self.player.signal_1 * self.player.weight_signal_1 +
#             self.player.signal_2 * self.player.weight_signal_2 +
#             self.player.signal_3 * self.player.weight_signal_3 +
#             self.player.signal_4 * self.player.weight_signal_4
#         )
#         self.player.guess = guess

#     def error_message(self, values):
#         allocated_tokens = (
#             values['weight_signal_1'] +
#             values['weight_signal_2'] +
#             values['weight_signal_3'] +
#             values['weight_signal_4']
#         )
#         if allocated_tokens != 100.0:
#             return 'The allocation of tokens to information must add up to 100.'

    

# class Guess(Page):
#     timeout_seconds = 1*60
#     form_model = 'player'
#     form_fields = ['weight_signal_1', 'weight_signal_2', 'weight_signal_3', 'weight_signal_4']

#     def vars_for_template(self):
#         individualism   = self.player.participant.vars['Individualism']
#         treatment       = self.player.participant.vars['treatment']
#         majority_status = self.player.participant.vars['majority_status']
#         # individualism   = self.player.participant.Individualism,
#         # treatment       = self.player.participant.treatment,
#         # majority_status = self.player.participant.majority_status,
#         # Just to confirm it's printing
#         print(f'Participant {self.player.participant.code} has individualism value: {individualism}')
#         print(f'Participant {self.player.participant.code} has treatment value: {treatment}')
#         print(f'Participant {self.player.participant.code} has status value: {majority_status}')

        
#         # Retrieve shuffled values for the current round
#         shuffled_values = self.player.participant.vars['shuffled_values']
#         current_round_values = shuffled_values[self.round_number - 1]

#         # Assign shuffled values to the player for the current round
#         self.player.signal_1 = current_round_values['signal_1']
#         self.player.signal_2 = current_round_values['signal_2']
#         self.player.signal_3 = current_round_values['signal_3']
#         self.player.signal_4 = 100  # Always set signal_4 to 100
#         self.player.asset_value = current_round_values['asset_value']

#         # Return the values to the template (optional, if needed for display)
#         return {
#             'individualism': individualism,
#             'treatment': treatment,
#             'majority_status': majority_status,
#             'signal_1': self.player.signal_1,
#             'signal_2': self.player.signal_2,
#             'signal_3': self.player.signal_3,
#             'signal_4': self.player.signal_4,  # Always 100
#             'asset_value': self.player.asset_value
#         }
#     # def vars_for_template(self):
#     #     task = get_values()
#     #     self.player.signal_1 = task['signal_1']
#     #     self.player.signal_2 = task['signal_2']
#     #     self.player.signal_3 = task['signal_3']
#     #     self.player.signal_4 = Constants.MEAN_ASSET_VALUE
#     #     self.player.asset_value = task['asset_value']
#     #     return task
    
#     def js_vars(self):
#         return dict(
#             signal1=self.player.signal_1,
#             signal2=self.player.signal_2,
#             signal3=self.player.signal_3,
#             signal4=100
#         )

#     def before_next_page(self):
#         target_value = self.player.asset_value
#         guess = 1/100 * (self.player.signal_1 * self.player.weight_signal_1 +
#                          self.player.signal_2 * self.player.weight_signal_2 +
#                          self.player.signal_3 * self.player.weight_signal_3 +
#                          self.player.signal_4 * self.player.weight_signal_4)
#         # earnings = Constants.PAYOFF_SCALER - (guess - target_value) ** 2
#         # self.player.earnings = round(earnings, 2)
#         # self.player.target_value = target_value
#         self.player.guess = guess

#     def error_message(self, values):
#         allocated_tokens = (values['weight_signal_1'] + values['weight_signal_2'] +
#                             values['weight_signal_3'] + values['weight_signal_4'])
#         if allocated_tokens != 100.0:
#             return 'The allocation of tokens to information must add up to 100.'

# class Results(Page):
#     form_model = 'player'

    # def before_next_page(self):
        # if self.player.participant.vars['selected_app'] == 'asset_indiv_no_game':
            # if self.player.round_number == self.player.participant.vars['selected_round']:
                #self.player.participant.vars['random_payment'] = self.player.earnings
                #self.player.payoff = self.player.earnings
                # self.player.participant.vars['guess'] = self.player.guess
                #self.player.participant.vars['target_value'] = self.player.target_value

class Results(Page):
    def vars_for_template(self):
        individualism = self.player.participant.vars['Individualism']
        treatment = self.player.participant.vars['treatment']
        majority_status = self.player.participant.vars['majority_status']

        # Determine opposite type
        opposite_type = 'Collectivist' if individualism == 'Individualist' else 'Individualist'

        # Determine owner types and images based on treatment
        if treatment == 'owners_with_type':
            show_owner_type_info = True

            owner_type_1 = individualism
            owner_type_2 = individualism if majority_status == 'Majority' else opposite_type
            owner_type_3 = opposite_type

            owner_image_1 = self.get_image_path(owner_type_1)
            owner_image_2 = self.get_image_path(owner_type_2)
            owner_image_3 = self.get_image_path(owner_type_3)
        else:
            show_owner_type_info = False
            owner_type_1 = owner_type_2 = owner_type_3 = ''
            owner_image_1 = owner_image_2 = owner_image_3 = ''

        return {
            'owner_1': 'Member 1 (me)',
            'owner_2': 'Member 2',
            'owner_3': 'Member 3',
            'owner_type_1': owner_type_1,
            'owner_type_2': owner_type_2,
            'owner_type_3': owner_type_3,
            'owner_image_1': owner_image_1,
            'owner_image_2': owner_image_2,
            'owner_image_3': owner_image_3,
            'show_owner_type_info': show_owner_type_info,
            'mean_asset_value': Constants.MEAN_ASSET_VALUE,
        }

    @staticmethod
    def get_image_path(owner_type):
        if owner_type == 'Individualist':
            return 'data/person.png'
        elif owner_type == 'Collectivist':
            return 'data/people.png'
        return ''


class NextRoundSoon(Page):
    form_model = 'player'
    timeout_seconds = 15
    timer_text = 'Time until the next task:'

    def is_displayed(self):
        return True

from .models import save_assignment_counts, export_assignment_counts_to_csv

class SaveCounts(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds

    def before_next_page(self):
        if not self.session.vars.get('assignment_counts_saved', False):
            save_assignment_counts(self.subsession)
            export_assignment_counts_to_csv(self.session)
            self.session.vars['assignment_counts_saved'] = True


page_sequence = [
    #InstructionsCarousel,
    #AttentionCheck1,
    #AttentionCheck2,
    #Disqualification,
    #ContinueStudy,
    #CreateTaskOrder,
    AssignTreatments,
    Guess,
    Results,
    SaveCounts #,
    #NextRoundSoon
]