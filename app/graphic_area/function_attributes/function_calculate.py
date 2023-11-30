from .calculate_functions.function_library import FunctionLibrary


class FunctionCalculate:
    def __init__(self, function):
        self.function = function

        self.calculate_function = FunctionLibrary.get_function_config_attribut_by_funcname_atribute(
            function.function_name,
            'function'
        )
        self.parameters_default_values = FunctionLibrary.get_function_config_parameters_default_values_by_name(
            function.function_name
        )


    def set_default_parameters(self):
        for param_name, param_value in self.parameters_default_values.items():
            self.set_parameter_value(param_name, param_value)

    
        



