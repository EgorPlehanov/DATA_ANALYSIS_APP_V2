from .node import *
from ..folder import *



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
                    key = "add",
                    name = "add",
                    icon = icons.ADD,
                    function = lambda a, b: {'sum': a + b},
                    parameters = [
                        OutParamConfig(name = "sum", connect_point_color = "green"),

                        SVParamConfig(name = "a"),
                        SVParamConfig(name = "b", min_value=-100, max_value=100),
                    ]
                ),

                NodeConfig(
                    key = "test2",
                    name = "Тестовая 2->1",
                    parameters = [
                        OutParamConfig(name = "Param ", connect_point_color = "green"),

                        SVParamConfig(name = "Param ", connect_point_color = "red"),
                        SVParamConfig(name = "Param ", connect_point_color = "orange", has_connect_point = False),
                    ]
                ),

                NodeConfig(
                    key = "test3",
                    name = "Тестовая 3->2",
                    parameters = [
                        OutParamConfig(name = "Param ", connect_point_color = "green"),
                        OutParamConfig(name = "Param ", connect_point_color = "blue"),

                        SVParamConfig(name = "Param ", connect_point_color = "red"),
                        SVParamConfig(name = "Param ", connect_point_color = "orange"),
                        SVParamConfig(name = "Param ", connect_point_color = "purple"),
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
                    function = None,
                    parameters = [
                        OutParamConfig(name = "Image", connect_point_color = colors.BLUE_ACCENT),

                        # TODO: добавить параметр выбора файла
                    ]
                ),

                NodeConfig(
                    key = "image_library",
                    name = "Библиотека изображений",
                    icon = icons.IMAGE_SEARCH,
                    color = colors.BLACK,
                    width = 300,
                    function = None,
                    parameters = [
                        OutParamConfig(name = "Image", connect_point_color = colors.BLUE_ACCENT),

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
                    function = None,
                    parameters = [
                        OutParamConfig(name = "Value", connect_point_color = colors.BLUE_ACCENT_200),

                        SVParamConfig(name = "Min"),
                        SVParamConfig(name = "Max"),
                    ]
                )
            ]
        ),

        NodeConfig(
            key = "output",
            name = "Вывести результат",
            icon = icons.SEND,
            color = colors.BLACK,
            function = None,
            parameters = [
                # TODO: добавить параметр который будет только принимать
            ]
        )
    ]