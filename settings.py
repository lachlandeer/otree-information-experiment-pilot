from os import environ
SESSION_CONFIG_DEFAULTS = dict(real_world_currency_per_point=0.005, participation_fee=0)
SESSION_CONFIGS = [dict(name='my_session', 
                        num_demo_participants=3, 
                        app_sequence=[
                         'Introduction', 
                         'asset_indiv_no_game', 
                         'GroupPreferenceElicitation', 
                         #'asset_live_game', 
                         #'bonus', 
                         'CollectivismSurvey', 
                         'DemographicsSurvey',
                         'RandomPaymentResults'
                         ]
                       )
                  ]
LANGUAGE_CODE = 'en'
REAL_WORLD_CURRENCY_CODE = 'GBP'
USE_POINTS = True
DEMO_PAGE_INTRO_HTML = ''
PARTICIPANT_FIELDS = ['selected_app', 'selected_round', 'random_payment', 'group_results', 'condition', 
                      'task_1', 'task_2', 'task_3', 'task_4', 'task_5', 'task_6', 'task_7', 'task_8', 'task_9', 'task_10', 
                      'task_11', 'task_12', 'task_13', 'task_14', 'task_15', 'task_16', 'task_17', 'task_18', 'task_19', 'task_20',
                      'bonus_tasks']
SESSION_FIELDS = []
ROOMS = []

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

SECRET_KEY = 'blahblah'

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ['otree']


