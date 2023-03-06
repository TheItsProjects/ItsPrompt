PyPI version
![PyPI - Downloads](https://img.shields.io/pypi/dm/ItsPrompt)
![GitHub issues](https://img.shields.io/github/issues/TheItsProjects/ItsPrompt)
![GitHub Repo stars](https://img.shields.io/github/stars/TheItsProjects/ItsPrompt)
![GitHub](https://img.shields.io/github/license/TheitsProjects/ItsPrompt)

# ItsPrompt

Do you ever feel the need to ask a user of your code for an input?

Using `input()` is easy, but is it great? 

Do you want to give the user a selection list, a yes-or-no question, or maybe a multiline input field?

And do you think all of this should be done easily, without carring to much how it all works?

Then you are right here! **ItsPrompt** gives you the ability to ask the user for input, the *fancy* way.

**ItsPrompt** tries to be an easy-to-use module for managing prompts for the user. You task is to create a great program, not how to ask the user for input. That is why **ItsPrompt** is there to take care of this problem, so you can focus on the important things!

---

### A small, thankfull note

This project is not the first to accomplish the above mentioned tasks. There is another package, `PyInquirer`, which inspired me to build **ItsPrompt**.

On my way to create a small program I came to a point were I needed a simple GUI, and I tried `PyInquirer`. Unfortunately, at the current time it is not actively maintained and a bit outdated. I thought of updating it, but then I thought "*Isn't it easier to just create my own version?*" - And so I did!

**ItsPrompt** is not a copy or a fork of `PyInquirer`. I built this module from the ground up, without every looking deep into the source code of `PyInquirer`.

On my way to build this package, I learned a lot about `prompt-toolkit`, and all of this just because of `PyInquirer`! Thanks!

---

## Features

- many prompt types (more details below):
    - select
    - raw_select
    - expand
    - checkbox
    - confirm
    - input
- big feature set
- simple, pythonic syntax
- a helpful toolbar with error messages
- customizable style with `prompt-toolkit`

---

## Installation

This package is hosted on pypi, so the installation is as simple as it can get:

```
python3 -m pip install ItsPrompt
```

---

## Usage

Import the `Prompt` class:

```py
from ItsPrompt.prompt import Prompt
```

Now you can ask the user any type of prompt by calling the specific function from the `Prompt` class, e.g.:

```py
result = Prompt.input('What is your name?')
print(result)
```

You see how easy it is?

---

## Prompt types

As mentioned above, **ItsPrompt** has multiple prompt types. All of them can be accessed via the `Prompt` class.

### `select`

![](/media/select.png)

```py
Prompt.select(
    question='question',
    options=('option1', ('option2', 'opt2')),
    default='option1',
    style=my_style,
)
```

*additional information on the function arguments can be found in the docstring*


### `raw_select`

![](/media/raw_select.png)

```py
Prompt.raw_select(
    question='question',
    options=('option1', ('option2', 'opt2')),
    default='opt2',
    allow_keyboard=True,
    style=my_style,
)
```

*additional information on the function arguments can be found in the docstring*

### `expand`

![](/media/expand.png)

```py
Prompt.expand(
    question='question',
    options=('option1', ('2', 'option2', 'opt2')),
    default='opt2',
    allow_keyboard=True,
    style=my_style,
)
```

*additional information on the function arguments can be found in the docstring*

### `checkbox`

![](/media/checkbox.png)

```py
Prompt.checkbox(
    question='question',
    options=('option1', ('option2', 'opt2')),
    pointer_at=1,
    default_checked='option1',
    min_selections=1,
    style=my_style,
)
```

*additional information on the function arguments can be found in the docstring*

### `confirm`

![](/media/confirm.png)

```py
Prompt.confirm(
    question='question',
    default=False,
    style=my_style,
)
```

*additional information on the function arguments can be found in the docstring*

### `input`

![](/media/input.png)

```py
Prompt.input(
    question='question',
    default='something',
    multiline=False,
    show_symbol='*',
    validate=validation_function,
    style=my_style,
)
```

*additional information on the function arguments can be found in the docstring*

---

## Additional Features and Tips

### Options

The `options` is always a `tuple` containing `str` and `tuple` objects. 

If an option is given as a `str`, this will be used as the options display name and the id, which will be returned when selecting this option.

*In case of `expand`, the first character of the `str` will be used as its key.*

If an option is given as a `tuple`, the first value will be the options name, the second value the options id to return.

*In case of `expand`, the first value will be the key, the second value the name and the third value the id.*

---

### Styling

**ItsPrompt** uses `prompt-toolkit` for its prompts. This module not only provides an easy way to interact with the command line, but also a full set of styling features.

To create your own style, there are two ways:

***Changing the default style***

To change the default style, you need to import the `default_style` and change its values:

```py
from ItsPrompt.data.style import default_style

default_style.error = 'fg:ansired bg:ansiwhite'
```

This will automatically change the style of all prompts, which do not have an own style defined.

***Creating your own style***

To define your own style for a specific prompt, import `PromptStyle` and create an object. Then assign it to the `style` argument of a prompt.

```py
from ItsPrompt.data.style import PromptStyle

my_style = PromptStyle(
    question_mark='fg:ansiblue',
    error='fg:ansired bg:ansiwhite',
)
```

All styles which are not given, **will not** be the same as the default style. If you want this to be the case, then copy the `default_style` and change your values, instead of directly creating your own style:

```py
from ItsPrompt.data.style import create_from_default

my_style = create_from_default()

my_style.error = 'fg:ansired bg:ansiwhite'
```

> Warning! Not copying the default style and changing it instead will result in all prompts using your changes, as a variable is by default not a copy, but a reference to the same object!

---

### Prompt Validation

The `input` allows you to validate the input before submitting it. For every character the user types, the validation will be run and a friendly error will be shown in the toolbar.

To use the validation feature, create a function which takes a `str` as an argument and returns either a `str` or `None`.

```py
def input_not_empty(input: str) -> str | None:
    if len(input) == 0:
        return 'Address can not be empty!'

Prompt.input(
    ...
    validate=input_not_empty,
    ...
)
```

The `str` argument will be the current user input, which can then be checked, but not changed!

If you want to show that the validation succeeded, return `None` (or nothing). This will not trigger any errors.

If you want to show an error, return a `str` with the errors text. Your text will be shown in the toolbar. As long as the validation returns a `str`, the user may not submit the input.

---

### Further Information

If you need some easy examples, refer to [example.py](example.py)!

If you want to contribute, check out the projects repository: [ItsPrompt](https://github.com/TheItsProjects/ItsPrompt)!

If you got any other questions, or want to give an idea on how to improve **ItsPrompt**, join our discord: [TheItsProjects](https://discord.gg/rP9Qke2jDs)!

---

Puh, that was so much to read... But now, lets have fun with **ItsPrompt**!
