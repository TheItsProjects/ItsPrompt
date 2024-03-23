Prompt Styling
==============

`ItsPrompt` uses `prompt_toolkit` for its prompts. This module not only provides an easy way to interact with the
command line, but also a full set of styling features.

You can learn more about the available styling features in the 
`Styling Documentation <https://python-prompt-toolkit.readthedocs.io/en/master/pages/printing_text.html#formatted-text>`_ 
of `prompt_toolkit`.

`ItsPrompt` makes it a bit easier for you to style each component of a prompt. For every component, we give a separate
attribute in the `PromptStyle` class, which you can style with valid `prompt_toolkit` styling:

.. code-block:: python
    
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

.. image:: https://raw.githubusercontent.com/TheItsProjects/ItsPrompt/main/media/styling_raw_select.png

.. image:: https://raw.githubusercontent.com/TheItsProjects/ItsPrompt/main/media/styling_input.png

+-------------------+---------------------------------------+-------------------------------------------------+
| styling tag       | default style                         | default design                                  |
+===================+=======================================+=================================================+
| `question_mark`   | `fg:ansigreen`                        | .. image:: ../media/styling/question_mark.png   |
+-------------------+---------------------------------------+-------------------------------------------------+
| `question`        | **\***                                | .. image:: ../media/styling/question.png        |
+-------------------+---------------------------------------+-------------------------------------------------+
| `option`          | **\***                                | .. image:: ../media/styling/option.png          |
+-------------------+---------------------------------------+-------------------------------------------------+
| `selected_option` | `fg:ansicyan`                         | .. image:: ../media/styling/selected_option.png |
+-------------------+---------------------------------------+-------------------------------------------------+
| `tooltip`         | `fg:ansibrightblue bg:ansiwhite bold` | .. image:: ../media/styling/tooltip.png         |
+-------------------+---------------------------------------+-------------------------------------------------+
| `text`            | **\***                                | .. image:: ../media/styling/text.png            |
+-------------------+---------------------------------------+-------------------------------------------------+
| `grayout`         | `fg:ansibrightblack`                  | .. image:: ../media/styling/grayout.png         |
+-------------------+---------------------------------------+-------------------------------------------------+
| `error`           | `fg:ansiwhite bg:ansired bold`        | .. image:: ../media/styling/error.png           |
+-------------------+---------------------------------------+-------------------------------------------------+
| `separator`       | `fg:ansibrightgreen`                  | .. image:: ../media/styling/separator.png       |
+-------------------+---------------------------------------+-------------------------------------------------+

.. note:: **\***\ These values are not changed from the default `prompt_toolkit` values.


To create your own style, there are two ways:

Changing the Default Style
--------------------------

To change the default style, you need to import the :const:`~ItsPrompt.data.style.default_style` and change its values:

.. code-block:: python
    
    from ItsPrompt.data.style import default_style

    default_style.error = 'fg:ansired bg:ansiwhite'

This will automatically change the style of all prompts, which do not have an own style defined.

Creating your own Style
-----------------------

To define your own style for a specific prompt, import :class:`~ItsPrompt.data.style.PromptStyle` and create an object. 
Then assign it to the `style` argument of any prompt.

.. code-block:: python

    from ItsPrompt.data.style import PromptStyle

    my_style = PromptStyle(
        question_mark='fg:ansiblue',
        error='fg:ansired bg:ansiwhite',
    )

.. note:: 

    If you omit a style attribute of your :class:`~ItsPrompt.data.style.PromptStyle`, this attribute **will not** use 
    the one given by the :const:`~ItsPrompt.data.style.default_style`. Instead, it will use the default style given by 
    `prompt_toolkit`.

If you want to create your own style from the :const:`~ItsPrompt.data.style.default_style`, you can use the
:meth:`~ItsPrompt.data.style.create_from_default` method:

.. code-block:: python

    from ItsPrompt.data.style import create_from_default

    my_style = create_from_default()
    
    my_style.error = 'fg:ansired bg:ansiwhite'

This will create a copy of the :const:`~ItsPrompt.data.style.default_style` and change its `error` attribute. All other
attributes will remain the same as the :const:`~ItsPrompt.data.style.default_style`.

.. note::

    Warning! Not copying the default style and changing it instead will result in all prompts using your changes, as a
    variable is by default not a copy, but a reference to the same object!
