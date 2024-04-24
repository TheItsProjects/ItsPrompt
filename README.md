[![PyPI version](https://badge.fury.io/py/ItsPrompt.svg)](https://badge.fury.io/py/ItsPrompt)
[![linting](https://github.com/TheItsProjects/ItsPrompt/actions/workflows/lint.yml/badge.svg)](https://github.com/TheItsProjects/ItsPrompt/actions/workflows/lint.yml)
[![Tests](https://github.com/TheItsProjects/ItsPrompt/actions/workflows/tests.yml/badge.svg)](https://github.com/TheItsProjects/ItsPrompt/actions/workflows/tests.yml)

[![PyPI - Downloads](https://img.shields.io/pypi/dm/ItsPrompt)](https://pypi.org/project/ItsPrompt/)
[![GitHub issues](https://img.shields.io/github/issues/TheItsProjects/ItsPrompt)](https://github.com/TheItsProjects/ItsPrompt/issues)
[![GitHub Repo stars](https://img.shields.io/github/stars/TheItsProjects/ItsPrompt)](https://github.com/TheItsProjects/ItsPrompt/stargazers)
[![GitHub](https://img.shields.io/github/license/TheitsProjects/ItsPrompt)](https://github.com/TheItsProjects/ItsPrompt/blob/main/LICENSE)
[![Discord](https://img.shields.io/discord/1082381448624996514)](https://discord.gg/rP9Qke2jDs)

[![Read the Docs](https://img.shields.io/readthedocs/itsprompt)](http://itsprompt.readthedocs.io/)

![Demonstration](https://raw.githubusercontent.com/TheItsProjects/ItsPrompt/main/docs/source/media/ItsPrompt.gif)

# ItsPrompt

Do you ever feel the need to ask a user of your code for an input?

Using `input()` is easy, but is it great?

Do you want to give the user a selection list, a yes-or-no question, or maybe a multiline input field?

And do you think all of this should be done easily, without caring to much how it all works?

Then you are right here! **ItsPrompt** allows you to ask the user for input, the *fancy* way.

**ItsPrompt** tries to be an easy-to-use module for managing prompts for the user. Your task is to create a great
program, not finding yourself questioning how to ask the user for input. That is why **ItsPrompt** is there to take care
of this problem, so you can focus on the important things!

## TOC

<!-- TOC -->
* [ItsPrompt](#itsprompt)
  * [TOC](#toc)
    * [A small, thankful note](#a-small-thankful-note)
  * [Features](#features)
  * [Installation](#installation)
  * [Quick Example](#quick-example)
  * [Usage](#usage)
  * [Further Information](#further-information)
<!-- TOC -->

---

### A small, thankful note

This project is not the first to accomplish the above-mentioned tasks. There is another package, `PyInquirer`, which
inspired me to build **ItsPrompt**.

On my way to create a small program I came to a point were I needed a simple GUI, and I tried `PyInquirer`.
Unfortunately, at the current time it is not actively maintained and a bit outdated. I thought of updating it, but then
I thought "*Isn't it easier to just create my own version?*" - And so I did!

**ItsPrompt** is not a copy or a fork of `PyInquirer`. I built this module from the ground up, without ever looking deep
into the source code of `PyInquirer`.

On my way to build this package, I learned a lot about `prompt-toolkit`, and all of this just because of `PyInquirer`!
Thanks!

---

## Features

- many prompt types:
    - select
    - raw_select
    - expand
    - checkbox
    - confirm
    - input
    - table
- prompt autocompletion and validation
- customizable style with `prompt_toolkit`
- a helpful toolbar with error messages
- simple, pythonic syntax

---

## Installation

This package is hosted on pypi, so the installation is as simple as it can get:

```bash
python3 -m pip install ItsPrompt
```

This will install `ItsPrompt` without pandas. If you want to use `TablePrompt`
(see [table](https://itsprompt.readthedocs.io/en/latest/guide/prompt_types.html#table)) with
`pandas.DataFrame`, you can install pandas support either by:

- installing pandas separately
- install `ItsPrompt` via `pip install ItsPrompt[df]`

---

## Quick Example

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

## Usage

To learn more about the usage, visit our [documentation](https://itsprompt.readthedocs.io).

---

## Further Information

Visit our [documentation](https://itsprompt.readthedocs.io/) to learn more about the usage of **ItsPrompt**!

If you need some easy examples, refer to [example.py](example.py)!

If you want to contribute, check out the projects repository: [ItsPrompt](https://github.com/TheItsProjects/ItsPrompt)!

If you got any other questions, or want to give an idea on how to improve **ItsPrompt**:

- visit our discussions: [ItsPrompt Discussions](https://github.com/TheItsProjects/ItsPrompt/discussions)!
- join our discord: [TheItsProjects](https://discord.gg/rP9Qke2jDs)!

---

Puh, that was so much to read... But now, lets have fun with **ItsPrompt**!
