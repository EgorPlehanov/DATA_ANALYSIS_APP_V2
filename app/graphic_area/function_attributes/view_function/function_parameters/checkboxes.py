from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ....function import Function

from .parameter_editor_interface import ParamEditorInterface
from ...function_typing import ParameterType

from typing import List
from dataclasses import dataclass, field
from flet import Container, ControlEvent, Checkbox, Column


@dataclass
class CBItem:
    key: str            = None
    label: str          = None
    default_value: bool = False

@dataclass
class CBConfig:
    name: str                = ''
    title: str               = ''
    checkboxes: List[CBItem] = field(default_factory=list)
    default_value: List[str] = field(default_factory=list)

    @property
    def type(self) -> ParameterType:
        return ParameterType.CHECKBOXES

    def __post_init__(self):
        for chkbox in self.checkboxes:
            chkbox.default_value = chkbox.key in self.default_value


class CheckboxesEditor(ParamEditorInterface, Container):
    def __init__(self, function: 'Function', config: CBConfig = CBConfig()):
        self._type = ParameterType.CHECKBOXES
        self.function = function
        
        self._name = config.name
        self.title = config.title
        self.checkboxes = config.checkboxes
        self.default_value = config.default_value

        super().__init__()
        self._set_styles()
        self.content = self._create_content()


    def _create_content(self) -> Column:
        return Column(
            controls=[
                Checkbox(
                    label = checkbox.label,
                    value = checkbox.default_value,
                    key = str(checkbox.key),
                    on_change = self._on_change,
                )
                for checkbox in self.checkboxes
            ]
        )
    

    def _on_change(self, e: ControlEvent) -> None:
        '''
        Обновляет значение параметр в экземпляре класса Function
        Изменяет список выбранных чекбоксов
        '''
        key = e.control.key
        value = e.control.value

        current_value = self.function.calculate.get_current_parameter_value(self._name)
        if value:
            current_value.append(key)
        else:
            current_value.remove(key)
        
        self.function.calculate.set_parameter_value(self._name, current_value)
        self.update()
         