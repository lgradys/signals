from typing import List

from dash import dcc


class Option:

    def __init__(self, label, value):
        self.__label = label
        self.__value = value

    def get_label(self) -> str:
        return self.__label

    def get_value(self) -> str:
        return self.__value


class Dropdown(dcc.Dropdown):

    def __init__(self, dropdown_id: str, options: List[Option], value=None):
        super().__init__(
            id=dropdown_id,
            options=[{'label': option.get_label(), 'value': option.get_value()} for option in options],
            clearable=True,
            className='dropdown-select',
            value=value)
