from typing import Callable
from prompt_toolkit import HTML, Application
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.layout.containers import Window
from prompt_toolkit.buffer import Buffer

import string


class InputPrompt(Application):

    def __init__(
        self,
        question: str,
        default: str | None = None,
        multiline: bool = False,
        show_symbol: str | None = None,
        validate: Callable[[str], str | None] | None = None,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)

        # get prompt content box
        self.prompt_content: FormattedTextControl = self.layout.container.get_children(
        )[0].get_children()[0].content  # type: ignore

        # get input buffer
        self.buffer: Buffer = self.layout.container.get_children(
        )[0].get_children()[1].content.buffer  # type: ignore

        # save toolbar window and box (for showing errors)
        self.toolbar_window: Window = self.layout.container.get_children()[
            1]  # type: ignore
        self.toolbar_content: FormattedTextControl = self.layout.container.get_children(
        )[1].content  # type: ignore

        # save standard toolbar content
        self.toolbar_content_default_text = self.toolbar_content.text

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

        # when show_symbol is given, we "hack" the interface (hiding the buffer and adding a FormattedTextControl to only show the symbols)
        if self.show_symbol:
            self.layout.container.get_children()[0].get_children(
            )[1].width = 0  # type: ignore

            self.symbol_content = FormattedTextControl()

            self.layout.container.get_children()[0].get_children().append(
                Window(self.symbol_content))

        # save validator function
        self.validate = validate

    def update(self):
        '''update prompt content'''
        content = f'[<question_mark>?</question_mark>] <question>{self.question}</question>: '

        if self.default and self.buffer.text == '':
            content += f'<grayout>{self.default}</grayout>'

        self.prompt_content.text = HTML(content)

        # update symbol_content if symbols should be shown
        if self.show_symbol:
            replaced_content = ''
            for char in self.buffer.text:
                if char == '\n':
                    replaced_content += '\n'
                else:
                    replaced_content += self.show_symbol

            self.symbol_content.text = HTML(replaced_content)

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

    def prompt(self) -> str | None:
        '''start the application, returns the return value'''
        self.update()
        out: str | None = self.run()

        return out

    def on_up(self):
        '''if multiline, this manually moves the buffer cursor up'''
        if self.multiline:
            self.buffer.cursor_up()

        self.update()

    def on_down(self):
        '''if multiline, this manually moves the buffer cursor down'''
        if self.multiline:
            self.buffer.cursor_down()

        self.update()

    def on_space(self):
        '''manually append a space to input'''
        self.buffer.text += ' '
        self.buffer.cursor_right()

        self.update()

    def on_key(self, key_sequence: list[str]):
        '''append key to input'''
        key = key_sequence[0]

        # only append if key is printable, otherwise the key is not important
        if key.isprintable():
            self.buffer.text += key
            self.buffer.cursor_right()

        self.update()

    def on_backspace(self):
        '''remove last letter from input'''
        self.buffer.text = self.buffer.text[:-1:]

        self.update()

    def on_ctrl_backspace(self):
        '''remove last word from input'''
        for i in range(len(self.buffer.text) - 2, -1, -1):
            if self.buffer.text[i] in string.punctuation + string.whitespace:
                self.buffer.text = self.buffer.text[:i + 1:]
                break
        else:
            # break was not called, so there is only one word in input
            # this word will be removed
            self.buffer.text = ''

        self.update()

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
        if self.multiline:
            self.buffer.text += '\n'
            self.buffer.cursor_down()
            self.update()
            return

        self._submit()
