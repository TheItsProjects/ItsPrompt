from ItsPrompt.objects.prompts.separator import Separator

CompletionDict = dict[str, "CompletionDict | None"]

TablePromptDict = dict[str, list[str]]
TablePromptList = list[list[str]]

OptionWithId = tuple[str, str, str | None]
OptionsList = tuple[str | OptionWithId | Separator, ...]
