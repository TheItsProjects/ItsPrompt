from pandas import DataFrame

from ItsPrompt.prompt import Prompt

# table
data = DataFrame({
    'Food': ['Pizza', 'Burger', 'Salad'],
    'Qty': [1, 0, 0],
})

Prompt.table(
    'Please fill in your quantity',
    data,
)
