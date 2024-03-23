Options and Data in ItsPrompt
=============================

`ItsPrompt` has a number of ways to display and check options and data.

Option Parameter
----------------

The `option` parameter is always a :class:`tuple` with the type annotation :const:`~ItsPrompt.objects.prompts.type.OptionsList`. 

Option as a String
~~~~~~~~~~~~~~~~~~

Options can be given as a :class:`str`. In this case, the string is displayed as the option and returned as the 
selected option, if the user selects it.

.. note:: In case of :meth:`~ItsPrompt.prompt.Prompt.expand()`, the first character of the :class:`str` will be used as the key.

Options as a Tuple of OptionWithId
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Options can be given as a :class:`tuple` with the type annotation :const:`~ItsPrompt.objects.prompts.type.OptionWithId`.

For all prompts excluding :meth:`~ItsPrompt.prompt.Prompt.expand`, the tuple is structured as follows

- The first element is the displayed option
- The second element is the id of the option

For the :meth:`~ItsPrompt.prompt.Prompt.expand` prompt, the tuple is structured as follows:

- The first element is the key of the option
- The second element is the displayed option
- The third element is the id of the option

Separators
~~~~~~~~~~

Options can be separated using a :class:`~ItsPrompt.objects.prompts.type.Separator`. A Separator name can be given using
the `label` parameter.

Separators are available in the prompt types:

- :meth:`~ItsPrompt.prompt.Prompt.select`
- :meth:`~ItsPrompt.prompt.Prompt.raw_select`
- :meth:`~ItsPrompt.prompt.Prompt.checkbox`
- :meth:`~ItsPrompt.prompt.Prompt.expand`

.. note:: The separator cannot be selected as an option. It is purely for cosmetic purposes.

Example:

.. code-block:: python

    from ItsPrompt.prompt import Prompt
    from ItsPrompt.objects.prompts.separator import Separator
    
    ans = Prompt.select(
        'What food would you like?',
        (Separator('The veggies'), 'Salad', Separator('The meaties'), 'Pizza', 'Burger'),
        default='Pizza',
    )

Data Parameter
--------------

The :meth:`~ItsPrompt.prompt.Prompt.table` prompt has a `data` parameter instead of the `option` parameter. The `data`
parameter has to be one of the following types:

- a :class:`~ItsPrompt.objects.prompts.type.TablePromptList`
- a :class:`~ItsPrompt.objects.prompts.type.TablePromptDict`
- a :class:`pandas.DataFrame`

.. note:: The type :class:`pandas.DataFrame` is only available if the `pandas` library is installed.

The `data` is used as the content of the table. The user may change the fields of the table. The output of the `table`
prompt is of the same type, as the input data is represented, with the user given values.

.. note::

    Currently, all fields are represented as strings and every field is editable by the user. This may be changed
    in the future.

Data as a TablePromptList
~~~~~~~~~~~~~~~~~~~~~~~~~

A :class:`~ItsPrompt.objects.prompts.type.TablePromptList` is a :class:`list` of :class:`list` with each cell
represented by a :class:`str`.

Every sub-list represents a column in the table.

.. code-block:: python

    data = [
        ["field 1", "field 2"], 
        ["field 3", "field 4"]
    ]

will be rendered:

+---------+---------+
| 0       | 1       |
+=========+=========+
| field 1 | field 3 |
+---------+---------+
| field 2 | field 4 |
+---------+---------+

Data as a TablePromptDict
~~~~~~~~~~~~~~~~~~~~~~~~~

A :class:`~ItsPrompt.objects.prompts.type.TablePromptDict` is a :class:`dict` with the keys as the column names and the
values as a :class:`list` of :class:`str`, where each :class:`list` represents a column in the table.

.. code-block:: python

    data = {
        "column 1": ["field 1", "field 2"], 
        "column 2": ["field 3", "field 4"]
    }

+----------+----------+
| column 1 | column 2 |
+==========+==========+
| field 1  | field 3  |
+----------+----------+
| field 2  | field 4  |
+----------+----------+

Data as a DataFrame
~~~~~~~~~~~~~~~~~~~

A :class:`pandas.DataFrame` can be used as well. Read more about them in the `pandas documentation <https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html>`_.

.. code-block:: python

    DataFrame(["field 1", "field 2"])

+---------+
| 0       |
+=========+
| field 1 |
+---------+
| field 2 |
+---------+

.. note::

    Currently, the `table` prompt cannot display styling in the `DataFrame` fields. All styling tags will be displayed
    as-is, so a `<u>...</u>` will not be underlined, but rather displayed as its shown.

Input Prompt Parameters
-----------------------

The :meth:`~ItsPrompt.prompt.Prompt.input` prompt has many options to check and complete the input. The following parameters are available:

- `default`: The default value of the input. If the user does not enter anything, the default value is returned.
- `multiline`: If set to :const:`True`, the user can enter multiple lines of text.
- `show_symbol`: Can be set to a :class:`str` to show this symbol instead of the characters entered by the user. 
  This is useful for password prompts.
