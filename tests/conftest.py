import os
from typing import NamedTuple

import pytest
from prompt_toolkit.application import create_app_session
from prompt_toolkit.input import create_pipe_input, ansi_escape_sequences, PipeInput
from prompt_toolkit.keys import Keys
from prompt_toolkit.output import DummyOutput


def key_converter(*keys: Keys | str) -> str:
    """
    Convert a key sequence to a sequence of stringified keys

    The keys may either be a `prompt_toolkit.keys.Keys` or a string, which will be interpreted as text to type.

    The returned string is usable with `PipeInput.send_text()`.

    :return: all given keys combined to a single string
    :rtype: str
    """
    out = ""

    for key in keys:
        if type(key) is Keys:
            out += ansi_escape_sequences.REVERSE_ANSI_SEQUENCES[key]
        else:
            out += key

    return out


@pytest.fixture(autouse=True, scope="function")
def mock_input():
    """
    Fixture for creating a dummy prompt session

    Terminal inputs can be created by using pipe_input.
    """
    with create_pipe_input() as pipe_input:
        with create_app_session(input=pipe_input, output=DummyOutput()):
            yield pipe_input


@pytest.fixture(autouse=True, scope="function")
def send_keys(mock_input: PipeInput):
    """
    Fixture for easily sending keys to the terminal session

    The returned callable can be called to convert a list of Keys or strings to one string, which will then be sent
    to the terminal session via PipeInput.
    """
    yield lambda *x: mock_input.send_text(key_converter(*x))


class FakeTerminalSize(NamedTuple):
    columns: int
    lines: int


@pytest.fixture(autouse=True)
def mock_terminal_size(monkeypatch: pytest.MonkeyPatch):

    def get_fake_terminal_size(x=None):
        """
        Fixture for mocking the output of the `os.get_terminal_size()` method

        This fixture is needed in order for `TablePrompt()` to work.
        """
        return FakeTerminalSize(180, 60)

    monkeypatch.setattr(os, "get_terminal_size", get_fake_terminal_size)
