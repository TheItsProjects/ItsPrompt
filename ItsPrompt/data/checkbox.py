from dataclasses import dataclass

from ..objects.prompts.option import Option
from ..objects.prompts.options_with_separator import OptionsWithSeparator
from ..objects.prompts.separator import Separator
from ..objects.prompts.type import OptionsList


@dataclass
class CheckboxOption(Option):
    name: str
    id: str
    is_selected: bool
    is_disabled: bool


def process_data(options: OptionsList) -> OptionsWithSeparator[CheckboxOption | Separator]:
    """
    Processes the given `options` and returns the processed list

    :param options: A list of options to process
    :type options: tuple[str | OptionWithId | Separator, ...]
    :raises TypeError: If an option is not processable, a `TypeError` will be raised
    :return: a list of `CheckboxOption`
    :rtype: list[CheckboxOption]
    """
    processed_options: list[CheckboxOption | Separator] = []

    # process given options
    for option in options:
        if type(option) is str:
            processed_options.append(CheckboxOption(name=option, id=option, is_selected=False, is_disabled=False))
        elif type(option) is tuple:
            processed_options.append(CheckboxOption(name=option[0], id=option[1], is_selected=False, is_disabled=False))
        elif type(option) is Separator:
            processed_options.append(option)
        else:
            raise TypeError('Argument is not processable')

    return OptionsWithSeparator(*processed_options)
