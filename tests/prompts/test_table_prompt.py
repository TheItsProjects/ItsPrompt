import pytest
from pandas import DataFrame
from pandas.testing import assert_frame_equal
from prompt_toolkit.keys import Keys

from ItsPrompt.objects.prompts.type import TablePromptDict, TablePromptList
from ItsPrompt.prompt import Prompt


# --- table ---
@pytest.mark.parametrize(
    "keys,a",
    [
        [
            (Keys.Enter,),
            DataFrame({"0": ["first", "second", "third"]}),
        ],
        [
            (Keys.Down, "new", Keys.Enter),
            DataFrame({"0": ["first", "secondnew", "third"]}),
        ],
        [
            (Keys.Left, Keys.Right, Keys.Up, Keys.Down, Keys.Enter),
            DataFrame({"0": ["first", "second", "third"]}),
        ],
        [
            (Keys.Backspace, Keys.Enter),
            DataFrame({"0": ["firs", "second", "third"]}),
        ],
    ],
)
def test_table_dataframe(send_keys, mock_terminal_size, keys: list[Keys | str], a: DataFrame):
    data = DataFrame(["first", "second", "third"])

    send_keys(*keys)

    ans = Prompt.table("", data)

    assert_frame_equal(ans, a)


@pytest.mark.parametrize(
    "keys,a",
    [
        [
            (Keys.Enter,),
            {"0": ["first", "second", "third"]},
        ],
        [
            (Keys.Down, "new", Keys.Enter),
            {"0": ["first", "secondnew", "third"]},
        ],
        [
            (Keys.Left, Keys.Right, Keys.Up, Keys.Down, Keys.Enter),
            {"0": ["first", "second", "third"]},
        ],
        [
            (Keys.Backspace, Keys.Enter),
            {"0": ["firs", "second", "third"]},
        ],
    ],
)
def test_table_dictionary(send_keys, mock_terminal_size, keys: list[Keys | str], a: TablePromptDict):
    data = {"0": ["first", "second", "third"]}

    send_keys(*keys)

    ans = Prompt.table("", data)

    assert ans == a


@pytest.mark.parametrize(
    "keys,a",
    [
        [
            (Keys.Enter,),
            [["first", "second", "third"]],
        ],
        [
            (Keys.Down, "new", Keys.Enter),
            [["first", "secondnew", "third"]],
        ],
        [
            (Keys.Left, Keys.Right, Keys.Up, Keys.Down, Keys.Enter),
            [["first", "second", "third"]],
        ],
        [
            (Keys.Backspace, Keys.Enter),
            [["firs", "second", "third"]],
        ],
    ],
)
def test_table_list(send_keys, mock_terminal_size, keys: list[Keys | str], a: TablePromptList):
    data = [["first", "second", "third"]]

    send_keys(*keys)

    ans = Prompt.table("", data)

    assert ans == a


def test_table_raises_keyboard_interrupt(send_keys):
    send_keys(Keys.ControlC)

    data = DataFrame(["first", "second", "third"])

    with pytest.raises(KeyboardInterrupt):
        ans = Prompt.table("", data)


def test_table_dictionary_raises_lists_not_same_lengths(send_keys):
    send_keys(Keys.ControlC)

    data = {"0": ["first", "second", "third"], "1": ["other first"]}

    with pytest.raises(ValueError):
        ans = Prompt.table("", data)
