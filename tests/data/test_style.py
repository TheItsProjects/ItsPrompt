from ItsPrompt.data.style import create_from_default, default_style


def test_create_from_default():
    style = create_from_default()

    assert style == default_style
