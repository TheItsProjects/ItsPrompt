from ItsPrompt.prompt import Prompt

# checkbox
Prompt.checkbox(
    'What beverages would you like?',
    ('Coke', 'Water', 'Juice'),
    default_checked=('Water',),
    disabled=("Coke",),
    min_selections=1,
)
