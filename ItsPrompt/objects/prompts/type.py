from ItsPrompt.objects.prompts.separator import Separator

OptionWithId = tuple[str, str, str | None]
"""
The OptionWithId tuple is used to store an option, its id and an optional key (for expand prompt).

For all prompts excluding :meth:`~ItsPrompt.prompt.Prompt.expand`, the tuple is structured as follows

- The first element is the displayed option
- The second element is the id of the option

For the :meth:`~ItsPrompt.prompt.Prompt.expand` prompt, the tuple is structured as follows:

- The first element is the key of the option
- The second element is the displayed option
- The third element is the id of the option
"""

OptionsList = tuple[str | OptionWithId | Separator, ...]
"""
Different types of options that can be used in a prompt.

Can be given by either:

- A :class:`str`, which is the displayed option and its id
- A :class:`tuple` containing the displayed option, its id and an optional key (for expand prompt)
- A :class:`~ItsPrompt.objects.prompts.separator.Separator` instance
"""

TablePromptList = list[list[str]]
"""
A type hint for the :class:`list` structure used to represent a table prompt.

Each inner :class:`list` represents a row in the table.

The cells are represented by the :class:`str` type.

"""

TablePromptDict = dict[str, list[str]]
"""
A type hint for the :class:`dict` structure used to represent a table prompt.

The keys are the column names and the values are the cells in the column.
"""

CompletionDict = dict[str, "CompletionDict | None"]
"""
A type hint for the :class:`dict` structure used to represent the completion dictionary.
"""
