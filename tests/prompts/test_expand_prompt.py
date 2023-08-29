import pytest
from prompt_toolkit.keys import Keys

from ItsPrompt.prompt import Prompt


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


def test_expand_raises_keyboard_interrupt(send_keys):
    send_keys(Keys.ControlC)

    options = ("first", "second", "third")

    with pytest.raises(KeyboardInterrupt):
        ans = Prompt.expand("", options)
