from prompt_toolkit import HTML, Application
from prompt_toolkit.layout.controls import FormattedTextControl

from ..data.expand import process_data


class ExpandPrompt(Application):

    def __init__(
        self,
        question: str,
        options: tuple[str | tuple[str, str, str], ...],
        default: str | None = None,
        allow_keyboard: bool = False,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)

        # get prompt content box
        self.prompt_content: FormattedTextControl = self.layout.container.get_children(
        )[0].content  # type: ignore

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

        # default select default option (or "help" if not given)
        if default is None:
            self.selection = 'h'
            return

        for i, option in enumerate(self.options):
            if option.id == default:
                self.selection = option.key
                break
        else:
            raise ValueError('Default value is not a valid id.')

    def update(self):
        '''update prompt content'''
        # question
        content = f'[<question_mark>?</question_mark>] <question>{self.question}</question>: <text>({self.keys})</text>'

        # options, show only if it is expanded
        if self.is_expanded:
            for option in self.options:
                if option.key == self.selection:
                    content += f'\n<selected_option>    {option.key}) {option.name}</selected_option>'
                else:
                    content += f'\n<option>    {option.key}) {option.name}</option>'

        # text
        content += f'\n<text>    Answer: {self.selection}</text>'

        self.prompt_content.text = HTML(content)

    def prompt(self) -> str | None:
        '''start the application, returns the return value'''
        self.update()
        out: str | None = self.run()

        return out

    def on_up(self):
        '''when up is pressed, the previous indexed option will be selected'''
        if not self.allow_keyboard:
            return

        self.selection = self.keys[(self.keys.index(self.selection) - 1) %
                                   len(self.keys)]

        self.update()

    def on_down(self):
        '''when down is pressed, the next indexed option will be selected'''
        if not self.allow_keyboard:
            return

        self.selection = self.keys[(self.keys.index(self.selection) + 1) %
                                   len(self.keys)]

        self.update()

    def on_key(self, key_sequence: list[str]):
        '''when a index is pressed, which is available to select, select this index'''
        key = key_sequence[0]

        # return if key is not a an available key
        if not key in self.keys:
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
