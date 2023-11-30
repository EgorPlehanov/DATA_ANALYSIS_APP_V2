from .view_function import *


class FunctionView:
    def __init__(self, function):
        self._function = function

        self.card_view = FunctionCardView(function)
        self.parameters_view = FunctionParametersView(function)
        self.results_view = FunctionResultView(function)
