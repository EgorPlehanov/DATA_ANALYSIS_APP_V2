from .view_function import *

from flet import Page


class FunctionView:
    def __init__(self, page: Page, function):
        self.page = page
        self.function = function

        self.card_view = FunctionCardView(self.page, function)
        self.parameters_view = FunctionParametersView(function)
        self.results_view = FunctionResultView(function)


    def change_selection(self):
        self.card_view.change_selection()
        self.parameters_view.change_selection()
        self.results_view.change_selection()