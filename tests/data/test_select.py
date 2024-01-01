import pytest

from ItsPrompt.data.select import SelectOption, process_data
from ItsPrompt.objects.prompts.separator import Separator


def test_process_data_standard_options():
    options = ("first", "second", "third")

    result = [
        SelectOption("first", "first", False),
        SelectOption("second", "second", False),
        SelectOption("third", "third", False),
    ]

    ans = process_data(options)

    assert ans == result


def test_process_data_tuple_options():
    options = (
        ("first", "1"),
        ("second", "2"),
        ("third", "3"),
    )

    result = [
        SelectOption("first", "1", False),
        SelectOption("second", "2", False),
        SelectOption("third", "3", False),
    ]

    ans = process_data(options)

    assert ans == result


def test_process_data_raises_type_error():
    options = ("first", "second", 3)

    with pytest.raises(TypeError):
        ans = process_data(options)  # type: ignore # mypy: ignore


def test_process_data_with_separator():
    separator = Separator("second")
    options = ("first", separator, "third")

    result = [
        SelectOption("first", "first", False),
        separator,
        SelectOption("third", "third", False)
    ]

    ans = process_data(options)

    assert ans.with_separators == result
