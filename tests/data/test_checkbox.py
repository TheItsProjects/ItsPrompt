import pytest

from ItsPrompt.data.checkbox import CheckboxOption, process_data


def test_process_data_standard_options():
    options = ("first", "second", "third")

    result = [
        CheckboxOption("first", "first", False, False),
        CheckboxOption("second", "second", False, False),
        CheckboxOption("third", "third", False, False),
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
        CheckboxOption("first", "1", False, False),
        CheckboxOption("second", "2", False, False),
        CheckboxOption("third", "3", False, False),
    ]

    ans = process_data(options)

    assert ans == result


def test_process_data_raises_type_error():
    options = ("first", "second", 3)

    with pytest.raises(TypeError):
        ans = process_data(options)  # type: ignore # mypy: ignore
