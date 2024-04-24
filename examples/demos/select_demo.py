from ItsPrompt.objects.prompts.separator import Separator
from ItsPrompt.prompt import Prompt

Prompt.select(
    'What food would you like?',
    (Separator('The veggies'), 'Salad', Separator('The meaties'), 'Pizza', 'Burger'),
    default='Pizza',
)
