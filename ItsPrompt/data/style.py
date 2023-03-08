import copy
from dataclasses import asdict, dataclass

from prompt_toolkit.styles import Style


@dataclass
class PromptStyle:
    '''
    The style object used for styling the prompts.
    
    Empty styles will not be styled, so they appear without any styling.
    '''
    question_mark: str = ''
    question: str = ''
    option: str = ''
    selected_option: str = ''
    tooltip: str = ''
    error: str = ''
    text: str = ''
    grayout: str = ''


default_style = PromptStyle(
    question_mark='fg:ansigreen',
    selected_option='fg:ansicyan',
    tooltip='fg:ansibrightblue bg:ansiwhite bold',
    error='fg:ansiwhite bg:ansired bold',
    grayout='fg:ansibrightblack',
)


def convert_style(style: PromptStyle) -> Style:
    '''
    Converts the given `PromptStyle` to a usable `Style` object.

    :param style: The style to convert
    :type style: PromptStyle
    :return: The converted `Style` object
    :rtype: Style
    '''
    return Style.from_dict(asdict(style))


def create_from_default() -> PromptStyle:
    '''
    Returns a copy of the default style, which can be edited without changing the default style.

    :return: A editable copy of the default style
    :rtype: PromptStyle
    '''
    return copy.deepcopy(default_style)
