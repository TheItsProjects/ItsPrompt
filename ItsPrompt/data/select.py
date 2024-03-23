from dataclasses import dataclass

from ItsPrompt.objects.prompts.option import Option
from ItsPrompt.objects.prompts.options_with_separator import OptionsWithSeparator
from ItsPrompt.objects.prompts.separator import Separator
from ItsPrompt.objects.prompts.type import OptionsList


@dataclass
class SelectOption(Option):
    name: str
    id: str
    is_disabled: bool


def process_data(options: OptionsList) -> OptionsWithSeparator[SelectOption | Separator]:
    """
    Processes the given `options` and returns the processed list

    :param options: A list of options to process
    :type options: tuple[str | OptionWithId | Separator, ...]
    :raises TypeError: If an option is not processable, a `TypeError` will be raised
    :return: a list of `SelectOptions`
    :rtype: list[SelectOption]
    """
    processed_options: list[SelectOption | Separator] = []

    # process given options
    for option in options:
        if type(option) is str:
            processed_options.append(SelectOption(name=option, id=option, is_disabled=False))
        elif type(option) is tuple:
            processed_options.append(SelectOption(name=option[0], id=option[1], is_disabled=False))
        elif type(option) is Separator:
            processed_options.append(option)
        else:
            raise TypeError('Argument is not processable')

    return OptionsWithSeparator(*processed_options)
