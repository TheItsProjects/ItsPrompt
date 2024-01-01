import pytest
from prompt_toolkit.keys import Keys

from ItsPrompt.objects.prompts.separator import Separator
from ItsPrompt.prompt import Prompt


# --- Select ---
@pytest.mark.parametrize(
    "keys,i",
    [
        [(Keys.Enter,), 0],
        [(Keys.Down, Keys.Enter), 1],
        [(Keys.Down, Keys.Down, Keys.Enter), 2],
        [(Keys.Up, Keys.Enter), 2],
    ],
)
def test_select(send_keys, keys: list[Keys | str], i: int):
    options = ("first", "second", "third")

    send_keys(*keys)

    ans = Prompt.select("", options)

    assert ans == options[i]


@pytest.mark.parametrize(
    "keys,i",
    [
        [(Keys.Enter,), 1],
        [(Keys.Down, Keys.Enter), 2],
        [(Keys.Down, Keys.Down, Keys.Enter), 0],
        [(Keys.Up, Keys.Enter), 0],
    ],
)
def test_select_with_default(send_keys, keys: list[Keys | str], i: int):
    options = ("first", "second", "third")

    send_keys(*keys)

    ans = Prompt.select("", options, default="second")

    assert ans == options[i]


def test_select_raises_invalid_default():
    options = ("first", "second", "third")
    with pytest.raises(ValueError):
        ans = Prompt.select("", options, default="invalid")


def test_select_raises_keyboard_interrupt(send_keys):
    send_keys(Keys.ControlC)

    options = ("first", "second", "third")

    with pytest.raises(KeyboardInterrupt):
        ans = Prompt.select("", options)


# yapf: disable
@pytest.mark.parametrize(
    "keys,i",
    [
        [(Keys.Enter,), 1],
        [(Keys.Up, Keys.Enter), 2],
        [(Keys.Down, Keys.Down, Keys.Enter), 1]
    ]
)
# yapf: enable
def test_select_with_disabled(send_keys, keys: list[Keys | str], i: int):
    options = ("first", "second", "third")

    send_keys(*keys)

    ans = Prompt.select("", options, disabled=("first",))

    assert ans == options[i]


def test_select_with_separator(send_keys):
    options = ("first", "second", Separator("separator"), "third")

    send_keys(Keys.Down, Keys.Down, Keys.Enter)

    ans = Prompt.select("", options)

    assert ans == "third"


def test_select_raises_invalid_disabled():
    options = ("first", "second", "third")
    with pytest.raises(ValueError):
        ans = Prompt.select("", options, disabled=("invalid",))


def test_select_raises_default_is_disabled():
    options = ("first", "second", "third")
    with pytest.raises(ValueError):
        ans = Prompt.select("", options, default="first", disabled=("first",))
