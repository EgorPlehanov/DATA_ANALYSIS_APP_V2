from .param_editor_interface import ParamEditorInterface

from typing import Literal
from flet import Container, TextField, TextStyle


class TextFieldEditor(ParamEditorInterface, Container):
    def __init__(self,
        param_name: str             = '',
        value_type: Literal['function', 'int_number', 'number'] = 'number',
        label: str                 = None,
        prefix_text: str            = None,
        hint_text: str              = None,
        helper_text: str            = None,
        default_value: str          = None,
        autocorrect: bool           = False
    ):
        self._type = 'text_field'
        self._param_name = param_name
        self.value_type = value_type
        self.label = label
        self.prefix_text = prefix_text
        self.hint_text = hint_text
        self.helper_text = helper_text
        self.default_value = default_value
        self.autocorrect = autocorrect

        super().__init__()
        self.set_styles()
        self.content = self.create_content()


    def create_control(self) -> TextField:
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
            on_blur = self.on_change,
            on_submit = self.on_change,
        )
    

    def on_change(self, e) -> None:
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
    