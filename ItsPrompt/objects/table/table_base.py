from abc import ABC, abstractmethod
from typing import Generator


class TableDataBase(ABC):  # pragma: no cover

    @property
    @abstractmethod
    def row_count(self) -> int:
        """Returns the number of rows in the table, including the header"""
        pass

    @property
    @abstractmethod
    def col_count(self) -> int:
        """Returns the number of columns in the table"""
        pass

    @property
    @abstractmethod
    def columns(self) -> tuple[str, ...]:
        """Returns the column names in the table (the first row, headers)"""
        pass

    @abstractmethod
    def items(self) -> Generator[tuple[str, tuple[str, ...]], None, None]:
        """Gets all the items in the table (each tuple contains the header and the values)"""
        pass

    @abstractmethod
    def get_item_at(self, row: int, col: int) -> str:
        """Returns the item at the given position in the table"""
        pass

    @abstractmethod
    def set_item_at(self, row: int, col: int, val: str) -> None:
        """Sets the item at the given position in the table"""
        pass

    @abstractmethod
    def add_key(self, row: int, col: int, key: str):
        """Adds the key to the given cell"""
        pass

    @abstractmethod
    def del_key(self, row: int, col: int):
        """Deletes the key from the given cell"""
        pass

    @abstractmethod
    def get_column_location(self, val: str) -> int:
        """Returns the location of the column in the table"""
        pass

    @abstractmethod
    def get_data(self):
        """Returns the actual data"""
        pass
