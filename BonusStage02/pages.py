from otree.api import *
import random
from .models import *


class InstructionsStage02(Page):
    def is_displayed(self):
        print(f"IN is_displayed(): round_number = {self.player.round_number}")
        return self.round_number == 1

    def before_next_page(self):
        player = self.player
        print(f"Starting before_next_page for player {player.id_in_subsession}")
        print(f"participant vars available: {list(player.participant.vars.keys())}")

        full_round_data = player.participant.vars.get('stage2_task_rounds', {})
        print(f"stage2_task_rounds length: {len(full_round_data)}")
        print(f"stage2_task_rounds keys: {list(full_round_data.keys())}")

        sampled_rounds = random.sample(list(full_round_data.keys()), C.NUM_ROUNDS)
        print(f"Sampled rounds: {sampled_rounds}")

        # ✅ Pick one bonus recipient for the whole stage
        fixed_recipient = random.choice(['Member 2', 'Member 3'])
        player.participant.vars['bonus_recipient_stage02'] = fixed_recipient

        tasks = []
        for r in sampled_rounds:
            original_data = full_round_data[r]
            data = original_data.copy()
            data['round_source'] = r
            data['bonus_recipient'] = fixed_recipient

            owner_types = original_data.get('owner_types', {})
            data['recipient_type'] = owner_types.get(fixed_recipient)

            if data['recipient_type'] is None:
                print(f"❌ recipient_type is None! round {r}, bonus_recipient = {fixed_recipient}")
                print(f"   owner_types = {owner_types}")

            tasks.append(data)

        player.participant.vars['extended_bonus_tasks'] = tasks
        print(f"✅ Successfully created extended_bonus_tasks with {len(tasks)} tasks using fixed recipient: {fixed_recipient}")


        # except Exception as e:
        #     print(f"Error in before_next_page: {e}")
        #     raise


class BonusTaskStage02(Page):
    form_model = 'player'
    form_fields = ['weight_signal_1', 'weight_signal_2', 'weight_signal_3', 'weight_signal_4']

    def vars_for_template(self):
        player = self.player
        task = player.participant.vars['extended_bonus_tasks'][player.round_number - 1]

        # Store signals in player model
        player.signal_1 = task.get('signal_1')
        player.signal_2 = task.get('signal_2')
        player.signal_3 = task.get('signal_3')
        player.signal_4 = task.get('signal_4')

        player.display_signal_1 = task.get('display_signal_1')
        player.display_signal_2 = task.get('display_signal_2')
        player.display_signal_3 = task.get('display_signal_3')
        player.players_signal_position = task.get('players_signal_position')
        player.bonus_recipient = task.get('bonus_recipient')
        player.recipient_type = task.get('recipient_type')

        positions = task.get('member_positions', {})  # e.g., {'You': 2, 'Member 2': 1, 'Member 3': 3}
        owner_types = task.get('owner_types', {})

        # Reverse mapping to position -> role
        position_to_member = {pos: member for member, pos in positions.items()}

        member_labels = []
        member_types = []
        member_signals = []
        weight_fields = ['weight_signal_1', 'weight_signal_2', 'weight_signal_3']

        signal_lookup = {
            1: player.signal_1,
            2: player.signal_2,
            3: player.signal_3,
        }

        # Reconstruct ordered member data
        for pos in range(1, 4):
            member = position_to_member[pos]
            label = f"Member {pos}"
            if member == 'You':
                label += " (me)"
            member_labels.append(label)
            member_types.append(owner_types.get(member, ''))
            display_signal_pos = task.get(f'display_signal_{pos}')
            member_signals.append(signal_lookup.get(display_signal_pos))

        # Determine bonus recipient's label and type based on their display position
        bonus_recipient_label = ''
        bonus_recipient_type = ''
        for pos in range(1, 4):
            member = position_to_member[pos]
            if member == player.bonus_recipient:
                bonus_recipient_label = f"Member {pos}"
                bonus_recipient_type = owner_types.get(member, '')

        return {
            'members': list(zip(member_labels, member_types, member_signals, weight_fields)),
            'mean_asset_value': C.MEAN_ASSET_VALUE,
            'recipient_type': player.recipient_type,
            'bonus_recipient': player.bonus_recipient,
            'bonus_recipient_label': bonus_recipient_label,
            'bonus_recipient_type': bonus_recipient_type,
        }

    # def vars_for_template(self):
    #     player = self.player
    #     print(f"BonusTaskStage02 for player {player.id_in_subsession}, round {player.round_number}")

    #     if 'extended_bonus_tasks' not in player.participant.vars:
    #         print("ERROR: extended_bonus_tasks not found in participant vars")
    #         print(f"Available vars: {list(player.participant.vars.keys())}")
    #         return {}

    #     if player.round_number > len(player.participant.vars['extended_bonus_tasks']):
    #         print(f"ERROR: round_number ({player.round_number}) exceeds available tasks")
    #         return {}

    #     task = player.participant.vars['extended_bonus_tasks'][player.round_number - 1]

    #     # Store signals in player model
    #     player.signal_1 = task.get('signal_1')
    #     player.signal_2 = task.get('signal_2')
    #     player.signal_3 = task.get('signal_3')
    #     player.signal_4 = task.get('signal_4')

    #     player.display_signal_1 = task.get('display_signal_1')
    #     player.display_signal_2 = task.get('display_signal_2')
    #     player.display_signal_3 = task.get('display_signal_3')
    #     player.players_signal_position = task.get('players_signal_position')
    #     player.bonus_recipient = task.get('bonus_recipient')
    #     player.recipient_type = task.get('recipient_type')

    #     positions = task.get('member_positions', {})
    #     owner_types = task.get('owner_types', {})

    #     member_signals = [task.get(f'display_signal_{i}') for i in range(1, 4)]
    #     weight_fields = ['weight_signal_1', 'weight_signal_2', 'weight_signal_3']

    #     member_labels = [''] * 3
    #     member_types = [''] * 3

    #     for member, pos in positions.items():
    #         label = member + ' (me)' if member == 'Member 1' else member
    #         member_labels[pos - 1] = label
    #         member_types[pos - 1] = owner_types.get(member, '')

    #     return {
    #         'member_labels': member_labels,
    #         'member_types': member_types,
    #         'member_signals': member_signals,
    #         'mean_asset_value': C.MEAN_ASSET_VALUE,
    #         'weight_fields': weight_fields,
    #         'recipient_type': player.recipient_type
    #     }

    def error_message(self, values):
        total = sum(values.get(f'weight_signal_{i}', 0) for i in range(1, 5))
        if total != 100.0:
            return 'The allocation of tokens to information must add up to 100.'


