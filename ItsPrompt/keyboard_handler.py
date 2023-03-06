from prompt_toolkit.key_binding import KeyBindings, KeyPressEvent

kb = KeyBindings()

# Each of the options gets the keyboard input and runs the equivalent function in the event.app class, if the function exists.


@kb.add('c-c')
def quit(event: KeyPressEvent):
    event.app.exit()


@kb.add('up')
def up(event: KeyPressEvent):
    if hasattr(event.app, 'on_up'):
        event.app.on_up()  # type: ignore


@kb.add('down')
def down(event: KeyPressEvent):
    if hasattr(event.app, 'on_down'):
        event.app.on_down()  # type: ignore


@kb.add('enter')
def enter(event: KeyPressEvent):
    if hasattr(event.app, 'on_enter'):
        event.app.on_enter()  # type: ignore


@kb.add('space')
def space(event: KeyPressEvent):
    if hasattr(event.app, 'on_space'):
        event.app.on_space()  # type: ignore


@kb.add('escape', 'enter')
def alt_enter(event: KeyPressEvent):
    if hasattr(event.app, 'on_alt_enter'):
        event.app.on_alt_enter()  # type: ignore


# backspace is mapped to ctrl-h
@kb.add('c-h')
def backspace(event: KeyPressEvent):
    if hasattr(event.app, 'on_backspace'):
        event.app.on_backspace()  # type: ignore


# ctrl-backspace is mapped to ctrl-w
@kb.add('c-w')
def ctrl_backspace(event: KeyPressEvent):
    if hasattr(event.app, 'on_ctrl_backspace'):
        event.app.on_ctrl_backspace()  # type: ignore


@kb.add('<any>')
def wildcard(event: KeyPressEvent):
    # wildcard function, used for prompts which need standard key presses like numbers or characters
    if hasattr(event.app, 'on_key'):
        event.app.on_key(  # type: ignore
            [key.key for key in event.key_sequence], )
