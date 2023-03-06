from prompt_toolkit import HTML, Application
from prompt_toolkit.layout.controls import FormattedTextControl

from ..data.select import process_data


class SelectPrompt(Application):

    def __init__(
        self,
        question: str,
        options: tuple[str | tuple[str, str], ...],
        default: str | None = None,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)

        # get prompt content box
        self.prompt_content: FormattedTextControl = self.layout.container.get_children(
        )[0].content  # type: ignore

        # save question
        self.question = question

        # process options
        self.options = process_data(options)

        # default select default option (or first if not given)
        if default is None:
            self.selection = 0
            return

        for i, option in enumerate(self.options):
            if option.id == default:
                self.selection = i
                break
        else:
            raise ValueError('Default value is not a valid id.')

    def update(self):
        '''update prompt content'''
        content = f'[<question_mark>?</question_mark>] <question>{self.question}</question>:'

        for i, option in enumerate(self.options):
            if i == self.selection:
                content += f'\n<selected_option>  > {option.name}</selected_option>'
            else:
                content += f'\n<option>    {option.name}</option>'

        self.prompt_content.text = HTML(content)

    def prompt(self) -> str | None:
        '''start the application, returns the return value'''
        self.update()
        out: str | None = self.run()

        return out

    def on_up(self):
        '''when up is pressed, the previous indexed option will be selected'''
        self.selection = (self.selection - 1) % len(self.options)

        self.update()

    def on_down(self):
        '''when down is pressed, the next indexed option will be selected'''
        self.selection = (self.selection + 1) % len(self.options)

        self.update()

    def on_enter(self):
        # get selected id
        self.exit(result=self.options[self.selection].id)
