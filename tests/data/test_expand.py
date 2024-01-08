import pytest

from ItsPrompt.data.expand import ExpandOption, process_data
from ItsPrompt.objects.prompts.separator import Separator


def test_process_data_standard_options():
    options = ("first", "second", "third")

    result = [
        ExpandOption("f", "first", "first", False),
        ExpandOption("s", "second", "second", False),
        ExpandOption("t", "third", "third", False),
        ExpandOption("h", "Help Menu, list or hide all options", "", False),
    ]

    ans = process_data(options)

    assert ans == result


def test_process_data_tuple_options():
    options = (
        ("1", "first", "1"),
        ("2", "second", "2"),
        ("3", "third", "3"),
    )

    result = [
        ExpandOption("1", "first", "1", False),
        ExpandOption("2", "second", "2", False),
        ExpandOption("3", "third", "3", False),
        ExpandOption("h", "Help Menu, list or hide all options", "", False),
    ]

    ans = process_data(options)

    assert ans == result


def test_process_data_raises_unique_keys():
    options = ("double", "double")

    with pytest.raises(ValueError):
        ans = process_data(options)


def test_process_data_raises_key_too_long():
    options = (("tt", "too long", "tt"),)

    with pytest.raises(ValueError):
        ans = process_data(options)


def test_process_data_raises_key_not_ascii():
    options = (("❓", "not ascii", "na"),)

    with pytest.raises(ValueError):
        ans = process_data(options)


def test_process_data_raises_h_given():
    options = (("h", "h given", "h"),)

    with pytest.raises(ValueError):
        ans = process_data(options)


def test_process_data_raises_type_error():
    options = (["i", "invalid"],)

    with pytest.raises(TypeError):
        ans = process_data(options)  # type: ignore # mypy: ignore


def test_process_data_with_separator():
    separator = Separator("second")
    options = ("first", separator, "third")

    result = [
        ExpandOption("f", "first", "first", False), separator,
        ExpandOption("t", "third", "third", False),
        ExpandOption(key='h', name='Help Menu, list or hide all options', id='', is_disabled=False)
    ]

    ans = process_data(options)

    assert ans.with_separators == result