- `validate`: A function that validates the input. Read more about this in the :ref:`validation` section.
- `completions`: A list of completions that the user can select from. Read more about this in the :ref:`completions` section.
- `completer`: A function that returns a list of completions. Read more about this in the :ref:`completions` section.

.. note::

   Only the `validate`, `completions`, and `completer` parameters are described here in detail. The other parameters can
   be found in the :meth:`~ItsPrompt.prompt.Prompt.input` API documentation.

.. _validation:

Prompt Validation
~~~~~~~~~~~~~~~~~

The `validate` parameter can be used to validate the input. For every character entered by the user, the `validate`
function is called with the current input as a :class:`str`. The function should return either

- a :class:`str` to show the string as an error message
- :const:`False` to show a default error message
- :const:`None` (or :const:`True`) to accept the input

.. code-block:: python

    # define a validation function
    def input_not_empty(input: str) -> str | None:
        if len(input) == 0:
            return 'Address can not be empty!'
    
    
    # using a function
    Prompt.input(
        ...,
        validate=input_not_empty,
        ...,
    )
    
    # using lambda
    Prompt.input(
        ...,
        validate=lambda x: "test" in x,
        ...,
    )
    
The :class:`str` given to the function is the current input of the user. It cannot be changed.

If you want to show that the validation succeeded, return :const:`None` (or nothing, or :const:`True`). This will not
trigger any errors.

If you want to show an error, return a :class:`str` with the errors text or :const:`False`. If you return a 
:class:`str`, your text will be shown in the toolbar. If you return :const:`False`, a general error message will be 
shown. As long as the validation returns a :class:`str` or :const:`False`, the user may not submit the input.

.. _completions:

Prompt Completion
~~~~~~~~~~~~~~~~~

The `completions` and `completer` parameters can be used to give the user a list of completions to choose from.

.. note:: If you use `completions` or `completer`, you are unable to use `show_symbol`.

.. note:: `completions` and `completer` are **mutually exclusive**!. You may only use one of them at a time.

There are three ways to give completions to the user:

- A :class:`list` of :class:`str` (read more about this in the :ref:`completions_as_a_list` section)
- A nested :class:`dict` (read more about this in the :ref:`completions_as_a_dict` section)
- A :class:`~prompt_toolkit.completion.Completer` given by `prompt_toolkit` (read more about this in the 
  :ref:`completions_as_a_completer` section)

.. _completions_as_a_list:

Completions as a List
*********************

:meth:`~ItsPrompt.prompt.Prompt.input` takes a :class:`list[str]` to use as simple word completions. Each :class:`str` in the list is a possible value to complete.

.. code-block:: python

    prompt.input(
        ...,
        completions=['Mainstreet 4', 'Fifth way'],
        ...,
    )

.. _completions_as_a_dict:

Completions as a Dict
*********************

You can use a :class:`dict` for nested completions. Each "layer" will be a completion, after the first was accepted. The
type annotation for the :class:`dict` can be found here: :const:`~ItsPrompt.objects.prompts.type.CompletionDict`.

Example:

.. code-block:: python

    completions = {
        '1': {
            '1.1': None,
            '1.2': {
                '1.2.1', '1.2.2'
            }
        },
        '2': {
            '2.1': {'2.1.1'}
        }
    }
    
    prompt.input(
        ...,
        completions=completions,
        ...,
    )
    
In this example, the user can select `1` or `2` as the first completion. If the user selects `1`, they can select `1.1`
or `1.2`, then `1.2.1` and so on.

The key of each entry is the completion that will be shown. The key is either :const:`None` if there are no further 
completions or a new :class:`dict`, where the key is the completion and the value is the next "layer", and so on.

.. _completions_as_a_completer:

Completions as a Completer
**************************

In the background your completions will be mapped to a :class:`~prompt_toolkit.completion.Completer`, provided by 
`prompt_toolkit`.

If you need more customization, you can use a :class:`~prompt_toolkit.completion.Completer` given by `prompt-toolkit` or
create your own completer. For more information on this process, read here: 
`Completions in prompt-toolkit <https://python-prompt-toolkit.readthedocs.io/en/stable/pages/asking_for_input.html#autocompletion>`_.

There are a number of completers available, for example:

- :class:`~prompt_toolkit.completion.PathCompleter`
    - automatically complete file system paths
- :class:`~prompt_toolkit.completion.ExecutableCompleter`
    - automatically complete executables in a file system
- :class:`~prompt_toolkit.completion.WordCompleter`
    - As simple as it can get. Just completes the letters of the word, that are actually present (the `FuzzyCompleter`
      which `completions` uses in background completes based on a probability, and may show matches which are not
      exact).
- ...

To add your own completer to an :meth:`~ItsPrompt.prompt.Prompt.input` field, you can use the `completer` parameter:

.. code-block:: python

    prompt.input(
        ...,
        completer=my_completer,
        ...,
    )

.. note:: `completions` and `completer` are **mutually exclusive**!. You may only use one of them at a time.
