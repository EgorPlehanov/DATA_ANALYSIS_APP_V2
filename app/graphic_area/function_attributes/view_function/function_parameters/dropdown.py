from .param_editor_interface import ParamEditorInterface

from typing import List
from dataclasses import dataclass
from flet import Container, Dropdown, dropdown


@dataclass
class DDOptionItem:
    key: str    = None
    text: str   = None


class DropdownEditor(ParamEditorInterface, Container):
    def __init__(self,
        name: str                   = None,
        title: str                  = None,
        options: List[DDOptionItem] = None,
        default_value: str          = None
    ):
        self._type = 'dropdown'
        self._name = name
        self.title = title
        self.options = options
        self.default_value = default_value

        super().__init__()
        self.set_styles()
        self.content = self.create_content()


    def create_content(self) -> Dropdown:
        return Dropdown(
            dense=True,
            label=self.title,
            options=[
                dropdown.Option(key=option.key, text=option.text)
                for option in self.options
            ],
            value=self.default_value,
            on_change=self.on_change
        )
    

    def on_change(self, e) -> None:
        '''
        Обновляет значение параметра в экземпляре класса Function и карточке функции
        '''
        param_value = e.control.value
        # self.function.set_parameter_value(self._param_name, param_value)

        # self.update_function_card()
