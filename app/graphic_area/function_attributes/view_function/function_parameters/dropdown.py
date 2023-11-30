from .parameter_editor_interface import ParamEditorInterface

from typing import List
from dataclasses import dataclass, field
from flet import Container, Dropdown, dropdown


@dataclass
class DDOptionItem:
    key: str    = ''
    text: str   = 'Не задано'

@dataclass
class DDConfig:
    name: str                   = ''
    title: str                  = ''
    options: List[DDOptionItem] = field(default_factory=list)
    default_value: str          = ''


class DropdownEditor(ParamEditorInterface, Container):
    def __init__(self, config: DDConfig = DDConfig()):
        self._type = 'dropdown'
        self._name = config.name
        self.title = config.title
        self.options = config.options
        self.default_value = config.default_value

        super().__init__()
        self._set_styles()
        self.content = self._create_content()


    def _create_content(self) -> Dropdown:
        return Dropdown(
            dense=True,
            label=self.title,
            options=[
                dropdown.Option(key=option.key, text=option.text)
                for option in self.options
            ],
            value=self.default_value,
            on_change=self._on_change
        )
    

    def _on_change(self, e) -> None:
        '''
        Обновляет значение параметра в экземпляре класса Function и карточке функции
        '''
        param_value = e.control.value
        # self.function.set_parameter_value(self._param_name, param_value)

        # self.update_function_card()
