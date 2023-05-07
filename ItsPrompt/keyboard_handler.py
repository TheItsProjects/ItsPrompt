from prompt_toolkit import Application
from prompt_toolkit.key_binding import KeyBindings, KeyPressEvent


def generate_key_bindings(app: type[Application]) -> KeyBindings:
    '''
    Generates a KeyBindings object for use in a Prompt class

    The `app` is used to check whether specific functions for handling the key events exist. It has to be a Prompt object (e.g. InputPrompt).
    
    The available functions are:
    
    `on_up()`
    
    `on_down()`
    
    `on_left()`
    
    `on_right()`
    
    `on_enter()`
    
    `on_space()`
    
    `on_alt_enter()`
    
    `on_backspace()`
    
    `on_ctrl_backspace()`
    
    `on_key()`

    :param app: An application type to check whether one of the above functions exists
    :type app: type[Application]
    :return: An usable KeyBindings instance
    :rtype: KeyBindings
    '''

    kb = KeyBindings()

    # Each of the options gets the keyboard input and runs the equivalent function in the event.app class, if the function exists.

    @kb.add('c-c')
    def quit(event: KeyPressEvent):
        event.app.exit()

    @kb.add('up', filter=hasattr(app, 'on_up'))
    def up(event: KeyPressEvent):
        event.app.on_up()  # type: ignore

    @kb.add('down', filter=hasattr(app, 'on_down'))
    def down(event: KeyPressEvent):
        event.app.on_down()  # type: ignore

    @kb.add('left', filter=hasattr(app, 'on_left'))
    def left(event: KeyPressEvent):
        event.app.on_left()  # type: ignore

    @kb.add('right', filter=hasattr(app, 'on_right'))
    def right(event: KeyPressEvent):
        event.app.on_right()  # type: ignore

    @kb.add('enter', filter=hasattr(app, 'on_enter'))
    def enter(event: KeyPressEvent):
        event.app.on_enter()  # type: ignore

    @kb.add('space', filter=hasattr(app, 'on_space'))
    def space(event: KeyPressEvent):
        event.app.on_space()  # type: ignore

    @kb.add('escape', 'enter', filter=hasattr(app, 'on_alt_enter'))
    def alt_enter(event: KeyPressEvent):
        event.app.on_alt_enter()  # type: ignore

    # backspace is mapped to ctrl-h
    @kb.add('c-h', filter=hasattr(app, 'on_backspace'))
    def backspace(event: KeyPressEvent):
        event.app.on_backspace()  # type: ignore

    # ctrl-backspace is mapped to ctrl-w
    @kb.add('c-w', filter=hasattr(app, 'on_ctrl_backspace'))
    def ctrl_backspace(event: KeyPressEvent):
        event.app.on_ctrl_backspace()  # type: ignore

    @kb.add('<any>', filter=hasattr(app, 'on_key'))
    def wildcard(event: KeyPressEvent):
        # wildcard function, used for prompts which need standard key presses like numbers or characters
        event.app.on_key(  # type: ignore
            [key.key for key in event.key_sequence], )

    return kb
