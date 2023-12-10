from ..function_typing import ResultData, ViewType
from .result_attributes import *

from dataclasses import dataclass
from typing import Any
from flet import (
    Container, colors, padding, border, Column, Ref, Text, Row,
    MainAxisAlignment, FontWeight, IconButton, icons, Icon, Markdown,
    CrossAxisAlignment, animation, BorderSide, AnimationCurve
)


@dataclass
class ResultItem:
    control: Any     = None
    is_main: bool    = False
    button_name: str = 'Показать'
    is_open: bool    = False


class FunctionResultView(Container):
    def __init__(self, function):
        super().__init__()
        self.function = function
        self.key = self.function.id

        self.border_radius = 10
        self.bgcolor = colors.BLACK26
        self.padding = padding.only(left=10, top=10, right=20, bottom=10)
        self.on_click = self.function._on_click

        self.result_data: ResultData = self.function.get_result()

        self.ref_title = Ref[Text]()
        self.view_title = self._create_view_title()

        self.content = self.create_content()


    def change_selection(self):
        '''Изменяет выделение результата'''
        self.border = border.all(color=colors.BLUE) if self.function.selected else None


    def create_content(self) -> Column | Row:
        if (
            self.result_data.main_data is None
            and self.result_data.extra_data is None
            and self.result_data.error_message is None
        ):
            self.ref_title.current.value = 'Нет данных для построения графиков функции ' + self.function.calculate_function_name
            return self.view_title

        is_many_graphs = True
        self.ref_title.current.value = f"График{'и' if is_many_graphs else ''} функции {self.function.calculate_function_name}"
        return Column([
            self.view_title,
            self._create_view_result(self.result_data),
        ])


    def _create_view_title(self) -> Row:
        '''Создает заголовок результата'''
        return Row(
            alignment = MainAxisAlignment.CENTER,
            controls = [Text(
                ref = self.ref_title,
                weight = FontWeight.BOLD,
                size = 20
            )]
        )


    def _create_view_result(self, result_data: ResultData) -> Column:
        '''Создает содержимое результата'''
        element_controls = []
        
        error_message = result_data.error_message
        if error_message is not None:
            element_controls.append(ResultItem(
                control = ResultErrorMessage(error_message),
                is_main = True
            ))
        
        main_data = result_data.main_data
        if main_data is not None:
            type = result_data.type.strip()
            if result_data.view_chart:
                element_controls.append(ResultItem(
                    control = ResultChart(main_data, type),
                    is_main = result_data.main_view == ViewType.CHART,
                    button_name = f"Показать график: ***{type}***"
                ))

            if result_data.view_histogram:
                element_controls.append(ResultItem(
                    control = ResultHistogram(main_data, type),
                    is_main = result_data.main_view == ViewType.HISTOGRAM,
                    button_name = f"Показать гистограмму: ***{type}***"
                ))
                    

            if result_data.view_table_horizontal:
                element_controls.append(ResultItem(
                    control = ResultTableHorizontal(main_data),
                    is_main = result_data.main_view == ViewType.TABLE_HORIZONTAL,
                    button_name = f"Показать таблицу данных: ***{type}***"
                ))
                    
            if result_data.view_table_vertical:
                element_controls.append(ResultItem(
                    control = ResultTableVertical(main_data),
                    is_main = result_data.main_view == ViewType.TABLE_VERTICAL,
                    button_name = f"Показать таблицу статистических параметров: ***{type}***",
                ))

        extra_data = result_data.extra_data
        if extra_data:
            for data in extra_data:
                element_controls.append(ResultItem(
                    control = self._create_view_result(data),
                    button_name = f"Показать дополнительные данные:{(f' ***{data.type.strip()}***')}"
                ))

        initial_data = result_data.initial_data
        if initial_data:
            for data in initial_data:
                element_controls.append(ResultItem(
                    control = self._create_view_result(data),
                    button_name = f"Показать исходные данные:{(f' ***{data.type.strip()}***')}"
                ))

        return Column([
            item.control if item.is_main
            else ResultToggleContainer(item.control, item.button_name, item.is_open)
            for item in element_controls
        ])

    

    def update_values(self) -> None:
        '''Обновляет представление результатов'''
        self.result_data = self.function.get_result()
        self.content = self.create_content()
        self.update()
        