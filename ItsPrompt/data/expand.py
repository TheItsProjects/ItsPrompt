from dataclasses import dataclass

from ..objects.prompts.option import Option
from ..objects.prompts.options_with_separator import OptionsWithSeparator
from ..objects.prompts.separator import Separator
from ..objects.prompts.type import OptionsList


@dataclass
class ExpandOption(Option):
    key: str
    name: str
    id: str
    is_disabled: bool


def process_data(options: OptionsList) -> OptionsWithSeparator[ExpandOption | Separator]:
    """
    Processes the given `options` and returns the processed list

    :param options: A list of options to process
    :type options: tuple[str | OptionWithId | Separator, ...]
    :raises ValueError: If the keys are not unique
    :raises ValueError: If the keys are not of length 1
    :raises ValueError: If the keys are not ascii
    :raises ValueError: If the keys are using h
    :raises TypeError: If an option is not processable
    :return: A list of `ExpandOptions`
    :rtype: list[ExpandOption]
    """
    # check if every key is unique, otherwise return error
    keys = [option[0] for option in options if type(option) is not Separator]  # type: ignore
    if len(set(keys)) < len(keys):
        raise ValueError('Keys must be unique!')

    # check that every key string is only one char long
    if any(
        [
            len(option[0]) > 1 or len(option[0]) < 1 for option in options if  # type: ignore
            type(option) is not Separator
        ]
    ):
        raise ValueError('Keys must be of length 1!')

    # check that every key is ascii
    if any([not option[0].isascii() for option in options if type(option) is not Separator]):  # type: ignore
        raise ValueError('Keys must be ascii!')

    # check if h is not assigned
    if any([option[0] == 'h' for option in options if type(option) is not Separator]):  # type: ignore
        raise ValueError('The h-key is not assignable!')

    processed_options: list[ExpandOption] = []

    # process given options
    for option in options:
        if type(option) is str:
            # use the first letter as the key, and str as name and id
            processed_options.append(ExpandOption(key=option[0], name=option, id=option, is_disabled=False))
        elif type(option) is tuple:
            processed_options.append(
                ExpandOption(key=option[0], name=option[1], id=option[2], is_disabled=False)  # type: ignore
            )
        elif type(option) is Separator:
            processed_options.append(option)  # type: ignore
        else:
            raise TypeError('Argument is not processable')

    # append a help option
    processed_options.append(
        ExpandOption(key='h', name='Help Menu, list or hide all options', id='', is_disabled=False)
    )

    return OptionsWithSeparator(*processed_options)
