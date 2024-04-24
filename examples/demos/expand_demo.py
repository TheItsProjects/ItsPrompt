from ItsPrompt.prompt import Prompt

# expand
Prompt.expand(
    'Where do you want your food to be delivered?',
    ('my home', 'another home'),
    allow_keyboard=True,
)
