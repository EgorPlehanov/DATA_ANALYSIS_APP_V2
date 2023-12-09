from .function_attributes import *

from flet import Page
from itertools import count
from copy import deepcopy
from typing import List
from pandas import DataFrame


class Function:
    id_counter = count()

    def __init__(self, page: Page, graphic_area, key):
        self.page = page
        self._graphic_area = graphic_area

        self.id = next(Function.id_counter)
        self.key = key
        self.config = FunctionLibrary.get_function_config_by_key(key)

        self.type = self.config.type
        self.name = self.config.name
        
        self.formatted_name: str = self._create_formatted_name()
        self.calculate_function_name = self.config.function.__name__

        self.calculate = FunctionCalculate(self)
        self.view = FunctionView(page, self)

        self.selected: bool = False                     # выбрана ли функция
        self.is_requires_dropdown_update: bool = self._is_update_required()   # требует ли обновление выпадающего списка функций
        self.list_dependent_in: List[Function] = []     # функции от которых зависит данная функция
        self.list_dependent_out: List[Function] = []    # функции которые зависят от данной
    

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
        return deepcopy(self.calculate.result.main_data)
    

    def delete(self, e) -> None:
        '''Вызывает метод удаления функции'''
        self._graphic_area.delete_function(self)


    def _on_click(self, e) -> None:
        '''Вызывает метод изменения выделения функции'''
        self._graphic_area.change_selected_function(self)


    def change_selection(self) -> None:
        '''Изменяет выделение функции'''
        self.selected = not self.selected
        self.view.change_selection()


    def update_view(self) -> None:
        '''Вызывает методы для обновления представлений'''
        self.view.update_view()

    
    def update_dependencies_parameters(self):
        '''Вызывает методы для обновления параметров зависимых функций'''
        self.view.update_dependencies_parameters()
    