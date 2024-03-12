from .node import *
from ..folder import *
from .calculate_function import *



class NodeLibrary:
    @staticmethod
    def get_nodes_configs() -> List[NodeConfig]:
        return NodeLibrary.nodes_configs


    nodes_configs = [
        Folder(
            name = "Test",
            icon = icons.QUESTION_MARK,
            obj_list = [

                NodeConfig(
                    key = "test2",
                    name = "Тестовая 2->1",
                    parameters = [
                        OutParamConfig(name = "Param 1", connect_point_color = "green"),

                        SingleValueParamConfig(name = "Param 2", connect_point_color = "red"),
                        SingleValueParamConfig(name = "Param 3", connect_point_color = "orange", has_connect_point = False),
                    ]
                ),

                NodeConfig(
                    key = "test3",
                    name = "Тестовая 3->2",
                    parameters = [
                        OutParamConfig(name = "Param 1", connect_point_color = "green"),
                        OutParamConfig(name = "Param 2", connect_point_color = "blue"),

                        SingleValueParamConfig(name = "Param 3", connect_point_color = "red"),
                        SingleValueParamConfig(name = "Param 4", connect_point_color = "orange"),

                        BoolValueParamConfig(
                            key="bool_val_1", name="Bool tristate",
                            default_value = True, is_tristate = True
                        ),
                        BoolValueParamConfig(key="bool_val_2", name="Bool", default_value = True),

                        TextValueParamConfig(key="text", name="Text", default_value = "Test"),
                    ]
                ),

            ]
        ),

        Folder(
            name = "Данные",
            icon = icons.DATA_ARRAY,
            obj_list = [
                NodeConfig(
                    key = "open_image",
                    name = "Открыть изображение",
                    icon = icons.IMAGE,
                    color = colors.BLACK,
                    width = 300,
                    # function = None,
                    parameters = [
                        OutParamConfig(key = "image", name = "Image", connect_point_color = colors.BLUE_ACCENT),

                        # TODO: добавить параметр выбора файла
                    ]
                ),

                NodeConfig(
                    key = "image_library",
                    name = "Библиотека изображений",
                    icon = icons.IMAGE_SEARCH,
                    color = colors.BLACK,
                    width = 300,
                    # function = None,
                    parameters = [
                        OutParamConfig(key = "image", name = "Image", connect_point_color = colors.BLUE_ACCENT),

                        # TODO: добавить параметр выбора файла из библиотеки (сохраненной в проекте)
                    ]
                )
            ]
        ),
        
        Folder(
            name = "Математические",
            icon = icons.FUNCTIONS,
            obj_list = [
                NodeConfig(
                    key = "random_value",
                    name = "Случайное значение",
                    icon = icons.CASINO,
                    color = colors.BLUE_700,
                    function = random_value,
                    parameters = [
                        OutParamConfig(key = "value", name = "Value", connect_point_color = colors.BLUE_ACCENT_200),

                        SingleValueParamConfig(key = "min_value", name = "Min"),
                        SingleValueParamConfig(key = "max_value", name = "Max"),
                        SingleValueParamConfig(
                            key = "decimal_accuracy", name = "Десятичная точность",
                            decimal_accuracy = 0, default_value = 3,
                            min_value = -1, max_value = 10
                        ),
                    ]
                ),
                
                NodeConfig(
                    key = "add",
                    name = "Cумма двух чисел",
                    icon = icons.ADD,
                    function = add_two_numbers,
                    parameters = [
                        OutParamConfig(key = "sum", name = "Sum", connect_point_color = "green"),

                        SingleValueParamConfig(key = "a", name = "A"),
                        SingleValueParamConfig(key = "b", name = "B"),
                    ]
                ),
            ]
        ),

        NodeConfig(
            key = "display_result",
            name = "Вывести результат",
            icon = icons.SEND,
            color = colors.BLACK,
            function = display_result,
            is_display_result = True,
            parameters = [
                TakeValueParamConfig(key = "result", name = "Result"),
                TextValueParamConfig(key="label", name="Label", hint_text = "Название результата..."),
            ]
        )
    ]