from .param_editor_interface import ParamEditorInterface

from typing import List
from dataclasses import dataclass
from flet import Container, Ref, Checkbox, Column


@dataclass
class CBItem:
    key: str            = None
    label: str          = None
    default_value: bool = False


class CheckboxesEditor(ParamEditorInterface, Container):
    def __init__(self,
        param_name: str          = '',
        title: str               = '',
        checkboxes: List[CBItem] = [],
        default_value: bool      = False
    ):
        self._type = 'checkbox'
        self._param_name = param_name
        self.title = title
        self.checkboxes = checkboxes
        self.default_value = default_value

        super().__init__()
        self.set_styles()
        self.content = self.create_content()


    def create_content(self) -> Column:
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
                    on_change=self.on_change,
                )
                for idx, checkbox in enumerate(self.checkboxes)
            ]
        )
    

    def on_change(self, e) -> None:
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
         