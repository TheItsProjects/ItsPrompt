import os

from pandas import DataFrame


class Table:

    def __init__(self, data: DataFrame) -> None:
        '''
        Creates a table object for storing the drawable table instance

        :param data: the data to display
        :type data: DataFrame
        '''
        # change type of all columns to str
        # TODO maybe later support more datatypes
        self.data = data.astype('string')

        # save amount of rows
        self.row_count = len(self.data) + 1
        self.col_count = len(self.data.columns)

        # get max cell width
        max_width = os.get_terminal_size().columns

        # get width for each cell
        self.cell_width = (max_width - 1) // len(self.data.columns) - 1

        # save current selected cell
        self.cur_cell = [0, 0]  # ignoring header, as this can not be selected

    def _col_is_last(self, col) -> bool:
        '''checks if the given column is the last column in the DataFrame'''
        return self.data.columns.get_loc(col) == len(self.data.columns) - 1

    def _char_if_last_else_otherchar(
        self,
        col,
        char: str,
        otherchar: str,
    ) -> str:
        '''returns the `char` if the given column is the last in the DataFrame, otherwise returns the `otherchar`'''
        return char if self._col_is_last(col) else otherchar

    def get_table_as_str(self) -> str:
        '''
        Returns the table as a printable string
        
        Respects the width of the terminal at time of creation of the table object. Later this may be made dynamic.
        '''

        # set initial list (each entry represents a line to print)
        table_out = [''] * (self.row_count * 2 + 1
                            )  # 2 lines for every row + bottom border

        # append left border to every string
        table_out[0] += '┌'

        for i in range(1, len(table_out), 2):
            table_out[i] += '│'
            table_out[i + 1] += '├'

        table_out[-1] = '└'

        # add headers
        for header in self.data.columns:
            table_out[
                0] += '─' * self.cell_width + self._char_if_last_else_otherchar(
                    header, '┐', '┬')

            if len(str(header)) > self.cell_width:
                # convert the header to str in case the user did not give a header, so it is an integer
                header = header[:self.cell_width - 1] + '.'

            table_out[1] += f'{header:^{self.cell_width}}' + '│'

        # add values, iterate over each column
        for header, values in self.data.items():
            # iterate over each row
            for i, val in zip(
                    range(2, len(table_out), 2),
                    values):  # start at 2, because first two rows are header
                table_out[
                    i] += '─' * self.cell_width + self._char_if_last_else_otherchar(
                        header, '┤', '┼')
                table_out[i + 1] += f'{str(val):{self.cell_width}}' + '│'

            table_out[
                -1] += '─' * self.cell_width + self._char_if_last_else_otherchar(
                    header, '┘', '┴')

        return '\n'.join(table_out)

    def on_up(self):
        '''when up is pressed, select same column, but row one above (or last row if current is 0)'''

        self.cur_cell[1] = (self.cur_cell[1] - 1) % (self.row_count - 1)

    def on_down(self):
        '''when down is pressed, select same column, but row one below (or first row if current is last)'''

        self.cur_cell[1] = (self.cur_cell[1] + 1) % (self.row_count - 1)

    def on_left(self):
        '''when left is pressed, select same row, but column one to the left (or last column if current is 0)'''

        self.cur_cell[0] = (self.cur_cell[0] - 1) % (self.col_count)

    def on_right(self):
        '''when right is pressed, select same row, but column one to the right (or first column if current is last)'''

        self.cur_cell[0] = (self.cur_cell[0] + 1) % (self.col_count)

    def add_key(self, key: str):
        '''add key to current selected cell'''
        self.data.iat[self.cur_cell[1], self.cur_cell[0]] += key

    def del_key(self):
        '''remove last key from current selected cell'''
        self.data.iat[self.cur_cell[1],
                      self.cur_cell[0]] = self.data.iat[self.cur_cell[1],
                                                        self.cur_cell[0]][:-1]

    def get_current_cursor_position(self) -> tuple[int, int]:
        '''returns the current position of the cursor, relative to the top left corner character as (0, 0)'''
        y = self.cur_cell[1] * 2 + 3  # 3 is offset for header

        item_length = len(self.data.iat[
            self.cur_cell[1],
            self.cur_cell[0]])  # length of the item in the current cell

        x = (self.cell_width + 1) * self.cur_cell[
            0] + 1 + item_length  # 1 is offset for left border, item_length is length of item
        return (x, y)
