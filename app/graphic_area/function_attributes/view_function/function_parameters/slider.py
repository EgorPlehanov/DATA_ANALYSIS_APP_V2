from .param_editor_interface import ParamEditorInterface

from typing import Literal
from flet import (
    Container, TextField, Slider, Ref, Column, Row, Text, InputBorder, TextThemeStyle
)


class SliderEditor(ParamEditorInterface, Container):
    def __init__(self,
        name: str                   = '',
        title: str                  = '',
        value_type: Literal['int_number', 'number'] = 'number',
        round_digits: int           = 2,
        min: int | float            = 0,
        max: int | float            = 0,
        step: int | float           = 1,
        default_value: int | float  = 0
    ):
        self._type = 'slider'
        self._name = name
        self.title = title
        self.value_type = value_type
        self.round_digits = round_digits
        self.min = min
        self.max = max
        self.step = step
        self.default_value = default_value

        super().__init__()
        self.set_styles()
        self.content = self.create_content()
    
    
    def create_content(self) -> Column:
        ref_textfield = Ref[TextField]()
        ref_slider = Ref[Slider]()

        slider_divisions = int((self.max - self.min) / self.step)
        editor_slider = Column(
            controls=[
                Row(
                    controls=[
                        Text(f'{self.title}:'),
                        TextField(
                            ref = ref_textfield,
                            value = self.default_value,
                            tooltip = f"Задайте значение от {self.min} до {self.max} (шаг {self.step})",
                            hint_text = f"Задайте {self._param_name}",
                            expand = True,
                            dense = True,
                            border = InputBorder.UNDERLINE,
                            data = {
                                'ref_slider': ref_slider,
                                'round_digits': self.round_digits,
                                'text_type': self.value_type,
                                'min': self.min,
                                'max': self.max,
                            },
                            on_change = None, #self._is_text_field_value_valid,
                            on_blur = self.on_change,
                            on_submit = self.on_change,
                        )
                    ],
                ),
                Row(
                    controls=[
                        Text(self.min, style = TextThemeStyle.BODY_SMALL),
                        Slider(
                            ref = ref_slider,
                            expand = True,
                            min = self.min,
                            max = self.max,
                            value = self.default_value,
                            divisions = slider_divisions,
                            label = '{value}',
                            data = {"ref_textfield": ref_textfield},
                            on_change = None, #self._update_slider_textfield,
                            on_change_end = self.on_change,
                        ),
                        Text(self.max, style = TextThemeStyle.BODY_SMALL),
                    ],
                    spacing = 0
                )
            ],
            spacing = 0
        )
        return editor_slider
    
    
    def on_change(self, e) -> None:
        '''
        Обнавляет значение параметра в экземпляре класса Function, заголовке слайдера и карточке функции
        '''
        if e.control.data.get('ref_slider'):
            param_editor = e.control.data.get('ref_slider').current
            if e.control.error_text or not e.control.value:
                return
        else:
            param_editor = e.control.data.get('ref_textfield').current
            param_editor.error_text = None

        # param_name = e.control.data.get('param_name')
        # round_digits = e.control.data.get('round_digits', 3)
        # param_value_type = e.control.data.get('text_type', 'number')
        # param_value = int(float(e.control.value) * 10**round_digits) / 10**round_digits \
        #     if round_digits > 0 and param_value_type != 'int_number' else int(float(e.control.value))

        # e.control.value = str(param_value)
        # param_editor.value = str(param_value)
        # self.function.set_parameter_value(param_name, param_value)

        # self.update_function_card()
    