from .table_dict import TableDataFromDict
from ..prompts.type import TablePromptDict, TablePromptList


class TableDataFromList(TableDataFromDict):

    def __init__(self, data: TablePromptList):
        # convert list to dict
        dict_data: TablePromptDict = {f"{col}": rows for col, rows in enumerate(data)}

        super().__init__(dict_data)

    def get_data(self) -> TablePromptList:  # type: ignore
        # convert dict to list
        list_data: TablePromptList = list(self.data.values())

        return list_data
