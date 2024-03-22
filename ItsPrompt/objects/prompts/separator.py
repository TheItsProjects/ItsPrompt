class Separator:
    """
    Used for creating distinctive sections in the prompt types:

    - :meth:`~ItsPrompt.prompt.Prompt.select`
    - :meth:`~ItsPrompt.prompt.Prompt.raw_select`
    - :meth:`~ItsPrompt.prompt.Prompt.checkbox`
    - :meth:`~ItsPrompt.prompt.Prompt.expand`

    It is purely cosmetic.
    """

    def __init__(self, label: str):
        """
        Initializes an instance of the Separator class with the given text.

        :param label: The text to be stored.
        """
        self.label = label
