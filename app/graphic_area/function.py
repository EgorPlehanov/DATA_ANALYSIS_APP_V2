from .function_attributes import *

from flet import *
from itertools import count


class Function:
    id_counter = count()

    def __init__(self, graphic_area, key):
        self._graphic_area = graphic_area

        self.id = next(Function.id_counter)
        self.key = key
        self.config = FunctionLibrary.get_function_config_by_key(key)

        self.type = self.config.type
        self.name = self.config.name

        
        self.formatted_name = self._create_formatted_name()
        self.calculate_function_name = self.config.function.__name__

        self.calculate = FunctionCalculate(self)
        self.view = FunctionView(self)
    

    def _create_formatted_name(self):
        return f'{self.name} (id: {self.id}, type: {self.type})'
    