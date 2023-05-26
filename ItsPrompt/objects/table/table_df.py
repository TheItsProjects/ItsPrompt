from typing import Generator

from pandas import DataFrame

from .table_base import TableDataBase


class TableDataFromDF(TableDataBase):

    def __init__(self, data: DataFrame) -> None:
        self.data = data.astype("str")  # convert all values to str
        self.data = self.data.rename(columns=lambda x: str(x))  # convert all headers to str

    @property
    def row_count(self) -> int:
        return len(self.data) + 1

    @property
    def col_count(self) -> int:
        return len(self.data.columns)

    @property
    def columns(self) -> tuple[str, ...]:
        return tuple(self.data.columns)

    def items(self) -> Generator[tuple[str, tuple[str, ...]], None, None]:
        for header, values in self.data.items():
            yield str(header), tuple(values)

    def get_item_at(self, row: int, col: int) -> str:
        return self.data.iat[row, col]

    def set_item_at(self, row: int, col: int, val: str) -> None:
        self.data.iat[row, col] = val

    def add_key(self, row: int, col: int, key: str):
        new = self.get_item_at(row, col) + key
        self.set_item_at(row, col, new)

    def del_key(self, row: int, col: int):
        new = self.get_item_at(row, col)[:-1]
        self.set_item_at(row, col, new)

    def get_column_location(self, val: str) -> int:
        return self.data.columns.get_loc(val)

    def get_data(self) -> DataFrame:
        return self.data
