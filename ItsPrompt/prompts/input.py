import string
from typing import Callable

from prompt_toolkit import HTML, Application
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.completion import (Completer, FuzzyCompleter,
                                       FuzzyWordCompleter, NestedCompleter)
from prompt_toolkit.layout.containers import Window
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.layout.processors import PasswordProcessor

from ..data.type import CompletionDict


class InputPrompt(Application):

    def __init__(
        self,
        question: str,
        default: str | None = None,
        multiline: bool = False,
        show_symbol: str | None = None,
        validate: Callable[[str], str | None] | None = None,
        completions: list[str] | CompletionDict | None = None,
        completer: Completer | None = None,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)

        # temp body variable for making object accessing clearer
        _body = self.layout.container.content.get_children()  # type: ignore
        _vsplit = _body[0].get_children()

        # get prompt content box
        self.prompt_content: FormattedTextControl = _vsplit[
            0].content  # type: ignore

        # get input buffer
        self.buffer: Buffer = _vsplit[1].content.buffer  # type: ignore

        # save toolbar window and box (for showing errors)
        self.toolbar_window: Window = _body[1]  # type: ignore
        self.toolbar_content: FormattedTextControl = self.toolbar_window.content  # type: ignore

        # save standard toolbar content
        self.toolbar_content_default_text = self.toolbar_content.text  # type: ignore

        # add updating function to buffer change event
        self.buffer.on_text_changed.add_handler(lambda _: self.update())

        # save whether error is currently shown
        self.is_error = False

        # save question
        self.question = question

        # save default input
        self.default = default

        # save whether multiline is enabled
        self.multiline = multiline

        # save show_symbol
        self.show_symbol = show_symbol

        # when show_symbol is given, use PasswordProcessor to show the symbol instead of the text
        if self.show_symbol:
            _vsplit[1].content.input_processors = [
                PasswordProcessor(self.show_symbol)
            ]

        # save validator function
        self.validate = validate

        # save the completer
        self.completer = None

        if completions and completer:
            raise ValueError(
                'completions and completer are mutually exclusive! Please use only one of them!'
            )

        if show_symbol and (completions or completer):
            # symbol and completer are mutually exclusive
            raise ValueError(
                'Completions are not compatible with show_symbol!')

        if completions:
            # a list or a dict of completions to use is given
            if type(completions) is list:
                # we use FuzzyWordCompleter
                self.completer = FuzzyWordCompleter(list(completions))
            elif type(completions) is dict:
                # we use FuzzyCompleter with NestedCompleter
                self.completer = FuzzyCompleter(
                    NestedCompleter.from_nested_dict(completions))

        elif completer:
            # a self-created completer is given
            self.completer = completer

        # assign the created completer to the buffer
        if self.completer:
            self.buffer.completer = self.completer

    def update(self):
        '''update prompt content'''
        content = f'[<question_mark>?</question_mark>] <question>{self.question}</question>: '

        if self.default and self.buffer.text == '':
            content += f'<grayout>{self.default}</grayout>'

        self.prompt_content.text = HTML(content)

        # run validation and show error, if validation gives error
        if not self.validate:
            return

        validation_result = self.validate(self.buffer.text)

        self.is_error = bool(validation_result)

        # show error, if error should be shown, else show normal prompt
        if not self.is_error:
            # show normal prompt, change style to standard toolbar
            self.toolbar_content.text = self.toolbar_content_default_text
            self.toolbar_window.style = 'class:tooltip'
        else:
            # show error prompt and error style
            self.toolbar_content.text = validation_result
            self.toolbar_window.style = 'class:error'

        # run completion
        # Since we take over control of the buffer and the keyboard, the completion
        # (and all of its commands) need to be run manually every time we press a key.
        # This does not in any way change the user experience,
        # as it does the exact same thing the standard completer does.
        if self.is_running:
            self.buffer.start_completion()

    def prompt(self) -> str | None:
        '''start the application, returns the return value'''
        self.update()
        out: str | None = self.run()

        return out

    def _submit(self):
        '''method for submitting result, as this is done by two functions'''
        # if an error is currently shown, prevent submit
        if self.is_error:
            return

        # return buffer if given, else default if given, else empty string
        if self.buffer.text != '':
            self.exit(result=self.buffer.text)
        elif self.default:
            self.exit(result=self.default)
        else:
            self.exit(result='')

    def on_alt_enter(self):
        '''if multiline is enabled, this will submit'''
        if self.multiline:
            self._submit()

    def on_enter(self):
        '''either submit key or in multiline, append new line'''
        # run completion
        if (self.is_running) and self.buffer.complete_state and (
                completion := self.buffer.complete_state.current_completion):
            self.buffer.apply_completion(completion)

        if self.multiline:
            self.buffer.text += '\n'
            self.buffer.cursor_down()
            self.update()
            return

        self._submit()
