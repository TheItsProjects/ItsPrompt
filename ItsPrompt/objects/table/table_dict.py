from typing import Generator

from .table_base import TableDataBase
from ..prompts.type import TablePromptDict


class TableDataFromDict(TableDataBase):

    def __init__(self, data: TablePromptDict) -> None:
        # make sure every list has same length
        lengths = set([len(t) for t in data.values()])
        if len(lengths) != 1:
            raise ValueError("Dictionary columns (lists) must be same length!")

        self.data = data

    @property
    def row_count(self) -> int:
        return len(next(iter(self.data.values()))) + 1

    @property
    def col_count(self) -> int:
        return len(self.data)

    @property
    def columns(self) -> tuple[str, ...]:
        return tuple(self.data.keys())

    def items(self) -> Generator[tuple[str, tuple[str, ...]], None, None]:
        for header, values in self.data.items():
            yield str(header), tuple(values)

    def get_item_at(self, row: int, col: int) -> str:
        # get the name of the column to edit (header)
        col_name = self.columns[col]

        return self.data[col_name][row]

    def set_item_at(self, row: int, col: int, val: str) -> None:
        # get the name of the column to edit (header)
        col_name = self.columns[col]

        self.data[col_name][row] = val

    def add_key(self, row: int, col: int, key: str):
        new = self.get_item_at(row, col) + key
        self.set_item_at(row, col, new)

    def del_key(self, row: int, col: int):
        new = self.get_item_at(row, col)[:-1]
        self.set_item_at(row, col, new)

    def get_column_location(self, val: str) -> int:
        return self.columns.index(val)

    def get_data(self) -> TablePromptDict:
        return self.data
