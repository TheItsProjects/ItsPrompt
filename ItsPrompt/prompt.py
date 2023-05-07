'''
# ItsPrompt

created by ItsNameless

:copyright: (c) 2023-present ItsNameless
:license: MIT, see LICENSE for more details.
'''

from typing import Callable

from pandas import DataFrame
from prompt_toolkit import HTML
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.completion import Completer
from prompt_toolkit.layout.containers import (Float, FloatContainer, HSplit,
                                              VSplit, Window)
from prompt_toolkit.layout.controls import BufferControl, FormattedTextControl
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.layout.menus import (CompletionsMenu,
                                         MultiColumnCompletionsMenu)

from .data.style import PromptStyle, convert_style, default_style
from .data.type import CompletionDict
from .keyboard_handler import generate_key_bindings
from .prompts.checkbox import CheckboxPrompt
from .prompts.confirm import ConfirmPrompt
from .prompts.expand import ExpandPrompt
from .prompts.input import InputPrompt
from .prompts.raw_select import RawSelectPrompt
from .prompts.select import SelectPrompt
from .prompts.table import TablePrompt


class Prompt:
    '''
    # Modern python prompter
    
    This tool is used to ask the user questions, the fancy way.
    
    Usage:
    ```
    answer = Prompt.checkbox('option 1', 'option 2')
    ```
    '''

    @classmethod
    def select(
        cls,
        question: str,
        options: tuple[str | tuple[str, str], ...],
        default: str | None = None,
        style: PromptStyle | None = None,
    ) -> str:
        '''
        Ask the user for selecting ONE of the given `options`.

        This method shows the question alongside the `options` as a nice list. The user has the ability to use the up, down and enter keys to navigate between the options and select the one thats right.

        The `options` are either a string, which is used as the display value and the id, or a tuple[str, str], where the first string is the display value and the second is the option's id.

        :param question: The question to display
        :type question: str
        :param options: A list of possible options
        :type options: tuple[str  |  tuple[str, str], ...]
        :param default: The id of the default option to select (empty or None if the first should be default), defaults to None
        :type default: str | None, optional
        :param style: A separate style to style the prompt (empty or None for default style), defaults to None
        :type style: PromptStyle | None, optional
        :raises KeyboardInterrupt: When the user presses ctrl-c, `KeyboardInterrupt` will be raised
        :return: The id of the selected option
        :rtype: str
        '''
        app = SelectPrompt(
            question,
            options,
            default,
            layout=Layout(
                HSplit([
                    Window(FormattedTextControl(), always_hide_cursor=True),
                    Window(FormattedTextControl(
                        HTML('Use UP, DOWN to select, ENTER to submit')),
                           char=' ',
                           style='class:tooltip',
                           height=1)
                ])),
            key_bindings=generate_key_bindings(SelectPrompt),
            erase_when_done=True,
            style=convert_style(style)
            if style else convert_style(default_style),
        )
        ans = app.prompt()
        if ans == None:
            raise KeyboardInterrupt()
        return ans

    @classmethod
    def raw_select(
        cls,
        question: str,
        options: tuple[str | tuple[str, str], ...],
        default: str | None = None,
        allow_keyboard: bool = False,
        style: PromptStyle | None = None,
    ) -> str:
        '''
        Ask the user for selection ONE of the given `options`.

        This method shows the question alongside the `options` as a nice list. The user needs to type the index of the answer. If `allow_keyboard` is given, the user may use the keyboard as in the `select()` method.

        The `options` are either a string, which is used as the display value and the id, or a tuple[str, str], where the first string is the display value and the second is the option's id.

        :param question: The question to display
        :type question: str
        :param options: A list of possible options
        :type options: tuple[str  |  tuple[str, str], ...]
        :param default: The id of the default option to select (empty or None if the first should be default), defaults to None
        :type default: str | None, optional
        :param allow_keyboard: Whether the user should be able to select the answer with up and down, defaults to False
        :type allow_keyboard: bool, optional
        :param style: A separate style to style the prompt (empty or None for default style), defaults to None
        :type style: PromptStyle | None, optional
        :raises KeyboardInterrupt: When the user presses ctrl-c, `KeyboardInterrupt` will be raised
        :return: The id of the selected option
        :rtype: str
        '''
        app = RawSelectPrompt(
            question,
            options,
            default,
            allow_keyboard,
            layout=Layout(
                HSplit([
                    Window(FormattedTextControl(), always_hide_cursor=True),
                    Window(FormattedTextControl(
                        HTML(
                            'Type the INDEX of your selection, ENTER to submit'
                        )),
                           char=' ',
                           style='class:tooltip',
                           height=1)
                ])),
            key_bindings=generate_key_bindings(RawSelectPrompt),
            erase_when_done=True,
            style=convert_style(style)
            if style else convert_style(default_style),
        )
        ans = app.prompt()
        if ans == None:
            raise KeyboardInterrupt()
        return ans

    @classmethod
    def expand(
        cls,
        question: str,
        options: tuple[str | tuple[str, str, str], ...],
        default: str | None = None,
        allow_keyboard: bool = False,
        style: PromptStyle | None = None,
    ) -> str:
        '''
        Ask the user for selecting ONE of the given `options`.

        The user needs to type the key of the option. If the user types `h`, all options will be shown.

        The `options` are either a string, where `s[0]` will be the key to select and the string will be used as name and id, or a tuple[str, str, str] where `t[0]` will be the key, `t[1]` the name and `t[2]` the id of the option.

        Every key must be a unique ascii character and of length 1, and there may not be a key assigned to `h`.

        :param question: The question to display
        :type question: str
        :param options: A list of possible options
        :type options: tuple[str  |  tuple[str, str, str], ...]
        :param default: The id of the default option to select (empty or None if `h` should be default), defaults to None
        :type default: str | None, optional
        :param allow_keyboard: Whether the user should be able to select the answer with up and down, defaults to False
        :type allow_keyboard: bool, optional
        :param style: A separate style to style the prompt (empty or None for default style), defaults to None
        :type style: PromptStyle | None, optional
        :raises KeyboardInterrupt: When the user presses ctrl-c, `KeyboardInterrupt` will be raised
        :return: The id of the selected option
        :rtype: str
        '''
        app = ExpandPrompt(
            question,
            options,
            default,
            allow_keyboard,
            layout=Layout(
                HSplit([
                    Window(FormattedTextControl(), always_hide_cursor=True),
                    Window(FormattedTextControl(
                        HTML(
                            'Type the KEY for your selection, ENTER to submit (use h to show all options)'
                        )),
                           char=' ',
                           style='class:tooltip',
                           height=1)
                ])),
            key_bindings=generate_key_bindings(ExpandPrompt),
            erase_when_done=True,
            style=convert_style(style)
            if style else convert_style(default_style),
        )
        ans = app.prompt()
        if ans == None:
            raise KeyboardInterrupt()
        return ans

    @classmethod
    def checkbox(
        cls,
        question: str,
        options: tuple[str | tuple[str, str], ...],
        pointer_at: int
        | None = None,
        default_checked: tuple[str, ...] | None = None,
        min_selections: int = 0,
        style: PromptStyle | None = None,
    ) -> list[str]:
        '''
        Ask the user for selecting MULTIPLE of the given `options`.

        The `options` will be shown as a nice list. The user may navigate with up and down, select or deselect with space and submit with enter.

        The `options` are either a string, which is used as the display value and the id, or a tuple[str, str], where the first string is the display value and the second is the option's id.

        :param question: The question to display
        :type question: str
        :param options: A list of possible options
        :type options: tuple[str  |  tuple[str, str], ...]
        :param pointer_at: A 0-indexed value, where the pointer should start (0 if None), defaults to None
        :type pointer_at: int | None, optional
        :param default_checked: A list of ids, which should be checked by default (empty if None)
        :type default_checked: tuple[str, ...] | None, optional
        :param min_selections: A minimum amount of options that need to be checked before submitting (prohibits the user of submitting, if not enough are checked; 0 if None)
        :type min_selections: int, optional
        :param style: A separate style to style the prompt (empty or None for default style), defaults to None
        :type style: PromptStyle | None, optional
        :raises KeyboardInterrupt: When the user presses ctrl-c, `KeyboardInterrupt` will be raised
        :return: The ids of the selected options
        :rtype: list[str]
        '''
        app = CheckboxPrompt(
            question,
            options,
            pointer_at,
            default_checked,
            min_selections,
            layout=Layout(
                HSplit([
                    Window(FormattedTextControl(), always_hide_cursor=True),
                    Window(FormattedTextControl(
                        HTML(
                            'Use UP, DOWN to change selection, SPACE to select, ENTER to submit'
                        )),
                           char=' ',
                           style='class:tooltip',
                           height=1)
                ])),
            key_bindings=generate_key_bindings(CheckboxPrompt),
            erase_when_done=True,
            style=convert_style(style)
            if style else convert_style(default_style),
        )
        ans = app.prompt()
        if ans == None:
            raise KeyboardInterrupt()
        return ans

    @classmethod
    def confirm(
        cls,
        question: str,
        default: bool | None = None,
        style: PromptStyle | None = None,
    ) -> bool:
        '''
        Ask the user for confirming or denying your prompt.

        The user needs to type "y", "n" or enter (only if default is given).

        If `default` is `True`, the prompt will be in the style of (Y/n).

        If `default` is `False`, the prompt will be in the style of (n/Y).

        If `default` is `None` (or not given), the prompt will be in the style of (y/n). In this case, the user may not use enter to submit the default, as there is no default given.

        :param question: The question to display
        :type question: str
        :param default: The default answer to select when pressing enter, defaults to None
        :type default: bool | None, optional
        :param style: A separate style to style the prompt (empty or None for default style), defaults to None
        :type style: PromptStyle | None, optional
        :raises KeyboardInterrupt: When the user presses ctrl-c, `KeyboardInterrupt` will be raised
        :return: Whether the user selected "y" or "n"
        :rtype: bool
        '''
        app = ConfirmPrompt(
            question,
            default,
            layout=Layout(
                HSplit([
                    Window(FormattedTextControl(), always_hide_cursor=True),
                    Window(FormattedTextControl(
                        HTML(
                            'Press Y or N, ENTER if default value is available'
                        )),
                           char=' ',
                           style='class:tooltip',
                           height=1)
                ])),
            key_bindings=generate_key_bindings(ConfirmPrompt),
            erase_when_done=True,
            style=convert_style(style)
            if style else convert_style(default_style),
        )

        ans = app.prompt()
        if ans == None:
            raise KeyboardInterrupt()
        return ans

    @classmethod
    def input(
        cls,
        question: str,
        default: str | None = None,
        multiline: bool = False,
        show_symbol: str | None = None,
        validate: Callable[[str], str | None] | None = None,
        completions: list[str] | CompletionDict | None = None,
        completer: Completer | None = None,
        completion_show_multicolumn: bool = False,
        style: PromptStyle | None = None,
    ) -> str:
        '''
        Ask the user for typing an input.

        If default is given, it will be returned if enter was pressed and no input was given by the user. If the user writes an input, the default will be overwritten.

        If multiline is activated, enter will not submit, but rather create a newline. Use `alt+enter` to submit.

        If show_symbol is given, all chars (except newlines) will be replaced with this character in the interface. The result will still be the input the user typed, it just will not appear in the CLI.

        Validate takes a function which receives a `str` (the current input of the user) and may return None or a `str`. If the function returns None, the prompt may assume that the input is valid. If it returns a `str`, this will be the error shown to the user. The user will not be able to submit the input, if validate returns an error.

        Completions may be a list of possible completion strings or a nested dictionary where the key is a completion string and the value is a new dict in the same style (more in the README.md).

        You can use your own Completer as well (more in the README.md).

        THESE VALUES ARE MUTUALLY EXCLUSIVE. You may not use both. If you use a completer, you can not use show_symbol!

        :param question: The question to display
        :type question: str
        :param default: The default value to fill in, defaults to None
        :type default: str | None, optional
        :param multiline: Whether to allow the user to type multiple lines, defaults to False
        :type multiline: bool, optional
        :param show_symbol: A symbol to show instead of the users input, defaults to None
        :type show_symbol: str | None, optional
        :param validate: A function to check the users input in real-time, defaults to None
        :type validate: Callable[[str], str | None] | None, optional
        :param completions: The completions to use, defaults to None
        :type completions: list[str] | CompletionDict | None, optional
        :param completer: A completer to use, defaults to None
        :type completer: Completer | None, optional
        :param completion_show_multicolumn: Whether to show the completions as a scrollable list or as multiple columns, defaults to False
        :type completion_show_multicolumn: bool, optional
        :param style: A separate style to style the prompt (empty or None for default style), defaults to None
        :type style: PromptStyle | None, optional
        :raises KeyboardInterrupt: When the user presses ctrl-c, `KeyboardInterrupt` will be raised
        :return: The input of the user
        :rtype: str
        '''

        # extracting the body, so we can display a floating auto completion field
        body = HSplit([
            VSplit([
                Window(
                    FormattedTextControl(),
                    always_hide_cursor=True,
                    dont_extend_width=True,
                ),
                Window(
                    BufferControl(Buffer(complete_while_typing=True))
                ),  # the completer will be passed in the Application class
            ]),
            Window(
                FormattedTextControl(
                    HTML(
                        f'Type your answer, {"ALT+ENTER" if multiline else "ENTER"} to submit'
                    )),
                char=' ',
                style='class:tooltip',
                height=1,
            )
        ])

        app = InputPrompt(
            question,
            default,
            multiline,
            show_symbol,
            validate,
            completions,
            completer,
            layout=Layout(
                FloatContainer(
                    content=body,
                    floats=[
                        Float(
                            MultiColumnCompletionsMenu(show_meta=False) if
                            completion_show_multicolumn else CompletionsMenu(),
                            xcursor=True,
                            ycursor=True,
                        )
                    ])),
            key_bindings=generate_key_bindings(InputPrompt),
            erase_when_done=True,
            style=convert_style(style)
            if style else convert_style(default_style),
        )

        ans = app.prompt()
        if ans == None:
            raise KeyboardInterrupt()
        return ans

    @classmethod
    def table(
        cls,
        question: str,
        data: DataFrame,
        style: PromptStyle | None = None,
    ) -> DataFrame:
        '''
        Ask the user for filling out the displayed table.

        This method shows the question alongside a table, which the user may navigate with the arrow keys. The user has the ability to use the up, down and enter keys to navigate between the options and change the text in each cell.

        The `data` is a pandas DataFrame, where the values will be input in the cells by default.

        # TODO
        :param question: The question to display
        :type question: str
        :param options: A list of possible options
        :type options: tuple[str  |  tuple[str, str], ...]
        :param default: The id of the default option to select (empty or None if the first should be default), defaults to None
        :type default: str | None, optional
        :param style: A separate style to style the prompt (empty or None for default style), defaults to None
        :type style: PromptStyle | None, optional
        :raises KeyboardInterrupt: When the user presses ctrl-c, `KeyboardInterrupt` will be raised
        :return: The id of the selected option
        :rtype: str
        '''
        app = TablePrompt(
            question,
            data,
            layout=Layout(
                HSplit([
                    Window(FormattedTextControl()),
                    Window(FormattedTextControl(
                        HTML('Use UP, DOWN, LEFT, RIGHT to select a cell, TYPE to add char, BACKSPACE to delete char, ENTER to submit')),
                           char=' ',
                           style='class:tooltip',
                           height=1)
                ])),
            key_bindings=generate_key_bindings(TablePrompt),
            erase_when_done=True,
            style=convert_style(style)
            if style else convert_style(default_style),
        )
        ans = app.prompt()
        if type(ans) != DataFrame and ans == None:
            raise KeyboardInterrupt()
        return ans
