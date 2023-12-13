from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .graphic_area import GraphicArea

from .function_attributes import *

from itertools import count
from copy import deepcopy
from typing import List
from pandas import DataFrame
from flet import Page, ContainerTapEvent, ControlEvent


class Function:
    id_counter = count()

    def __init__(self, page: Page, graphic_area: "GraphicArea", key: str):
        self.page = page
        self._graphic_area = graphic_area

        self.id = next(Function.id_counter)
        self.key = key
        self.config = FunctionLibrary.get_function_config_by_key(key)

        self.type = self.config.type
        self.name = self.config.name
        
        self.formatted_name: str = self._create_formatted_name()
        self.calculate_function_name = self.config.function.__name__

        self.color = self._get_random_color()

        self.calculate = FunctionCalculate(self)
        self.view = FunctionView(page, self)

        self.selected: bool = False                     # выбрана ли функция
        self.is_requires_dropdown_update: bool = self._is_update_required()   # требует ли обновление выпадающего списка функций
        self.list_dependent_from: List[Function] = []   # функции от которых зависит данная функция
        self.list_dependent_to: List[Function] = []     # функции которые зависят от данной
    

    def _create_formatted_name(self) -> str:
        '''Создает форматированное имя функции'''
        return f'{self.name} (id: {self.id}, type: {self.type})'
    

    def _is_update_required(self) -> bool:
        '''Проверяет требуется ли обновление выпадающего списка функций'''
        return any(param.type == ParameterType.DROPDOWN_FUNCTION_DATA for param in self.config.parameters.values())


    def get_result(self) -> ResultData:
        '''Возвращает результат вычисления функции'''
        return deepcopy(self.calculate.result)
    

    def get_result_main_data(self) -> DataFrame:
        '''Возвращает основные данные результата вычисления функции'''
        if self.calculate.result is not None:
            return deepcopy(self.calculate.result.main_data)
        return None


    def delete(self, e: ControlEvent) -> None:
        '''Вызывает метод удаления функции'''
        self.clear_dependencies()
        self._graphic_area.delete_function(self)


    def _on_click(self, e: ContainerTapEvent) -> None:
        '''Вызывает метод изменения выделения функции'''
        self._graphic_area.change_selected_function(self)


    def change_selection(self) -> None:
        '''Изменяет выделение функции'''
        self.selected = not self.selected
        self.view.change_selection()


    def update_view(self) -> None:
        '''Вызывает методы для обновления представлений'''
        self.view.update_view()
        self.recalculate_dependent_out_functions()


    def recalculate_dependent_out_functions(self) -> None:
        '''Вызывает методы для обновления функций, которые зависят от данной'''
        for function in self.list_dependent_to:
            function.recalculate_result()


    def recalculate_result(self) -> None:
        '''Вызывает метод для пересчета результата вычисления функции'''
        self.calculate.calculate()
        self.update_view()

    
    def update_dependencies_parameters(self) -> None:
        '''Вызывает методы для обновления параметров зависимых функций'''
        self.view.update_dependencies_parameters()
        for function in self.list_dependent_from:
            function.update_dependencies_parameters()


    def clear_dependencies(self):
        '''Очищает список зависимых функций'''
        for function in self.list_dependent_from:
            function.list_dependent_to.remove(self)
        for function in self.list_dependent_to:
            function.list_dependent_from.remove(self)

    
    def _get_random_color(self) -> str:
        '''Возвращает случайный цвет'''
        return Color.random()
    

    def update_color(self, color: str = None) -> None:
        '''Изменяет цвет функции'''
        if color is not None:
            self.color = color

            result = self.calculate.result
            if result is None:
                return
            result.color = color
            if result.extra_data is not None:
                for extra_data in result.extra_data:
                    extra_data.color = color

        self.view.update_color()

        # Обновляем зависимые функции чтобы в исходных данных
        # в результатах был правильный цвет
        if len(self.list_dependent_to):
            for function in self.list_dependent_to:
                function.recalculate_result()
    