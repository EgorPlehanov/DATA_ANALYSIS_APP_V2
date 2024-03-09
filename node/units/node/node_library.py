from .node import *
from ..typing import *



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

                        SVParamConfig(name = "a", connect_point_color = "red"),
                        SVParamConfig(name = "b", connect_point_color = "orange"),
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
        
       
    ]