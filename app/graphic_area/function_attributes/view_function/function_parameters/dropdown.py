from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ....function import Function

from .parameter_editor_interface import ParamEditorInterface
from ...function_typing import ParameterType

from typing import List
from dataclasses import dataclass, field
from flet import Container, Dropdown, dropdown, ControlEvent


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

    @property
    def type(self) -> ParameterType:
        return ParameterType.DROPDOWN


class DropdownEditor(ParamEditorInterface, Container):
    def __init__(self, function: 'Function', config: DDConfig = DDConfig()):
        self._type = ParameterType.DROPDOWN
        self.function = function
        
        self._name = config.name
        self.title = config.title
        self.options = config.options
        self.default_value = config.default_value

        self.key_str_to_value = {
            str(option.key): option.key
            for option in self.options
        }

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
    

    def _on_change(self, e: ControlEvent) -> None:
        '''Обновляет значение параметра в экземпляре класса Function и карточке функции'''
        value = self.key_str_to_value[e.control.value]
        self.function.calculate.set_parameter_value(self._name, value)
        self.update()
