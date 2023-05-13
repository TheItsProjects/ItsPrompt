import pytest

from ItsPrompt.data.select import process_data, SelectOption


def test_process_data_standard_options():
    options = ("first", "second", "third")

    result = [
        SelectOption("first", "first"),
        SelectOption("second", "second"),
        SelectOption("third", "third"),
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
        SelectOption("first", "1"),
        SelectOption("second", "2"),
        SelectOption("third", "3"),
    ]

    ans = process_data(options)

    assert ans == result


def test_process_data_raises_type_error():
    options = ("first", "second", 3)

    with pytest.raises(TypeError):
        ans = process_data(options)  # type: ignore # mypy: ignore
