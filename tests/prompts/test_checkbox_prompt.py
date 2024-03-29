import pytest
from prompt_toolkit.keys import Keys

from ItsPrompt.objects.prompts.separator import Separator
from ItsPrompt.prompt import Prompt


# --- checkbox ---
@pytest.mark.parametrize(
    "keys,i",
    [
        [(Keys.Enter,), ()],
        [(" ", Keys.Enter), (0,)],
        [(Keys.Down, " ", Keys.Enter), (1,)],
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
        [(Keys.Enter,), (0,)],
        [(" ", Keys.Enter), ()],
        [(Keys.Down, " ", Keys.Enter), (0, 1)],
        [(" ", Keys.Up, " ", Keys.Enter), (2,)],
    ],
)
def test_checkbox_with_default(send_keys, keys: list[Keys | str], i: list[int]):
    options = ("first", "second", "third")

    send_keys(*keys)

    ans = Prompt.checkbox("", options, default_checked=("first",))

    assert ans == [options[n] for n in i]


def test_checkbox_raises_invalid_default():
    options = ("first", "second", "third")

    with pytest.raises(ValueError):
        ans = Prompt.checkbox("", options, default_checked=("invalid",))


def test_checkbox_raises_keyboard_interrupt(send_keys):
    send_keys(Keys.ControlC)

    options = ("first", "second", "third")

    with pytest.raises(KeyboardInterrupt):
        ans = Prompt.checkbox("", options)


# yapf: disable
@pytest.mark.parametrize(
    "keys,i",
    [
        [(" ", Keys.Enter,), (1,)],
        [(Keys.Up, " ", Keys.Enter), (2,)],
        [(Keys.Down, Keys.Down, " ", Keys.Enter), (1,)]
    ]
)
# yapf: enable
def test_checkbox_with_disabled(send_keys, keys: list[Keys | str], i: list[int]):
    options = ("first", "second", "third")

    send_keys(*keys)

    ans = Prompt.checkbox("", options, disabled=("first",))

    assert ans == [options[n] for n in i]


def test_checkbox_with_separator(send_keys):
    options = ("first", "second", Separator("separator"), "third")

    send_keys(Keys.Down, Keys.Down, " ", Keys.Enter)

    ans = Prompt.checkbox("", options)

    assert ans == ["third"]


def test_checkbox_raises_invalid_disabled():
    options = ("first", "second", "third")
    with pytest.raises(ValueError):
        ans = Prompt.checkbox("", options, disabled=("invalid",))


# TODO check min selections with error box (visual)
