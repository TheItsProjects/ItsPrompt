from ItsPrompt.prompt import Prompt

from prompt_toolkit.keys import Keys
from prompt_toolkit.completion import FuzzyWordCompleter

import pytest


# --- Select ---
@pytest.mark.parametrize(
    "keys,i",
    [
        [(Keys.Enter, ), 0],
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
        [(Keys.Enter, ), 1],
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


# --- RawSelect ---
@pytest.mark.parametrize(
    "keys,i",
    [
        [(Keys.Enter, ), 0],
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
        [(Keys.Enter, ), 1],
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
        [(Keys.Enter, ), 0],
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


# --- Expand ---
@pytest.mark.parametrize(
    "keys,i",
    [
        [("f", Keys.Enter), 0],
        [("sft", Keys.Enter), 2],
        [(Keys.Enter, "hs", Keys.Enter), 1],
        [(Keys.Up, Keys.Down, "99", "s", Keys.Enter), 1],
    ],
)
def test_expand(send_keys, keys: list[Keys | str], i: int):
    options = ("first", "second", "third")

    send_keys(*keys)

    ans = Prompt.expand("", options)

    assert ans == options[i]


@pytest.mark.parametrize(
    "keys,i",
    [
        [("f", Keys.Enter), 0],
        [("sft", Keys.Enter), 2],
        [(Keys.Enter, "hs", Keys.Enter), 1],
    ],
)
def test_expand_with_default(send_keys, keys: list[Keys | str], i: int):
    options = ("first", "second", "third")

    send_keys(*keys)

    ans = Prompt.expand("", options, default="second")

    assert ans == options[i]


@pytest.mark.parametrize(
    "keys,i",
    [
        [(Keys.Up, Keys.Enter), 2],
        [(Keys.Down, "hs", Keys.Enter), 1],
    ],
)
def test_expand_with_keyboard(send_keys, keys: list[Keys | str], i: int):
    options = ("first", "second", "third")

    send_keys(*keys)

    ans = Prompt.expand("", options, allow_keyboard=True)

    assert ans == options[i]


def test_expand_raises_invalid_default():
    options = ("first", "second", "third")

    with pytest.raises(ValueError):
        ans = Prompt.expand("", options, default="invalid")


# --- checkbox ---
@pytest.mark.parametrize(
    "keys,i",
    [
        [(Keys.Enter, ), ()],
        [(" ", Keys.Enter), (0, )],
        [(Keys.Down, " ", Keys.Enter), (1, )],
        [(" ", Keys.Up, " ", Keys.Enter), (0, 2)],
    ],
)
def test_checkbox(send_keys, keys: list[Keys | str], i: list[int]):
    options = ("first", "second", "third")

    send_keys(*keys)

    ans = Prompt.checkbox("", options)

    assert ans == [options[n] for n in i]


@pytest.mark.parametrize(
    "keys,i",
    [
        [(Keys.Enter, ), (0, )],
        [(" ", Keys.Enter), ()],
        [(Keys.Down, " ", Keys.Enter), (0, 1)],
        [(" ", Keys.Up, " ", Keys.Enter), (2, )],
    ],
)
def test_checkbox_with_default(send_keys, keys: list[Keys | str],
                               i: list[int]):
    options = ("first", "second", "third")

    send_keys(*keys)

    ans = Prompt.checkbox("", options, default_checked=("first", ))

    assert ans == [options[n] for n in i]


def test_checkbox_raises_invalid_default():
    options = ("first", "second", "third")

    with pytest.raises(ValueError):
        ans = Prompt.checkbox("", options, default_checked=("invalid", ))


# TODO check min selections with error box (visual)


# --- confirm ---
@pytest.mark.parametrize(
    "key,a",
    [
        ["y", True],
        ["n", False],
        ["ay", True],
    ],
)
def test_confirm(send_keys, key: str, a: bool):
    send_keys(key)

    ans = Prompt.confirm("")

    assert ans == a


@pytest.mark.parametrize(
    "key,a",
    [
        ["y", True],
        ["n", False],
        [Keys.Enter, True],
    ],
)
def test_confirm_with_default(send_keys, key: str, a: bool):
    send_keys(key)

    ans = Prompt.confirm("", default=True)

    assert ans == a


# TODO confirm selections with error box (visual)


# --- input ---
@pytest.mark.parametrize(
    "keys,a",
    [
        [(Keys.Enter, ), ""],
        [("test", Keys.Enter), "test"],
    ],
)
def test_input(send_keys, keys: list[Keys | str], a: str):
    send_keys(*keys)

    ans = Prompt.input("")

    assert ans == a


@pytest.mark.parametrize(
    "keys,a",
    [
        [(Keys.Enter, ), "default"],
        [("test", Keys.Enter), "test"],
    ],
)
def test_input_with_default(send_keys, keys: list[Keys | str], a: str):
    send_keys(*keys)

    ans = Prompt.input("", default="default")

    assert ans == a


KeysAltEnter = Keys.Escape, Keys.Enter  # Vt100 terminals convert "alt+key" to "escape,key"


@pytest.mark.parametrize(
    "keys,a",
    [
        [(*KeysAltEnter, ), ""],
        [("test", Keys.Enter, *KeysAltEnter), "test\n"],
    ],
)
def test_input_with_multiline(send_keys, keys: list[Keys | str], a: str):
    send_keys(*keys)

    ans = Prompt.input("", multiline=True)

    assert ans == a


def test_input_raises_two_completers_given():
    completions = ["first", "second", "third"]
    completer = FuzzyWordCompleter(completions)

    with pytest.raises(ValueError):
        ans = Prompt.input("", completions=completions, completer=completer)


def test_input_raises_completer_and_show_symbol_given():
    completions = ["first", "second", "third"]

    with pytest.raises(ValueError):
        ans = Prompt.input("", completions=completions, show_symbol="*")


# TODO input show_symbol is showing symbol (visual)
# TODO input completer/completions is working (visual, functional)
# TODO input validation is showing error (visual)
