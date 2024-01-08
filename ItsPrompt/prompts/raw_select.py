from prompt_toolkit import Application, HTML
from prompt_toolkit.layout.controls import FormattedTextControl

from ..data.select import process_data
from ..objects.prompts.separator import Separator
from ..objects.prompts.type import OptionsList


class RawSelectPrompt(Application):

    def __init__(
        self,
        question: str,
        options: OptionsList,
        default: str | None = None,
        disabled: tuple[str, ...] | None = None,
        allow_keyboard: bool = False,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)

        # get prompt content box
        self.prompt_content: FormattedTextControl = self.layout.container.get_children()[0].content  # type: ignore

        # save question
        self.question = question

        # self keyboard option
        self.allow_keyboard = allow_keyboard

        # process options
        self.options = process_data(options)

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

        # default select default option (or first if not given)
        if default is not None:
            for i, option in enumerate(self.options):
                if option.id == default:
                    if option.is_disabled:
                        raise ValueError("Default value must not be disabled.")
                    self.selection = i
                    break
            else:
                raise ValueError('Default value is not a valid id.')
        else:
            self.selection = 0

        # if the current selection is disabled, we will skip it
        while self.options[self.selection].is_disabled:
            self.selection = (self.selection + 1) % len(self.options)

    def update(self):
        """update prompt content"""
        # question
        content = f'[<question_mark>?</question_mark>] <question>{self.question}</question>:'

        # options
        for i, option in self.options.with_separators_enumerate():

            if type(option) is Separator:
                content += f"\n<separator>{option.label}</separator>"
                continue

            disabled = ("<disabled>", "</disabled>") if option.is_disabled else ("", "")  # type: ignore
            # Disabled tags will only be inserted if the option is disabled,
            # otherwise there will only be an empty string inserted.

            if i == self.selection:
                content += f'\n{disabled[0]}<selected_option>    {i + 1}) {option.name}</selected_option>{disabled[1]}'  # type: ignore
            else:
                content += f'\n{disabled[0]}<option>    {i + 1}) {option.name}</option>{disabled[1]}'  # type: ignore

        # text
        content += f'\n<text>    Answer: {self.selection + 1}</text>'

        self.prompt_content.text = HTML(content)

    def prompt(self) -> str | None:
        """start the application, returns the return value"""
        self.update()
        out: str | None = self.run()

        return out

    def on_up(self):
        """when up is pressed, the previous indexed option will be selected"""
        if not self.allow_keyboard:
            return

        self.selection = (self.selection - 1) % len(self.options)

        # if the current selection is disabled, we will skip it
        while self.options[self.selection].is_disabled:
            self.selection = (self.selection - 1) % len(self.options)

        self.update()

    def on_down(self):
        """when down is pressed, the next indexed option will be selected"""
        if not self.allow_keyboard:
            return

        self.selection = (self.selection + 1) % len(self.options)

        # if the current selection is disabled, we will skip it
        while self.options[self.selection].is_disabled:
            self.selection = (self.selection + 1) % len(self.options)

        self.update()

    def on_key(self, key_sequence: list[str]):
        """when an index is pressed, which is available to select, select this index"""
        key = key_sequence[0]

        # return if key is not a number
        if not key.isnumeric():
            return

        id = int(key)

        # and return if key is not in the range of possible indices
        if id <= 0 or id > len(self.options):
            return

        # and return if selection is disabled
        if self.options[id - 1].is_disabled:
            return

        self.selection = id - 1

        self.update()

    def on_enter(self):
        # get selected id
        self.exit(result=self.options[self.selection].id)
