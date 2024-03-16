from typing import Iterator, TypeVar, Generic

from ItsPrompt.objects.prompts.separator import Separator

OptionOrSeparator = TypeVar("OptionOrSeparator")


class OptionsWithSeparator(Generic[OptionOrSeparator], list):
    """
    The `OptionsWithSeparator` class is a subclass of the built-in list class in Python.

    This class is designed to hold a list of arguments, but with a specific behavior: 
    it filters out all `Separator`s. The original list including the `Separator` instances is stored 
    in the `with_separators` attribute.

    :ivar with_separators: A list that holds the original arguments passed including all `Separator`s. 

    :param args: The items for the list

    Note:
        These `Separator` instances are excluded from the parent list object. To access the 
        original list that includes the `Separator` instances, use the `with_separators` 
        attribute.

    """

    def __init__(self, *args: OptionOrSeparator | Separator):
        self.with_separators = list(args)
        super().__init__([x for x in args if not isinstance(x, Separator)])

    def with_separators_enumerate(self) -> Iterator[tuple[int, OptionOrSeparator | Separator]]:
        """
        Enumerate the items in the `OptionsWithSeperator` list, including separators.

        For every Separator, the index is not increased and instead -1 is returned.

        :return: An iterator that yields tuples containing the index and the item.
        """
        index = 0

        for item in self.with_separators:
            if type(item) is Separator:
                yield -1, item
            else:
                yield index, item
                index += 1
