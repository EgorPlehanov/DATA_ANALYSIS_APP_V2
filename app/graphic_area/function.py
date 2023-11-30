from flet import *
from itertools import count

from function_attributes import *


class Function:
    id_counter = count()

    def __init__(self, graphic_area, function_name):
        self._graphic_area = graphic_area

        self.id = next(Function.id_counter)
        self.function_name = function_name

        self.calculate = FunctionCalculate(self)
        self.view = FunctionView(self)
  