from dataclasses import dataclass


@dataclass
class CheckboxOption:
    name: str
    id: str
    is_selected: bool


def process_data(
        options: tuple[str | tuple[str, str], ...]) -> list[CheckboxOption]:
    '''
    Processes the given `options` and returns the processed list

    :param options: A list of options to process
    :type options: tuple[str  |  tuple[str, str], ...]
    :raises TypeError: If an option is not processable, a `TypeError` will be raised
    :return: a list of `CheckboxOption`
    :rtype: list[CheckboxOption]
    '''
    processed_options: list[CheckboxOption] = []

    # process given options
    for option in options:
        if type(option) is str:
            processed_options.append(
                CheckboxOption(
                    name=option,
                    id=option,
                    is_selected=False,
                ))
        elif type(option) is tuple:
            processed_options.append(
                CheckboxOption(
                    name=option[0],
                    id=option[1],
                    is_selected=False,
                ))
        else:
            raise TypeError('Argument is not processable')

    return processed_options
