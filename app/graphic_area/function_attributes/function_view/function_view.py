from .function_card_view import FunctionCardView


class FunctionView:
    def __init__(self, function):
        self._function = function

        self.card_view = FunctionCardView(function)
        self.parameters_view = None
        self.results_view = None