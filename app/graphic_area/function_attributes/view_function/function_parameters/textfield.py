from .parameter_editor_interface import ParamEditorInterface
from ...function_typing import ValueType, ParameterType
from .parameters_utils import validate_textfield_value

from dataclasses import dataclass
from flet import Container, TextField, TextStyle, TapEvent


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

    @property
    def type(self) -> ParameterType:
        return ParameterType.TEXTFIELD


class TextFieldEditor(ParamEditorInterface, Container):
    def __init__(self, function, config: TFConfig = TFConfig()):
        self._type = ParameterType.TEXTFIELD
        self.function = function

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
            data = {'value_type': self.value_type},
            on_change = validate_textfield_value,
            on_blur = self._on_change,
            on_submit = self._on_change,
        )
    

    def _on_change(self, e) -> None:
        '''Обновляет значение параметра текстового поля в экземпляре класса Function'''
        if e.control.error_text:
            return
        self.function.calculate.set_parameter_value(self._name, e.control.value)
        self.update()
    