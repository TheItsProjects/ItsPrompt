import pytest
from prompt_toolkit.keys import Keys

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
