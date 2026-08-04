
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
        import math
        participant = player.participant
        session = player.session

        # Raw values in points
        main_points = float(participant.vars['paid_earnings'])
        conformity_points = float(participant.vars.get('part1_payoff', 0))

        # Convert to GBP (3 decimal places)
        main_gbp = main_points * session.config.get('real_world_currency_per_point', 0.005)
        conformity_gbp = conformity_points * session.config.get('real_world_currency_per_point', 0.005)
        participation_fee = float(session.config.get('participation_fee', 0))

        # Format itemized payments as strings with 3 decimal places
        main_earnings_currency = f"£{main_gbp:.3f}"
        conformity_earnings_currency = f"£{conformity_gbp:.3f}"
        participation_fee_formatted = f"£{participation_fee:.3f}"

        # Calculate raw total GBP
        total_raw_gbp = main_gbp + conformity_gbp + participation_fee

        # Round UP at the very end to 2 decimal places (e.g. 3.501 -> 3.51, 3.505 -> 3.51)
        total_rounded_gbp = math.ceil(round(total_raw_gbp, 4) * 100) / 100
        total_payment_now_formatted = f"£{total_rounded_gbp:.2f}"

        # Adjust the player's payoff so that the database records the rounded up total
        difference_in_gbp = total_rounded_gbp - total_raw_gbp
        difference_in_points = difference_in_gbp / session.config.get('real_world_currency_per_point', 0.005)
        player.payoff = difference_in_points

        return {
            # Main task payment
            'main_payment_round': participant.vars['paid_round'],
            'main_target_value': participant.vars['paid_target_value'],
            'main_guess': participant.vars['paid_guess'],
            'main_earnings_points': participant.vars['paid_earnings'],
            'main_earnings_currency': main_earnings_currency,

            # Bonus task payment (round only, no bonus payoff yet)
            'bonus_payment_round': participant.vars['bonus_payment_round'],

            # Participation fee
            'participation_fee': participation_fee_formatted,

            # Prediction Task payment
            'conformity_earnings_points': participant.vars.get('part1_payoff', 0),
            'conformity_earnings_currency': conformity_earnings_currency,

            # Total payment (rounded up to 2 decimal places at the end)
            'total_payment_now': total_payment_now_formatted,
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
