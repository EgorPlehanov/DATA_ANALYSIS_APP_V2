from flet import *
from itertools import count

from .function_attributes import *


class Function:
    id_counter = count()

    def __init__(self, graphic_area, function_key):
        self._graphic_area = graphic_area

        self.id = next(Function.id_counter)
        self.function_key = function_key
        self.function_config = FunctionLibrary.get_function_config_by_key(function_key)

        self.calculate = FunctionCalculate(self)
        self.view = FunctionView(self)
  