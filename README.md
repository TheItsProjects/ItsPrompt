[![PyPI version](https://badge.fury.io/py/ItsPrompt.svg)](https://badge.fury.io/py/ItsPrompt)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/ItsPrompt)](https://pypi.org/project/ItsPrompt/)
[![GitHub issues](https://img.shields.io/github/issues/TheItsProjects/ItsPrompt)](https://github.com/TheItsProjects/ItsPrompt/issues)
[![GitHub Repo stars](https://img.shields.io/github/stars/TheItsProjects/ItsPrompt)](https://github.com/TheItsProjects/ItsPrompt/stargazers)
[![GitHub](https://img.shields.io/github/license/TheitsProjects/ItsPrompt)](https://github.com/TheItsProjects/ItsPrompt/blob/main/LICENSE)
[![Discord](https://img.shields.io/discord/1082381448624996514)](https://discord.gg/rP9Qke2jDs)

![Demonstration](https://raw.githubusercontent.com/TheItsProjects/ItsPrompt/main/media/ItsPrompt.gif)

# ItsPrompt

Do you ever feel the need to ask a user of your code for an input?

Using `input()` is easy, but is it great? 

Do you want to give the user a selection list, a yes-or-no question, or maybe a multiline input field?

And do you think all of this should be done easily, without caring to much how it all works?

Then you are right here! **ItsPrompt** gives you the ability to ask the user for input, the *fancy* way.

**ItsPrompt** tries to be an easy-to-use module for managing prompts for the user. You task is to create a great program, not how to ask the user for input. That is why **ItsPrompt** is there to take care of this problem, so you can focus on the important things!

# TOC

- [ItsPrompt](#itsprompt)
- [TOC](#toc)
    - [A small, thankful note](#a-small-thankful-note)
  - [Features](#features)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Prompt types](#prompt-types)
    - [`select`](#select)
    - [`raw_select`](#raw_select)
    - [`expand`](#expand)
    - [`checkbox`](#checkbox)
    - [`confirm`](#confirm)
    - [`input`](#input)
    - [`table`](#table)
  - [Additional Features and Tips](#additional-features-and-tips)
    - [Options](#options)
    - [Data](#data)
    - [Styling](#styling)
    - [Prompt Validation](#prompt-validation)
    - [Prompt Completion](#prompt-completion)
    - [Further Information](#further-information)

---

### A small, thankful note

This project is not the first to accomplish the above mentioned tasks. There is another package, `PyInquirer`, which inspired me to build **ItsPrompt**.

On my way to create a small program I came to a point were I needed a simple GUI, and I tried `PyInquirer`. Unfortunately, at the current time it is not actively maintained and a bit outdated. I thought of updating it, but then I thought "*Isn't it easier to just create my own version?*" - And so I did!

**ItsPrompt** is not a copy or a fork of `PyInquirer`. I built this module from the ground up, without ever looking deep into the source code of `PyInquirer`.

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
    - table
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

![](https://raw.githubusercontent.com/TheItsProjects/ItsPrompt/main/media/select.png)

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

![](https://raw.githubusercontent.com/TheItsProjects/ItsPrompt/main/media/raw_select.png)

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

![](https://raw.githubusercontent.com/TheItsProjects/ItsPrompt/main/media/expand.png)

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

![](https://raw.githubusercontent.com/TheItsProjects/ItsPrompt/main/media/checkbox.png)

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

![](https://raw.githubusercontent.com/TheItsProjects/ItsPrompt/main/media/confirm.png)

```py
Prompt.confirm(
    question='question',
    default=False,
    style=my_style,
)
```

*additional information on the function arguments can be found in the docstring*

### `input`

![](https://raw.githubusercontent.com/TheItsProjects/ItsPrompt/main/media/input.png)

```py
Prompt.input(
    question='question',
    default='something',
    multiline=False,
    show_symbol='*', # not compatible with complete, completer
    validate=validation_function,
    complete=['completion1', 'completion2'], # either use complete
    completer=my_completer,                  # or completer
    completion_show_multicolumn=True,
    style=my_style,
)
```

*additional information on the function arguments can be found in the docstring*

### `table`

![](https://raw.githubusercontent.com/TheItsProjects/ItsPrompt/main/media/table.png)

```py
Prompt.table(
    question='something',
    data=DataFrame(['something']),
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

### Data

The `table` prompt takes a mandatory `data` argument, which needs to be a `pandas.DataFrame`.

This `DataFrame` is used as the content of the table. The user may change the fields of the table. The output of the `table` prompt is a `pandas.DataFrame` with the user given values.

Currently, the output will convert all input values to a `str`, so `int`, `bool`, ... will be converted to strings. This is a current limitation of the way the table is displayed, but may later be updated.

Another limitation of the `table` prompt is the use of styling in the `DataFrame` fields. All styling tags will be displayed as-is, so a `<u>...</u>` will not be underlined, but rather displayed as its shown.

---

### Styling

**ItsPrompt** uses `prompt-toolkit` for its prompts. This module not only provides an easy way to interact with the command line, but also a full set of styling features.

You can learn more about the available styling features in the documentation of `prompt-toolkit`: [Styling](https://python-prompt-toolkit.readthedocs.io/en/master/pages/printing_text.html#formatted-text).

**ItsPrompt** makes it a bit easier for you to style each component of a prompt. For every component, we give a separate attribute in the `PromptStyle` class, which you can style with valid `prompt-toolkit` styling:

```py
# examples for the different styling class components
Prompt.raw_select(
    question='question',
    options=(
        'option',
        'selected_option',
    )
)

Prompt.input(
    question='question',
    default='grayout',
    validate=lambda x: 'error',
)
```

![](https://raw.githubusercontent.com/TheItsProjects/ItsPrompt/main/media/styling_raw_select_annotated.png)

![](https://raw.githubusercontent.com/TheItsProjects/ItsPrompt/main/media/styling_input_annotated.png)

| ID  |    styling tag    |             default style             |
| --- | ----------------- | ------------------------------------- |
| 1   | `question_mark`   | `fg:ansigreen`                        |
| 2   | `question`        | *                                     |
| 3   | `option`          | *                                     |
| 4   | `selected_option` | `fg:ansicyan`                         |
| 5   | `tooltip`         | `fg:ansibrightblue bg:ansiwhite bold` |
| 6   | `text`            | *                                     |
| 7   | `grayout`          | `fg:ansibrightblack`                  |
| 8   | `error`           | `fg:ansiwhite bg:ansired bold`        |

*\*These values are not changed from the default `prompt-toolkit` values.*


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

All styles which are not given, **will not** be the same as the default style. Instead they will use the styling given by `prompt-toolkit`. If you want to change our default styles, then copy the `default_style` and change your values, instead of directly creating your own style:

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

### Prompt Completion

The `input` prompt type supports auto completion as well. 

> If you use a completer, you are unable to use `show_symbol`!

To give auto completion options, there are three ways:

***Creating a simple list of possible completions***

`Input` takes a `list[str]` to use as simple word completions. Each `str` in the list is a possible value to complete.

```py
prompt.input(
    ...
    completions=['Mainstreet 4', 'Fifth way'],
    ...
)
```

***Creating a nested dictionary of possible completions***

You can use a dictionary for nested completions. Each "layer" will be a completion, after the first was accepted. For example:

```py
completions = {
    '1' : {
        '1.1' : None,
        '1.2' : {
            '1.2.1', '1.2.2'
        }
    },
    '2' : {
        '2.1' : { '2.1.1' }
    }
}

prompt.input(
    ...
    completions=completions,
    ...
)
```

The key of each entry is the completion that will be shown. The key is either None if there are no further completions or a new dict, where the key is the completion and the value is the next "layer", and so on...

> For more information, the type signature of `CompletionDict` is:  
> `dict[str, "CompletionDict | None"]`

***Using a given Completer by `prompt-toolkit` or creating your own***

In the background your completions will be mapped to a `Completer`, provided by `prompt-toolkit`.

If you need more customization, you can use a `Completer` given by `prompt-toolkit` or create your own completer. For more information on this process, read here: [Completions in prompt-toolkit](https://python-prompt-toolkit.readthedocs.io/en/stable/pages/asking_for_input.html#autocompletion).

There are a number of completers available, for example:

- `PathCompleter`
    - automatically complete file system paths
- `ExecutableCompleter`
    - automatically complete executables in file system
- `WordCompleter`
    - As simple as it can get. Just completes the letters of the word, that are actually present (the `FuzzyCompleter` which `completions` uses in background completes based on a probability, and may show matches which are not exact).
- ...


To add your own completer to an input field, you can use the `completer` argument:

```py
prompt.input(
    ...
    completer=my_completer,
    ...
)
```

> `completions` and `completer` are **mutually exclusive**! You may not use both!

---

### Further Information

If you need some easy examples, refer to [example.py](example.py)!

If you want to contribute, check out the projects repository: [ItsPrompt](https://github.com/TheItsProjects/ItsPrompt)!

If you got any other questions, or want to give an idea on how to improve **ItsPrompt**:
- visit our discussions: [ItsPrompt Discussions](https://github.com/TheItsProjects/ItsPrompt/discussions)!
- join our discord: [TheItsProjects](https://discord.gg/rP9Qke2jDs)!

---

Puh, that was so much to read... But now, lets have fun with **ItsPrompt**!
