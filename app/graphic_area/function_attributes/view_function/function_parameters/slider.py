from .parameter_editor_interface import ParamEditorInterface
from ...function_typing import ValueType, ParameterType
from .parameters_utils import validate_textfield_value

from dataclasses import dataclass
from flet import (
    Container, TextField, Slider, Ref, Column, Row, Text, InputBorder, TextThemeStyle
)


@dataclass
class SLConfig:
    name: str                   = ''
    title: str                  = ''
    value_type: ValueType       = ValueType.FLOAT
    round_digits: int           = 2
    min: int | float            = 0
    max: int | float            = 1
    step: int | float           = 1
    default_value: int | float  = 1

    @property
    def type(self) -> ParameterType:
        return ParameterType.SLIDER


class SliderEditor(ParamEditorInterface, Container):
    def __init__(self, function, config: SLConfig = SLConfig()):
        self.function = function

        self._type = ParameterType.SLIDER
        self._name = config.name
        self.title = config.title
        self.value_type = config.value_type
        self.round_digits = config.round_digits
        self.min = config.min
        self.max = config.max
        self.step = config.step
        self.default_value = config.default_value

        super().__init__()
        self._set_styles()

        self.ref_textfield = Ref[TextField]()
        self.ref_slider = Ref[Slider]()

        self.content = self._create_content()
    
    
    def _create_content(self) -> Column:
        '''Создает модификатор параметра типа Slider'''
        editor_slider = Column(
            controls=[
                self._create_editor_part_textfield(),
                self._create_editor_part_slider()
            ],
            spacing = 0
        )
        return editor_slider
    

    def _create_editor_part_textfield(self) -> Row:
        '''Создает часть модификатора параметра с текстовым полем'''
        return Row(
            controls=[
                Text(f'{self.title if self.title else self._name}:'),
                TextField(
                    ref = self.ref_textfield,
                    value = self.default_value,
                    tooltip = f"Задайте значение от {self.min} до {self.max} (шаг {self.step})",
                    hint_text = f"Задайте {self._name}",
                    expand = True,
                    dense = True,
                    border = InputBorder.UNDERLINE,
                    data = {
                        'round_digits': self.round_digits,
                        'text_type': self.value_type,
                        'min': self.min,
                        'max': self.max,
                    },
                    on_change = validate_textfield_value,
                    on_blur = self._on_change,
                    on_submit = self._on_change,
                )
            ],
        )
    

    def _create_editor_part_slider(self) -> Row:
        '''Создает часть модификатора параметра со слайдером'''
        slider_divisions = int((self.max - self.min) / self.step)
        return Row(
            controls=[
                Text(self.min, style = TextThemeStyle.BODY_SMALL),
                Slider(
                    ref = self.ref_slider,
                    expand = True,
                    min = self.min,
                    max = self.max,
                    value = self.default_value,
                    divisions = slider_divisions,
                    label = '{value}',
                    on_change_end = self._on_change,
                ),
                Text(self.max, style = TextThemeStyle.BODY_SMALL),
            ],
            spacing = 0
        )
    
    
    def _on_change(self, e) -> None:
        '''Обнавляет значение параметра и значение текстового поля'''
        if isinstance(e.control, TextField):
            param_editor = self.ref_slider.current
            if e.control.error_text or not e.control.value:
                return
        else:
            param_editor = self.ref_textfield.current
            param_editor.error_text = None

        value = int(float(e.control.value) * 10**self.round_digits) / 10**self.round_digits \
            if self.round_digits > 0 and self.value_type != 'int_number' else int(float(e.control.value))

        e.control.value = str(value)
        param_editor.value = str(value)
        self.function.calculate.set_parameter_value(self._name, value)

        self.update()
    