from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..function import Function

from .view_function import *

from flet import Page


class FunctionView:
    def __init__(self, page: Page, function: "Function"):
        self.page = page
        self.function = function

        self.card_view = FunctionCardView(self.page, function)
        self.parameters_view = FunctionParametersView(function)
        self.results_view = FunctionResultView(function)


    def change_selection(self):
        '''Изменяет выделение функции'''
        self.card_view.change_selection()
        self.parameters_view.change_selection()
        self.results_view.change_selection()

    
    def update_view(self):
        '''Вызывает методы для обновления представлений'''
        self.card_view.update_values()
        self.results_view.update_values()


    def update_dependencies_parameters(self):
        '''Вызывает методы для обновления параметров зависимых функций'''
        self.parameters_view.update_dependencies_parameters()
    

    def update_color(self):
        '''Вызывает методы для обновления цвета'''
        self.results_view.update_values()
        self.card_view.update_color()
        