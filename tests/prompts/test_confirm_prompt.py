import pytest
from prompt_toolkit.keys import Keys

from ItsPrompt.prompt import Prompt


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


def test_confirm_raises_keyboard_interrupt(send_keys):
    send_keys(Keys.ControlC)

    with pytest.raises(KeyboardInterrupt):
        ans = Prompt.confirm("")


# TODO confirm selections with error box (visual)
