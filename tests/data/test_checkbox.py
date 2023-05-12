import pytest

from ItsPrompt.data.checkbox import process_data, CheckboxOption


def test_process_data_standard_options():
    options = ("first", "second", "third")

    result = [
        CheckboxOption("first", "first", False),
        CheckboxOption("second", "second", False),
        CheckboxOption("third", "third", False),
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
        CheckboxOption("first", "1", False),
        CheckboxOption("second", "2", False),
        CheckboxOption("third", "3", False),
    ]

    ans = process_data(options)

    assert ans == result


def test_process_data_raises_type_error():
    options = ("first", "second", 3)

    with pytest.raises(TypeError):
        ans = process_data(options)  # type: ignore # mypy: ignore