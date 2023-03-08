from prompt_toolkit import HTML, Application
from prompt_toolkit.layout.containers import Window
from prompt_toolkit.layout.controls import FormattedTextControl

from ..data.checkbox import process_data


class CheckboxPrompt(Application):

    CHECKED_SIGN = '\u25cf'
    UNCHECKED_SIGN = '\u25cb'

    def __init__(
        self,
        question: str,
        options: tuple[str | tuple[str, str], ...],
        pointer_at: int | None = None,
        default_checked: tuple[str, ...] | None = None,
        min_selections: int = 0,
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

        # save min selections
        self.min_selections = min_selections

        # process options
        self.options = process_data(options)

        # set pointer selection
        self.selection = pointer_at if pointer_at else 0

        # default check default option (or none if not given)
        if default_checked is not None:
            was_set = 0  # Keeping track of options which where selected.
            # If was_set is not as big as len(default_checked),
            # then we know that there was an invalid option which could not be checked,
            # so we raise an error.
            for option in self.options:
                if option.id in default_checked:
                    option.is_selected = True
                    was_set += 1

            if was_set != len(default_checked):
                raise ValueError(
                    'At least one of the given default_checked values is invalid.'
                )

    def update(self):
        '''update prompt content'''
        content = f'[<question_mark>?</question_mark>] <question>{self.question}</question>:'

        for i, option in enumerate(self.options):
            if i == self.selection:
                content += f'\n<selected_option>  > {self.__class__.CHECKED_SIGN if option.is_selected else self.__class__.UNCHECKED_SIGN} {option.name}</selected_option>'
            else:
                content += f'\n<option>    {self.__class__.CHECKED_SIGN if option.is_selected else self.__class__.UNCHECKED_SIGN} {option.name}</option>'

        self.prompt_content.text = HTML(content)

        # show error, if error should be shown, else show normal prompt
        if not self.is_error:
            # show normal prompt, change style to standard toolbar
            self.toolbar_content.text = self.toolbar_content_default_text
            self.toolbar_window.style = 'class:tooltip'
        else:
            # show error prompt and error style
            # the only error that might occur is that not enough options are selected
            self.toolbar_content.text = f'ERROR: a minimum of {self.min_selections} options need to be selected!'
            self.toolbar_window.style = 'class:error'

    def prompt(self) -> list[str] | None:
        '''start the application, returns the return value'''
        self.update()
        out: list[str] | None = self.run()

        return out

    def on_up(self):
        '''when up is pressed, the previous indexed option will be selected'''
        self.selection = (self.selection - 1) % len(self.options)

        # reset error
        self.is_error = False

        self.update()

    def on_down(self):
        '''when down is pressed, the next indexed option will be selected'''
        self.selection = (self.selection + 1) % len(self.options)

        # reset error
        self.is_error = False

        self.update()

    def on_space(self):
        '''when space is pressed, select or deselect current selection'''
        self.options[self.selection].is_selected = not self.options[
            self.selection].is_selected

        # reset error
        self.is_error = False

        self.update()

    def on_enter(self):
        # get selected options
        selected_options: list[str] = []

        for option in self.options:
            if option.is_selected:
                selected_options.append(option.id)

        # make sure that enough are selected
        if len(selected_options) < self.min_selections:
            # show error
            self.is_error = True
            self.update()
            return

        self.exit(result=selected_options)
