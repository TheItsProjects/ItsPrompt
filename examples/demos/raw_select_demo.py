from ItsPrompt.prompt import Prompt

# raw_select
Prompt.raw_select(
    'What pizza would you like?',
    ('Salami', 'Hawaii', 'four-cheese'),
    allow_keyboard=True,
)
