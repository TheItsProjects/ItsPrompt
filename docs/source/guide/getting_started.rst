Getting Started with ItsPrompt
==============================

What is ItsPrompt?
------------------

**ItsPrompt** is a Python package that simplifies user interaction in command-line interfaces. It offers a variety of 
prompt types, including:

- `select`
- `raw_select`
- `expand`
- `checkbox`
- `confirm`
- `input`
- `table`

Each prompt type provides a unique way of gathering user input. The package is designed with simplicity in mind, 
offering a straightforward, Pythonic syntax. It also provides a range of customization options, allowing you to style 
prompts and validate user input. 

ItsPrompt is built on top of the `prompt-toolkit` library, leveraging its capabilities for prompt creation and styling. 
This makes it an excellent tool for developers who want to create interactive command-line applications without having 
to worry about the intricacies of user input and command-line rendering.

Installation
------------

This package is hosted on pypi, so the installation is as simple as it can get:

.. code-block:: bash

    python3 -m pip install ItsPrompt


This will install `ItsPrompt` without pandas. If you want to use `TablePrompt` (see :ref:`prompt_types_table`) with
`pandas.DataFrame`, you can install pandas support either by:

- installing pandas separately
- install `ItsPrompt` via ``pip install ItsPrompt[df]``

Basic Usage
-----------

Import the `Prompt` class:

.. code-block:: python

    >>> from ItsPrompt.prompt import Prompt

Now you can ask the user any type of prompt by calling the specific function from the `Prompt` class, e.g.:

.. code-block:: python

    >>> result = Prompt.input('What is your name?')
    [?] What is your name?: ItsNameless
    >>> print(f"Hello {result}!")
    Hello ItsNameless!

You see how easy it is?

To learn more about the usage of ItsPrompt, check out :doc:`usage`.
