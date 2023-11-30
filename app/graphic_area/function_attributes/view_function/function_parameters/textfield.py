from .parameter_editor_interface import ParamEditorInterface
from function_typing import ValueType

from dataclasses import dataclass
from typing import Literal
from flet import Container, TextField, TextStyle


@dataclass
class TFConfig:
    name: str               = ''
    value_type: ValueType   = ValueType.FLOAT
    label: str              = None
    prefix_text: str        = None
    hint_text: str          = None
    helper_text: str        = None
    default_value: str      = ''
    autocorrect: bool       = False


class TextFieldEditor(ParamEditorInterface, Container):
    def __init__(self, config: TFConfig = TFConfig()):
        self._type = 'text_field'
        self._name = config.name
        self.value_type = config.value_type
        self.label = config.label
        self.prefix_text = config.prefix_text
        self.hint_text = config.hint_text
        self.helper_text = config.helper_text
        self.default_value = config.default_value
        self.autocorrect = config.autocorrect

        super().__init__()
        self._set_styles()
        self.content = self._create_content()


    def _create_content(self) -> TextField:
        return TextField(
            label = self.label,
            prefix_text = self.prefix_text,
            hint_text = self.hint_text,
            hint_style = TextStyle(italic=True),
            helper_text = self.helper_text,
            dense = True,
            autocorrect = self.autocorrect,
            value = self.default_value,
            on_change = None, #self._is_text_field_value_valid,
            on_blur = self._on_change,
            on_submit = self._on_change,
        )
    

    def _on_change(self, e) -> None:
        '''
        Обновляет значение параметра текстового поля в экземпляре класса Function
        '''
        if e.control.error_text:
            return
        text_field_value = e.control.value
        # self.function.set_parameter_value(
        #     self._param_name, text_field_value,
        #     text_field_value.replace('**', '\*\*') if text_field_value else 'Нет значения'
        # )
        # self.update_function_card()
    