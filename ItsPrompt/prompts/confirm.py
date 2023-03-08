from prompt_toolkit import HTML, Application
from prompt_toolkit.layout.containers import Window
from prompt_toolkit.layout.controls import FormattedTextControl


class ConfirmPrompt(Application):

    def __init__(
        self,
        question: str,
        default: bool | None = None,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)

        # get prompt content box
        self.prompt_content: FormattedTextControl = self.layout.container.get_children(
        )[0].content  # type: ignore

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

        # save default selection
        self.default = default

    def update(self):
        '''update prompt content'''
        content = f'[<question_mark>?</question_mark>] <question>{self.question}</question>: <text>({"Y" if self.default==True else "y"}/{"N" if self.default==False else "n"})</text>'

        self.prompt_content.text = HTML(content)

        # show error, if error should be shown, else show normal prompt
        if not self.is_error:
            # show normal prompt, change style to standard toolbar
            self.toolbar_content.text = self.toolbar_content_default_text
            self.toolbar_window.style = 'class:tooltip'
        else:
            # show error prompt and error style
            # the only error that might occur is that not enough options are selected
            self.toolbar_content.text = f'ERROR: a selection must be made!'
            self.toolbar_window.style = 'class:error'

    def prompt(self) -> bool | None:
        '''start the application, returns the return value'''
        self.update()
        out: bool | None = self.run()

        return out

    def on_key(self, key_sequence: list[str]):
        '''when Y or N is pressed, select value and submit'''
        key = key_sequence[0]

        # return if key is not an available key
        if not key in ['y', 'n']:
            return

        # exit with answer
        self.exit(result=key == 'y')

    def on_enter(self):
        # if no default is present, user is not able to just submit
        if self.default is None:
            self.is_error = True
            self.update()
            return

        self.exit(result=self.default)
