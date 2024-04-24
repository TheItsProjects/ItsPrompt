from ItsPrompt.prompt import Prompt


# standard input validation
def input_not_empty(input: str) -> str | None:
    if len(input) == 0:
        return 'Input field can not be empty!'

    return None


# input
Prompt.input(
    'Please type your address',
    validate=input_not_empty,
    completions=['Mainstreet 4', 'Fifth way'],
    completion_show_multicolumn=True,
)
