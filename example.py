# mypy: disable-error-code=assignment

try:
    from pandas import DataFrame

    NO_PANDAS = False
except ModuleNotFoundError:
    NO_PANDAS = True

from ItsPrompt.prompt import Prompt

# select
ans = Prompt.select(
    'What food would you like?',
    ('Pizza', 'Burger', 'Salad'),
    default='Pizza',
)
print(ans)

# raw_select
ans = Prompt.raw_select(
    'What pizza would you like?',
    ('Salami', 'Hawaii', 'four-cheese'),
    allow_keyboard=True,
)
print(ans)

# checkbox
ans = Prompt.checkbox(
    'What beverages would you like?',
    ('Coke', 'Water', 'Juice'),
    default_checked=('Water',),
    min_selections=1,
)
print(ans)

# expand
ans = Prompt.expand(
    'Where do you want your food to be delivered?',
    ('my home', 'another home'),
    allow_keyboard=True,
)
print(ans)

# standard input with simple lambda validation
ans = Prompt.input(
    'Please type your id',
    validate=lambda x: "test" in x,
)

print(ans)


# standard input with validation
def input_not_empty(input: str) -> str | None:
    if len(input) == 0:
        return 'Input field can not be empty!'

    return None


ans = Prompt.input(
    'Please type your name',
    validate=input_not_empty,
)

print(ans)

# standard input with validation and completion
ans = Prompt.input(
    'Please type your address',
    validate=input_not_empty,
    completions=['Mainstreet 4', 'Fifth way'],
    completion_show_multicolumn=True,
)
print(ans)

# standard input with password (show_symbol)
ans = Prompt.input(
    'Please type your password',
    show_symbol='*',
)

print(ans)

# confirm
ans = Prompt.confirm(
    'Is the information correct?',
    default=True,
)
print(ans)

# table
if not NO_PANDAS:
    data = DataFrame({
        'Food': ['Pizza', 'Burger', 'Salad'],
        'Qty': [1, 0, 0],
    })

    ans = Prompt.table(
        'Please fill in your quantity',
        data,
    )

    print(ans)

# styling

# examples for the different styling class components
Prompt.raw_select(question='question', options=(
    'option',
    'selected_option',
))

Prompt.input(
    question='question',
    default='grayout',
    validate=lambda x: 'error',
)

# change default style
from ItsPrompt.data.style import default_style

default_style.error = 'fg:ansired bg:ansiwhite'

# create your own style
from ItsPrompt.data.style import PromptStyle

my_style = PromptStyle(
    question_mark='fg:ansiblue',
    error='fg:ansired bg:ansiwhite',
)

# copy default style
from ItsPrompt.data.style import create_from_default

my_style = create_from_default()

my_style.error = 'fg:ansired bg:ansiwhite'
