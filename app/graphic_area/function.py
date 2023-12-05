from .function_attributes import *

from flet import Page
from itertools import count
from copy import deepcopy

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
        
        self.formatted_name = self._create_formatted_name()
        self.calculate_function_name = self.config.function.__name__

        self.calculate = FunctionCalculate(self)
        self.view = FunctionView(page, self)

        self.selected = False
    

    def _create_formatted_name(self):
        '''Создает форматированное имя функции'''
        return f'{self.name} (id: {self.id}, type: {self.type})'
    

    def get_result(self):
        '''Возвращает результат вычисления функции'''
        return deepcopy(self.calculate.result)
    

    def get_result_main_data(self):
        '''Возвращает основные данные результата вычисления функции'''
        return deepcopy(self.calculate.result.main_data)
    

    def delete(self, e):
        '''Вызывает метод удаления функции'''
        self._graphic_area.delete_function(self)


    def _on_click(self, e):
        '''Вызывает метод изменения выделения функции'''
        self._graphic_area.change_selected_function(self)


    def change_selection(self):
        '''Изменяет выделение функции'''
        self.selected = not self.selected
        self.view.change_selection()