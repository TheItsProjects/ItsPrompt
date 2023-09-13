import html
from typing import TYPE_CHECKING, Union

from prompt_toolkit import Application, HTML
from prompt_toolkit.data_structures import Point
from prompt_toolkit.layout.controls import FormattedTextControl

from ..data.table import Table
from ..objects.prompts.type import TablePromptDict, TablePromptList

if TYPE_CHECKING:  # pragma: no cover
    from pandas import DataFrame


class TablePrompt(Application):

    def __init__(
        self,
        question: str,
        data: Union["DataFrame", TablePromptDict, TablePromptList],
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)

        # get prompt content box
        self.prompt_content: FormattedTextControl = self.layout.container.get_children()[0].content  # type: ignore

        # save question
        self.question = question

        # process data
        self.table = Table(data)

        # set cursor
        self.prompt_content.get_cursor_position = lambda: Point(
            self.table.get_current_cursor_position()[0],
            self.table.get_current_cursor_position()[1] + 1,  # add 1 offset for height of question
        )

    def update(self):
        """update prompt content"""
        content = f'[<question_mark>?</question_mark>] <question>{self.question}</question>:\n'

        # append table
        content += html.escape(
            self.table.get_table_as_str()
        )  # escaping is needed so formatting from PromptToolkit won't destroy the whole table

        self.prompt_content.text = HTML(content)

    def prompt(self) -> Union["DataFrame", TablePromptDict, None]:
        """start the application, returns the return value"""
        self.update()
        out: Union["DataFrame", TablePromptDict, None] = self.run()

        return out

    def on_up(self):
        """when up is pressed, the cell one above will be selected"""
        self.table.on_up()

        self.update()

    def on_down(self):
        """when down is pressed, the cell one below will be selected"""
        self.table.on_down()

        self.update()

    def on_left(self):
        """when left is pressed, the cell one to the left will be selected"""
        self.table.on_left()

        self.update()

    def on_right(self):
        """when left is pressed, the cell one to the right will be selected"""
        self.table.on_right()

        self.update()

    def on_key(self, key_sequence: list[str]):
        """when a key is pressed, the key will be added to the current cells content"""
        key = key_sequence[0]
        self.table.add_key(key)

        self.update()

    def on_backspace(self):
        """when backspace is pressed, the last char will be removed from the current cells content"""
        self.table.del_key()

        self.update()

    def on_enter(self):
        # return the modified table
        self.exit(result=self.table.data.get_data())
