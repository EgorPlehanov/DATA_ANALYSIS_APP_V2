from .parameter_editor_interface import ParamEditorInterface
from ...function_typing import ParameterType

from typing import List
from dataclasses import dataclass, field
from flet import Container, Ref, Checkbox, Column


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
    # TODO: добавить валидацию полей для всех классов конфигураций

class CheckboxesEditor(ParamEditorInterface, Container):
    def __init__(self, function, config: CBConfig = CBConfig()):
        self.function = function

        self._type = ParameterType.CHECKBOXES
        self._name = config.name
        self.title = config.title
        self.checkboxes = config.checkboxes
        self.default_value = config.default_value

        super().__init__()
        self._set_styles()
        self.content = self._create_content()


    def _create_content(self) -> Column:
        ref_checkboxes = [Ref[Checkbox]() for _ in range(len(self.checkboxes))]
        return Column(
            controls=[
                Checkbox(
                    label=checkbox.label,
                    value=checkbox.default_value,
                    ref=ref_checkboxes[idx],
                    data={
                        'key': checkbox.key,
                        'ref_checkboxes': ref_checkboxes,
                        'param_name': self._param_name,
                    },
                    on_change=self._on_change,
                )
                for idx, checkbox in enumerate(self.checkboxes)
            ]
        )
    

    def _on_change(self, e) -> None:
        '''
        Обновляет значение параметр в экземпляре класса Function
        Изменяет список выбранных чекбоксов
        '''
        checkbox_key = e.control.data.get('key')
        checkbox_value = e.control.value

        # param_current_value = self.function.get_parameter_value(param_name).get('value', [])
        # if checkbox_value:
        #     param_current_value.append(checkbox_key)
        # else:
        #     param_current_value.remove(checkbox_key)
        # self.function.set_parameter_value(param_name, param_current_value)
        # self.update_function_card()
         