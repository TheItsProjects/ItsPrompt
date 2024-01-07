from prompt_toolkit import Application, HTML
from prompt_toolkit.layout.controls import FormattedTextControl

from ..data.expand import process_data
from ..objects.prompts.separator import Separator
from ..objects.prompts.type import OptionsList


class ExpandPrompt(Application):

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

        # save keyboard option
        self.allow_keyboard = allow_keyboard

        # save whether view is expanded or not
        self.is_expanded = False

        # process options
        self.options = process_data(options)

        # save a string with all keys
        self.keys = ''.join([option.key for option in self.options])

        # save disabled keys
        self.disabled = [key[0] for key in disabled] if disabled else ()

        # default select default option (or "help" if not given)
        if default is None:
            self.selection = 'h'

        else:
            for i, option in enumerate(self.options):
                if option.id == default:
                    self.selection = option.key
                    break
            else:
                raise ValueError('Default value is not a valid id.')

        # if default is disabled, raise an error
        if disabled and default in disabled:
            raise ValueError("Default value can not be disabled.")

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

    def update(self):
        """update prompt content"""
        # question
        content = f'[<question_mark>?</question_mark>] <question>{self.question}</question>: <text>({self.keys})</text>'

        # options, show only if it is expanded
        if self.is_expanded:
            for _, option in self.options.with_separators_enumerate():

                if type(option) is Separator:
                    content += f"\n<separator>{option.label}</separator>"
                    continue

                disabled = ("<disabled>", "</disabled>") if option.is_disabled else ("", "")  # type: ignore
                # Disabled tags will only be inserted if the option is disabled,
                # otherwise there will only be an empty string inserted.

                if option.key == self.selection:  # type: ignore
                    content += f'\n{disabled[0]}<selected_option>    {option.key}) {option.name}</selected_option>{disabled[1]}'  # type: ignore
                else:
                    content += f'\n{disabled[0]}<option>    {option.key}) {option.name}</option>{disabled[1]}'  # type: ignore

        # text
        content += f'\n<text>    Answer: {self.selection}</text>'

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

        self.selection = self.keys[(self.keys.index(self.selection) - 1) % len(self.keys)]

        # if the current selection is disabled, we will skip it
        while self.options[(self.keys.index(self.selection)) % len(self.keys)].is_disabled:
            self.selection = self.keys[(self.keys.index(self.selection) - 1) % len(self.keys)]

        self.update()

    def on_down(self):
        """when down is pressed, the next indexed option will be selected"""
        if not self.allow_keyboard:
            return

        self.selection = self.keys[(self.keys.index(self.selection) + 1) % len(self.keys)]

        # if the current selection is disabled, we will skip it
        while self.options[(self.keys.index(self.selection)) % len(self.keys)].is_disabled:
            self.selection = self.keys[(self.keys.index(self.selection) + 1) % len(self.keys)]

        self.update()

    def on_key(self, key_sequence: list[str]):
        """when an index is pressed, which is available to select, select this index"""
        key = key_sequence[0]

        # return if key is not an available key
        if key not in self.keys:
            return

        # return if key is disabled
        if key in self.disabled:
            return

        # only expand if h is pressed, otherwise change selection
        if key == 'h':
            self.is_expanded = not self.is_expanded
        else:
            self.selection = key

        self.update()

    def on_enter(self):
        # if current selection is h-key, change is_expanded
        # otherwise return selected id
        if self.selection == 'h':
            self.is_expanded = not self.is_expanded
            self.update()
            return

        # get selected id
        self.exit(result=self.options[self.keys.index(self.selection)].id)
