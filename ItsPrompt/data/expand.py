from dataclasses import dataclass


@dataclass
class ExpandOption:
    key: str
    name: str
    id: str


def process_data(
        options: tuple[str | tuple[str, str, str], ...]) -> list[ExpandOption]:
    '''
    Processes the given `options` and returns the processed list

    :param options: A list of options to process
    :type options: tuple[str  |  tuple[str, str, str], ...]
    :raises ValueError: If the keys are not unique
    :raises ValueError: If the keys are not of length 1
    :raises ValueError: If the keys are not ascii
    :raises ValueError: If the keys are using h
    :raises TypeError: If an option is not processable
    :return: A list of `ExpandOptions`
    :rtype: list[ExpandOption]
    '''
    # check if every key is unique, otherwise return error
    if any([options.count(option[0]) > 1 for option in options]):
        raise ValueError('Keys must be unique!')

    # check that every key string is only one char long
    if any([len(option[0]) > 1 or len(option[0]) < 1 for option in options]):
        raise ValueError('Keys must be of length 1!')

    # check that every key is ascii
    if any([not option[0].isascii() for option in options]):
        raise ValueError('Keys must be ascii!')

    # check if h is not assigned
    if any([option[0] == 'h' for option in options]):
        raise ValueError('The h-key is not assignable!')

    processed_options: list[ExpandOption] = []

    # process given options
    for option in options:
        if type(option) is str:
            # use first letter as key, and str as name and id
            processed_options.append(
                ExpandOption(
                    key=option[0],
                    name=option,
                    id=option,
                ))
        elif type(option) is tuple:
            processed_options.append(
                ExpandOption(
                    key=option[0],
                    name=option[1],
                    id=option[2],
                ))
        else:
            raise TypeError('Argument is not processable')

    # append a help option
    processed_options.append(
        ExpandOption(
            key='h',
            name='Help Menu, list or hide all options',
            id='',
        ))

    return processed_options