class ResultsStage02(Page):
    def vars_for_template(self):
        player = self.player
        task = player.participant.vars['extended_bonus_tasks'][player.round_number - 1]

        positions = task.get('member_positions', {})
        owner_types = task.get('owner_types', {})

        position_to_member = {pos: member for member, pos in positions.items()}

        member_labels = []
        member_types = []
        member_signals = []

        signal_lookup = {
            1: player.signal_1,
            2: player.signal_2,
            3: player.signal_3,
        }

        for pos in range(1, 4):
            member = position_to_member[pos]
            label = f"Member {pos}"
            if member == 'You':
                label += " (me)"
            member_labels.append(label)
            member_types.append(owner_types.get(member, ''))
            display_signal_pos = task.get(f'display_signal_{pos}')
            member_signals.append(signal_lookup.get(display_signal_pos))

        weight_values = [
            player.weight_signal_1,
            player.weight_signal_2,
            player.weight_signal_3,
        ]

        # Determine bonus recipient's display label and type
        bonus_recipient_label = ''
        bonus_recipient_type = ''
        for pos in range(1, 4):
            member = position_to_member[pos]
            if member == player.bonus_recipient:
                bonus_recipient_label = f"Member {pos}"
                bonus_recipient_type = owner_types.get(member, '')

        return {
            'members': list(zip(member_labels, member_types, member_signals, weight_values)),
            'mean_asset_value': C.MEAN_ASSET_VALUE,
            'weight_signal_4': player.weight_signal_4,
            'recipient_type': player.recipient_type,
            'bonus_recipient': player.bonus_recipient,
            'bonus_recipient_label': bonus_recipient_label,
            'bonus_recipient_type': bonus_recipient_type,
        }

        # return {
        #     'member_labels': member_labels,
        #     'member_types': member_types,
        #     'member_signals': [
        #         player.display_signal_1,
        #         player.display_signal_2,
        #         player.display_signal_3,
        #     ],
        #     'mean_asset_value': C.MEAN_ASSET_VALUE,
        #     'weight_signal_1': player.weight_signal_1,
        #     'weight_signal_2': player.weight_signal_2,
        #     'weight_signal_3': player.weight_signal_3,
        #     'weight_signal_4': player.weight_signal_4,
        #     'recipient_type': player.recipient_type,
        # }


page_sequence = [
    InstructionsStage02,
    BonusTaskStage02,
    ResultsStage02
]
