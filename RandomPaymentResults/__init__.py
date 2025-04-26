
from otree.api import *
c = cu

doc = ''
class C(BaseConstants):
    NAME_IN_URL = 'End'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    pass

class DisqualifiedStage01Results(Page):
    @staticmethod
    def vars_for_template(player: Player):
        participant = player.participant
        return {
            'disqualified_stage_1': participant.vars['disqualified_task_1'],
            # 'disqualified_stage_2': participant.vars['disqualified_task_2'],
            #'selected_app': participant.vars['selected_app'],
            #'selected_round': participant.vars['selected_round'],
            #'random_payment': participant.vars['random_payment']
        }

    @staticmethod
    def is_displayed(player):
        return player.round_number == 1 and player.participant.vars.get('disqualified_task_1', True)

# class DisqualifiedStage02Results(Page):
#     def vars_for_template(player: Player):
#         participant = player.participant
#         return {
#             'disqualified_stage_1': participant.vars['disqualified_task_1'],
#             #'disqualified_stage_2': participant.vars['disqualified_task_2'],
#             'selected_app': participant.vars['selected_app'],
#             'selected_round': participant.vars['selected_round'],
#             'random_payment': participant.vars['random_payment']
#         }

#     def is_displayed(player):
#         return player.round_number == 1 and player.participant.vars.get('disqualified_task_2', True)

class Results(Page):
    @staticmethod
    def vars_for_template(player: Player):
        participant = player.participant
        session = player.session

        return {
            # Main task payment
            'main_payment_round': participant.vars['paid_round'],
            'main_target_value': participant.vars['paid_target_value'],
            'main_guess': participant.vars['paid_guess'],
            'main_earnings_points': participant.vars['paid_earnings'],
            'main_earnings_currency': cu(participant.vars['paid_earnings']).to_real_world_currency(session),

            # Bonus task payment (round only, no bonus payoff yet)
            'bonus_payment_round': participant.vars['bonus_payment_round'],

            # Participation fee
            'participation_fee': session.config.get('participation_fee', 0),

            # Total payment (main payment + participation fee)
            'total_payment_now': participant.payoff_plus_participation_fee(),
        }

    # def vars_for_template(player: Player):
    #     participant = player.participant
    #     session = player.session
    #     return {
    #         # 'disqualified_stage_1': participant.vars['disqualified_task_1'],
    #         # 'disqualified_stage_2': participant.vars['disqualified_task_2'],
    #         'selected_app': participant.vars['selected_app'],
    #         'selected_round': participant.vars['selected_round'],
    #         'target_value': participant.vars['target_value'],
    #         'guess': participant.vars['guess'],
    #         'random_payment': participant.vars['random_payment'],
    #         'random_payment_currency': participant.vars['random_payment']/200,
    #         # 'participation_fee': session.config['participation_fee'],
    #         'payoff':  cu(participant.random_payment).to_real_world_currency(session),
    #         'total_payment': participant.payoff_plus_participation_fee()
    #     }
    
    @staticmethod
    def is_displayed(player):
        print(player.participant.vars.get('disqualified_task_1'))
        return player.round_number == 1 and player.participant.vars.get('disqualified_task_1') == False #player.participant.vars.get('disqualified_task_1', False)

page_sequence = [
    DisqualifiedStage01Results,
    #DisqualifiedStage02Results,
    Results
    ]
