from dataclasses import dataclass


@dataclass
class SelectOption:
    name: str
    id: str
    is_disabled: bool


def process_data(options: tuple[str | tuple[str, str], ...]) -> list[SelectOption]:
    """
    Processes the given `options` and returns the processed list

    :param options: A list of options to process
    :type options: tuple[str | tuple[str, str], ...]
    :raises TypeError: If an option is not processable, a `TypeError` will be raised
    :return: a list of `SelectOptions`
    :rtype: list[SelectOption]
    """
    processed_options: list[SelectOption] = []

    # process given options
    for option in options:
        if type(option) is str:
            processed_options.append(SelectOption(name=option, id=option, is_disabled=False))
        elif type(option) is tuple:
            processed_options.append(SelectOption(name=option[0], id=option[1], is_disabled=False))
        else:
            raise TypeError('Argument is not processable')

    return processed_options
