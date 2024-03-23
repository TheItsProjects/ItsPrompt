ItsPrompt Usage
===============

Question and Options
--------------------

Question
~~~~~~~~

All basic prompt types have a ``question`` parameter which is the question that will be asked to the user. 

.. code-block:: python
    
        from itsprompt.prompt import Prompt
    
        ans = Prompt.input(question="What is your name?")

        print(ans)

The above code will ask the user "What is your name?" and will store the user's input in the variable ``ans``.

Options
~~~~~~~

Prompt types which require the user to select an option from a list of options have an ``options`` parameter which is a
list of options that the user can select from.

.. code-block:: python
    
        from itsprompt.prompt import Prompt
    
        ans = Prompt.select(question="What is your favorite color?", options=["Red", "Green", "Blue"])

        print(ans)
        
The above code will ask the user "What is your favorite color?" and will store the user's selected option in the 
variable ``ans``.

There are many different ways to create options, including adding separators. To read more about them see 
:doc:`options_and_data`.

Default Option
~~~~~~~~~~~~~~

Prompt types which require options have the ability to have a default option. This is done by setting the ``default``
parameter to the name or id of the default option.

.. code-block:: python
    
        from itsprompt.prompt import Prompt
    
        ans = Prompt.select(question="What is your favorite color?", options=["Red", "Green", "Blue"], default="Green")

        print(ans)
        
The above code will ask the user "What is your favorite color?" and will store the user's selected option in the
variable ``ans``. The pointer will start on the option "Green".

Disabled Options
~~~~~~~~~~~~~~~~

Prompt types which require options have the ability to have disabled options. This is done by setting the ``disabled``
parameter to a list of the names or ids of the disabled options.

.. code-block:: python
    
        from itsprompt.prompt import Prompt
    
        ans = Prompt.select(question="What is your favorite color?", options=["Red", "Green", "Blue"], disabled=["Green"])

        print(ans)

The above code will ask the user "What is your favorite color?" and will store the user's selected option in the
variable ``ans``. The option "Green" will be grayed out and the user will not be able to select it.

Text Input
~~~~~~~~~~

Prompt types which require text input have a ``default`` parameter which is the default text that will be displayed in
the input field.

.. code-block:: python
    
        from itsprompt.prompt import Prompt
    
        ans = Prompt.input(question="What is your name?", default="John")

        print(ans)
        
The above code will ask the user "What is your name?" and will store the user's input in the variable ``ans``. The input
field will have the text "John" already in it.

Styling
-------

Prompt types have a ``style`` parameter which defines the style of the prompt. To read more about styling see 
:doc:`styling`.
