from .calculate_functions.function_library import FunctionLibrary


class FunctionCalculate:
    def __init__(self, function):
        self.function = function

        self.calculate_function = FunctionLibrary.get_function_config_attribute_by_key_attribute(
            function.function_key,
            'function'
        )
        self.parameters_default_values = FunctionLibrary.get_function_config_parameters_default_values_by_key(
            function.function_key
        )


    def set_default_parameters(self):
        for name, value in self.parameters_default_values.items():
            setattr(self, name, value)

    
        



