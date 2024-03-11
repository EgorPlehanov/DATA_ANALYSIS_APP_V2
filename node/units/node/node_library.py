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

                        SVParamConfig(name = "Param 2", connect_point_color = "red"),
                        SVParamConfig(name = "Param 3", connect_point_color = "orange", has_connect_point = False),
                    ]
                ),

                NodeConfig(
                    key = "test3",
                    name = "Тестовая 3->2",
                    parameters = [
                        OutParamConfig(name = "Param 1", connect_point_color = "green"),
                        OutParamConfig(name = "Param 2", connect_point_color = "blue"),

                        SVParamConfig(name = "Param 3", connect_point_color = "red"),
                        SVParamConfig(name = "Param 4", connect_point_color = "orange"),
                        BVParamConfig(key="bool_val3", name="Bool tristate", default_value = True, is_tristate = True),
                        BVParamConfig(key="bool_val4", name="Bool", default_value = True),
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

                        SVParamConfig(key = "min_value", name = "Min"),
                        SVParamConfig(key = "max_value", name = "Max"),
                        SVParamConfig(
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

                        SVParamConfig(key = "a", name = "A"),
                        SVParamConfig(key = "b", name = "B"),
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
            parameters = [
                TakeValueParamConfig(key = "result", name = "Result"),
            ]
        )
    ]