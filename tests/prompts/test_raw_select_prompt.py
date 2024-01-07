import pytest
from prompt_toolkit.keys import Keys

from ItsPrompt.objects.prompts.separator import Separator
from ItsPrompt.prompt import Prompt


# --- RawSelect ---
@pytest.mark.parametrize(
    "keys,i",
    [
        [(Keys.Enter,), 0],
        [("1", Keys.Enter), 0],
        [("2", Keys.Enter), 1],
        [(Keys.Up, Keys.Down, "abc", "99", Keys.Enter), 0],
    ],
)
def test_raw_select(send_keys, keys: list[Keys | str], i: int):
    options = ("first", "second", "third")

    send_keys(*keys)

    ans = Prompt.raw_select("", options)

    assert ans == options[i]


@pytest.mark.parametrize(
    "keys,i",
    [
        [(Keys.Enter,), 1],
        [("1", Keys.Enter), 0],
        [("2", Keys.Enter), 1],
    ],
)
def test_raw_select_with_default(send_keys, keys: list[Keys | str], i: int):
    options = ("first", "second", "third")

    send_keys(*keys)

    ans = Prompt.raw_select("", options, default="second")

    assert ans == options[i]


@pytest.mark.parametrize(
    "keys,i",
    [
        [(Keys.Enter,), 0],
        [(Keys.Down, Keys.Enter), 1],
        [(Keys.Up, Keys.Enter), 2],
    ],
)
def test_raw_select_with_keyboard(send_keys, keys: list[Keys | str], i: int):
    options = ("first", "second", "third")

    send_keys(*keys)

    ans = Prompt.raw_select("", options, allow_keyboard=True)

    assert ans == options[i]


def test_raw_select_raises_invalid_default():
    options = ("first", "second", "third")

    with pytest.raises(ValueError):
        ans = Prompt.raw_select("", options, default="invalid")


def test_raw_select_raises_keyboard_interrupt(send_keys):
    send_keys(Keys.ControlC)

    options = ("first", "second", "third")

    with pytest.raises(KeyboardInterrupt):
        ans = Prompt.raw_select("", options)


# yapf: disable
@pytest.mark.parametrize(
    "keys,i",
    [
        [(Keys.Enter,), 1],
        [("1", Keys.Enter), 1]
    ]
)
# yapf: enable
def test_raw_select_with_disabled(send_keys, keys: list[Keys | str], i: int):
    options = ("first", "second", "third")

    send_keys(*keys)

    ans = Prompt.raw_select("", options, disabled=("first",))

    assert ans == options[i]


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
def test_raw_select_with_disabled_and_keyboard(send_keys, keys: list[Keys | str], i: int):
    options = ("first", "second", "third")

    send_keys(*keys)

    ans = Prompt.raw_select("", options, disabled=("first",), allow_keyboard=True)

    assert ans == options[i]


def test_raw_select_with_separator(send_keys):
    options = ("first", "second", Separator("separator"), "third")

    send_keys("1", "2", Keys.Enter)

    ans = Prompt.raw_select("", options)

    assert ans == "second"


def test_raw_select_raises_invalid_disabled():
    options = ("first", "second", "third")
    with pytest.raises(ValueError):
        ans = Prompt.raw_select("", options, disabled=("invalid",))


def test_raw_select_raises_default_is_disabled():
    options = ("first", "second", "third")
    with pytest.raises(ValueError):
        ans = Prompt.raw_select("", options, default="first", disabled=("first",))
