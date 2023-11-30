from flet import *

from itertools import count
from .function_attributes.function_view import FunctionView

class Function:
    id_counter = count()

    def __init__(self, graphic_area, function_name):
        self.function_id = next(Function.id_counter)
        self._graphic_area = graphic_area

        # self.aggregation = 
        # self.view = FunctionView(self)
        self.view = Container(
            bgcolor=colors.BLUE,
            content=Text(f'Function {self.function_id}'),
        )





from dataclasses import dataclass
from typing import (List, Optional)
from pandas import DataFrame






class AggregationFunction:
    def __init__(self):
        pass



# class FunctionLibrary:
    