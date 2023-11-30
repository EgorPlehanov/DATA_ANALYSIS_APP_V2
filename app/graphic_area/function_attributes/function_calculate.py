from calculate_functions.function_library import FunctionLibrary


class FunctionCalculate:
    def __init__(self, function):
        self.function = function

        self.calculate_function = FunctionLibrary.get_function_config_attribut_by_funcname_atribute(
            function.function_name,
            'function'
        )

        

    
        



