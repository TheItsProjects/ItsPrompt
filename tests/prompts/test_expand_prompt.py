import pytest
from prompt_toolkit.keys import Keys

from ItsPrompt.objects.prompts.separator import Separator
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


# yapf: disable
@pytest.mark.parametrize(
    "keys,i",
    [
        [("f", Keys.Enter, "s", Keys.Enter), 1]
    ]
)
# yapf: enable
def test_expand_with_disabled(send_keys, keys: list[Keys | str], i: int):
    options = ("first", "second", "third")

    send_keys(*keys)

    ans = Prompt.expand("", options, disabled=("first",))

    assert ans == options[i]


def test_expand_raises_invalid_disabled():
    options = ("first", "second", "third")
    with pytest.raises(ValueError):
        ans = Prompt.expand("", options, disabled=("invalid",))


def test_expand_raises_default_is_disabled():
    options = ("first", "second", "third")
    with pytest.raises(ValueError):
        ans = Prompt.expand("", options, default="first", disabled=("first",))


@pytest.mark.parametrize(
    "keys,i",
    [
        [(Keys.Down, Keys.Enter), 1],
        [("s", Keys.Up, Keys.Up, Keys.Enter), 2],  # s, h, t
        [(Keys.Down, Keys.Enter), 1]
    ]
)
def test_expand_with_disabled_and_keyboard(send_keys, keys: list[Keys | str], i: int):
    options = ("first", "second", "third")

    send_keys(*keys)

    ans = Prompt.expand("", options, disabled=("first",), allow_keyboard=True)

    assert ans == options[i]


def test_expand_with_separator(send_keys):
    options = ("first", "second", Separator("separator"), "third")

    send_keys("h", "t", Keys.Enter)

    ans = Prompt.expand("", options)

    assert ans == "third"
