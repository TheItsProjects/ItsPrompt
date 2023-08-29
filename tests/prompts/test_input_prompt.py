import pytest
from prompt_toolkit.completion import FuzzyWordCompleter
from prompt_toolkit.keys import Keys

from ItsPrompt.prompt import Prompt


# --- input ---
@pytest.mark.parametrize(
    "keys,a",
    [
        [(Keys.Enter,), ""],
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
        [(Keys.Enter,), "default"],
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
        [(*KeysAltEnter,), ""],
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


def test_input_raises_keyboard_interrupt(send_keys):
    send_keys(Keys.ControlC)

    with pytest.raises(KeyboardInterrupt):
        ans = Prompt.input("")


# TODO input show_symbol is showing symbol (visual)
# TODO input completer/completions is working (visual, functional)
# TODO input validation is showing error (visual)
