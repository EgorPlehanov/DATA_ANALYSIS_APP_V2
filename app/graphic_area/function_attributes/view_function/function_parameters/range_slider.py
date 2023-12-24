from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ....function import Function

from .parameter_editor_interface import ParamEditorInterface
from ...function_typing import ValueType, ParameterType, Range
from .parameters_utils import validate_textfield_value

from dataclasses import dataclass
from flet import (
    Container, TextField, RangeSlider, Ref, Column, Row,
    Text, InputBorder, TextThemeStyle, ControlEvent
)


@dataclass
class RSLConfig:
    name: str             = ''
    title: str            = ''
    value_type: ValueType = ValueType.FLOAT
    round_digits: int     = 2
    min: int | float      = 0
    max: int | float      = 1
    step: int | float     = 1
    default_value: Range  = 1
    @property
    def type(self) -> ParameterType:
        return ParameterType.RANGE_SLIDER


class RangeSliderEditor(ParamEditorInterface, Container):
    def __init__(self, function: 'Function', config: RSLConfig = RSLConfig()):
        self._type = ParameterType.RANGE_SLIDER
        self.function = function

        self._name = config.name
        self.title = config.title
        self.value_type = config.value_type
        self.round_digits = config.round_digits
        self.min = config.min
        self.max = config.max
        self.step = config.step
        self.default_value = config.default_value

        self.start_value = self.default_value.start_value
        self.end_value = self.default_value.end_value

        super().__init__()
        self._set_styles()

        self.content = self._create_content()
    
    
    def _create_content(self) -> Column:
        '''Создает модификатор параметра типа Slider'''
        self.ref_textfield_start = Ref[TextField]()
        self.ref_textfield_end = Ref[TextField]()
        return Column(
            controls=[
                Text(self.title),
                self._create_textfield(self.ref_textfield_start, 'От', self.start_value),
                self._create_textfield(self.ref_textfield_end, 'До', self.end_value),
                self._create_range_slider()
            ],
            spacing = 0
        )
    

    def _create_textfield(self, ref: Ref, title: str = '', value: int | float = 0) -> Row:
        '''Создает часть модификатора параметра с текстовым полем'''
        return Row([
            Text(title),
            TextField(
                ref = ref,
                value = value,
                tooltip = f"Задайте значение от {self.min} до {self.max} (шаг {self.step})",
                hint_text = f"Задайте {self._name}",
                expand = True,
                dense = True,
                border = InputBorder.UNDERLINE,
                data = {
                    'round_digits': self.round_digits,
                    'value_type': self.value_type,
                    'min': self.min,
                    'max': self.max,
                },
                on_change = validate_textfield_value,
                on_blur = self._on_change,
                on_submit = self._on_change,
            )
        ])
    

    def _create_range_slider(self) -> Row:
        '''Создает часть модификатора параметра со слайдером'''
        self.ref_range_slider = Ref[RangeSlider]()
        slider_divisions = int((self.max - self.min) / self.step)
        return Row(
            controls=[
                Text(self.min, style = TextThemeStyle.BODY_SMALL),
                RangeSlider(
                    ref = self.ref_range_slider,
                    expand = True,
                    min = self.min,
                    max = self.max,
                    start_value = self.start_value,
                    end_value = self.end_value,
                    divisions = slider_divisions,
                    label = '{value}',
                    on_change_end = self._on_change,
                ),
                Text(self.max, style = TextThemeStyle.BODY_SMALL),
            ],
            spacing = 0
        )
    
    
    def _on_change(self, e: ControlEvent) -> None:
        '''Обнавляет значение параметра и значение текстового поля'''
        textfield_start = self.ref_textfield_start.current
        textfield_end = self.ref_textfield_end.current
        range_slider = self.ref_range_slider.current

        if isinstance(e.control, TextField):
            if (
                textfield_start.error_text or not textfield_start.value
                or textfield_end.error_text or not textfield_end.value
            ):
                return
            start_value = textfield_start.value
            end_value = textfield_end.value
        else:
            start_value = range_slider.start_value
            end_value = range_slider.end_value
            
        start_value = self._round_value(start_value)
        end_value = self._round_value(end_value)

        if start_value > end_value:
            start_value, end_value = end_value, start_value

        if isinstance(e.control, TextField):
            range_slider.start_value = start_value
            range_slider.end_value = end_value
        
        textfield_start.value = str(start_value)
        textfield_end.value = str(end_value)

        self.function.calculate.set_parameter_value(self._name, Range(start_value, end_value))
        self.update()


    def _round_value(self, value: int | float) -> int | float:
        '''Округляет значение параметра'''
        if self.round_digits > 0 and self.value_type != ValueType.INT:
            return int(float(value) * 10**self.round_digits) / 10**self.round_digits
        else:
            return int(float(value))
    