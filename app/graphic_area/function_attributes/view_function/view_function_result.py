from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ...function import Function

from ..function_typing import ResultData, ViewType
from .result_attributes import *

from dataclasses import dataclass
from typing import Any, List
from flet import (
    Container, colors, padding, border, Column, Text,
    TextAlign, Ref, Row, MainAxisAlignment, FontWeight
)


@dataclass
class ResultItem:
    control: Any     = None
    is_main: bool    = False
    button_name: str = 'Показать'
    is_open: bool    = False


class FunctionResultView(Container):
    '''Представление результата функции'''
    def __init__(self, function: "Function"):
        super().__init__()
        self.function = function
        self.key = self.function.id

        self.border_radius = 10
        self.bgcolor = colors.BLACK26
        self.padding = padding.only(left=10, top=10, right=20, bottom=10)
        # self.on_click = self.function._on_click

        self.result_data: ResultData = self.function.get_result()

        self.ref_title = Ref[Text]()
        self.view_title = self._create_view_title()

        self.content = self.create_content()


    def change_selection(self):
        '''Изменяет выделение результата'''
        self.border = border.all(color=colors.BLUE) if self.function.selected else None


    def create_content(self) -> Column | Row:
        '''Создает содержимое'''
        if (
            self.result_data.main_data is None
            and self.result_data.extra_data is None
            and self.result_data.error_message is None
        ):
            self.ref_title.current.value = self.function.name \
                + "\nНет данных для построения графиков функции"
            return self.view_title

        is_many_graphs = self._is_result_data_have_many_graphs()
        self.ref_title.current.value = f"График{'и' if is_many_graphs else ''} " \
            + f"функции {self.function.name}"
        
        return Column([
            self.view_title,
            self._create_view_result(self.result_data),
        ])


    def _is_result_data_have_many_graphs(self) -> bool:
        '''Проверяет есть ли в результатах больше одного графика'''
        result = self.result_data

        view_cnt = sum(filter(None, [
            result.view_chart, result.view_histogram,
            result.view_table_horizontal, result.view_table_vertical
        ])) if self.result_data.main_data is not None else 0
        extra_cnt = len(self.result_data.extra_data) \
            if self.result_data.extra_data is not None else 0

        count = view_cnt + extra_cnt
        return count > 1


    def _create_view_title(self) -> Row:
        '''Создает заголовок результата'''
        return Row(
            alignment = MainAxisAlignment.CENTER,
            controls = [Text(
                ref = self.ref_title,
                weight = FontWeight.BOLD,
                size = 20,
                text_align = TextAlign.CENTER
            )]
        )


    def _create_view_result(self, result_data: ResultData) -> Column:
        '''Создает содержимое результата'''
        result_items = []
        
        if result_data.error_message is not None:
            result_items.append(self._create_result_item('error_message', result_data))
        
        if result_data.main_data is not None:
            if result_data.view_chart:
                result_items.append(self._create_result_item(ViewType.CHART, result_data))

            if result_data.view_audio:
                result_items.append(self._create_result_item(ViewType.AUDIO, result_data))

            if result_data.view_histogram:
                result_items.append(self._create_result_item(ViewType.HISTOGRAM, result_data))
                    
            if result_data.view_table_horizontal:
                result_items.append(self._create_result_item(ViewType.TABLE_HORIZONTAL, result_data))
                    
            if result_data.view_table_vertical:
                result_items.append(self._create_result_item(ViewType.TABLE_VERTICAL, result_data))

        if result_data.extra_data:
            for data in result_data.extra_data:
                result_items.append(self._create_result_item('extra_data', data))

        if result_data.initial_data:
            for data in result_data.initial_data:
                result_items.append(self._create_result_item('initial_data', data))
        
        return Column(self._create_view_list_result_item(result_items))
    

    def _create_result_item(self, type: str, result_data: ResultData) -> ResultItem:
        '''Создает элемент результата по типу и данным'''
        error_message = result_data.error_message
        main_data = result_data.main_data
        function_type = result_data.type.strip() if result_data.type is not None else ''
        main_view = result_data.main_view
        color = result_data.color

        match type:
            case 'error_message':
                return ResultItem(
                    control = ResultErrorMessage(error_message),
                    is_main = True
                )
            case ViewType.CHART:
                return ResultItem(
                    control = ResultChart(main_data, function_type, color),
                    is_main = main_view == ViewType.CHART,
                    button_name = f"Показать график: ***{function_type}***"
                )
            case ViewType.HISTOGRAM:
                return ResultItem(
                    control = ResultHistogram(main_data, function_type, color),
                    is_main = main_view == ViewType.HISTOGRAM,
                    button_name = f"Показать гистограмму: ***{function_type}***"
                )
            case ViewType.TABLE_HORIZONTAL:
                return ResultItem(
                    control = ResultTableHorizontal(main_data),
                    is_main = main_view == ViewType.TABLE_HORIZONTAL,
                    button_name = f"Показать таблицу данных: ***{function_type}***"
                )
            case ViewType.TABLE_VERTICAL:
                return ResultItem(
                    control = ResultTableVertical(main_data),
                    is_main = main_view == ViewType.TABLE_VERTICAL,
                    button_name = f"Показать таблицу статистических параметров: ***{function_type}***",
                )
            case ViewType.AUDIO:
                return ResultItem(
                    control = ResultAudio(self.function.page, main_data),
                    is_main = True, # main_view == ViewType.AUDIO,
                    button_name = f"Показать аудио: ***{function_type}***"
                )
            case 'extra_data':
                return ResultItem(
                    control = self._create_view_result(result_data),
                    button_name = f"Показать дополнительные данные:{(f' ***{function_type}***')}"
                )
            case 'initial_data':
                return ResultItem(
                    control = self._create_view_result(result_data),
                    button_name = f"Показать исходные данные:{(f' ***{function_type}***')}"
                )
            case _:
                raise ValueError(f'Недопустимый тип: {type}')
            

    def _create_view_list_result_item(self, result_items: List[ResultItem]) -> List:
        '''Создает список элементов результата, помещает неглавные представления в раскрывающийся контейнер'''
        return [
            item.control if item.is_main
            else ResultToggleContainer(item.control, item.button_name, item.is_open)
            for item in result_items
        ]
    

    def update_values(self) -> None:
        '''Обновляет представление результатов'''
        self.result_data = self.function.get_result()
        self.content = self.create_content()
        self.update()
        