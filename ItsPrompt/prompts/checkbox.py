from prompt_toolkit import Application, HTML
from prompt_toolkit.layout.containers import Window
from prompt_toolkit.layout.controls import FormattedTextControl

from ..data.checkbox import process_data
from ..objects.prompts.separator import Separator
from ..objects.prompts.type import OptionsList


class CheckboxPrompt(Application):
    CHECKED_SIGN = '\u25cf'
    UNCHECKED_SIGN = '\u25cb'

    def __init__(
        self,
        question: str,
        options: OptionsList,
        pointer_at: int | None = None,
        default_checked: tuple[str, ...] | None = None,
        disabled: tuple[str, ...] | None = None,
        min_selections: int = 0,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)

        # get prompt content box
        self.prompt_content: FormattedTextControl = self.layout.container.get_children()[0].content  # type: ignore

        # save toolbar window and box (for showing errors)
        self.toolbar_window: Window = self.layout.container.get_children()[1]  # type: ignore
        self.toolbar_content: FormattedTextControl = self.layout.container.get_children()[1].content  # type: ignore

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
                raise ValueError('At least one of the given default_checked values is invalid.')

        # disable options (or none if not given)
        if disabled is not None:
            was_set = 0  # Keeping track of options which where disabled.
            # If was_set is not as big as len(disabled),
            # then we know that there was an invalid option which could not be disabled,
            # so we raise an error.
            for option in self.options:
                if option.id in disabled:
                    option.is_disabled = True
                    was_set += 1

            if was_set != len(disabled):
                raise ValueError("At least one of the given disabled values is invalid.")

        # set pointer selection
        self.selection = pointer_at if pointer_at else 0

        # if the current selection is disabled, we will skip it
        while self.options[self.selection].is_disabled:
            self.selection = (self.selection + 1) % len(self.options)

    def update(self):
        """update prompt content"""
        content = f'[<question_mark>?</question_mark>] <question>{self.question}</question>:'

        for i, option in self.options.with_separators_enumerate():

            if type(option) is Separator:
                content += f"\n<separator>{option.label}</separator>"
                continue

            disabled = ("<disabled>", "</disabled>") if option.is_disabled else ("", "")  # type: ignore
            # Disabled tags will only be inserted if the option is disabled,
            # otherwise there will only be an empty string inserted.
            selected = self.__class__.CHECKED_SIGN if option.is_selected else self.__class__.UNCHECKED_SIGN  # type: ignore

            if i == self.selection:
                content += f"\n{disabled[0]}<selected_option>  > {selected} {option.name}</selected_option>{disabled[1]}"  # type: ignore
            else:
                content += f"\n{disabled[0]}<option>    {selected} {option.name} </option>{disabled[1]}"  # type: ignore

        self.prompt_content.text = HTML(content)

        # show error, if error should be shown, else show normal prompt
        if not self.is_error:
            # show normal prompt, change style to standard toolbar
            self.toolbar_content.text = self.toolbar_content_default_text
            self.toolbar_window.style = 'class:tooltip'
        else:  # pragma: no cover
            # show error prompt and error style
            # the only error that might occur is that not enough options are selected
            self.toolbar_content.text = f'ERROR: a minimum of {self.min_selections} options need to be ' \
                                        f'selected!'
            self.toolbar_window.style = 'class:error'

    def prompt(self) -> list[str] | None:
        """start the application, returns the return value"""
        self.update()
        out: list[str] | None = self.run()

        return out

    def on_up(self):
        """when up is pressed, the previous indexed option will be selected"""
        self.selection = (self.selection - 1) % len(self.options)

        # if the current selection is disabled, we will skip it
        while self.options[self.selection].is_disabled:
            self.selection = (self.selection - 1) % len(self.options)

        # reset error
        self.is_error = False

        self.update()

    def on_down(self):
        """when down is pressed, the next indexed option will be selected"""
        self.selection = (self.selection + 1) % len(self.options)

        # if the current selection is disabled, we will skip it
        while self.options[self.selection].is_disabled:
            self.selection = (self.selection + 1) % len(self.options)

        # reset error
        self.is_error = False

        self.update()

    def on_space(self):
        """when space is pressed, select or deselect current selection"""
        self.options[self.selection].is_selected = not self.options[self.selection].is_selected

        # reset error
        self.is_error = False

        self.update()

    def on_enter(self):
        # get selected options
        selected_options: list[str] = []

        for option in self.options:
            if option.is_selected:
                selected_options.append(option.id)

        # make sure that enough options are selected
        if len(selected_options) < self.min_selections:  # pragma: no cover
            # show error
            self.is_error = True
            self.update()
            return

        self.exit(result=selected_options)
