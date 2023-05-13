import os

from pandas import DataFrame

from ItsPrompt.data.table import Table


def test_table_shortens_long_header(mock_terminal_size):
    width = os.get_terminal_size().columns

    data = DataFrame({"a" * (width - 1): ["first"]})

    table = Table(data)

    assert "." in table.get_table_as_str().split("\n")[1]
