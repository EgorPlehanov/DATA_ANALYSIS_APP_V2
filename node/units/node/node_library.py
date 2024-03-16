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
                    key = "test3",
                    name = "Тестовая 3->2",
                    parameters = [
                        OutParamConfig(name = "Param 1", connect_point_color = "green"),
                        OutParamConfig(name = "Param 2", connect_point_color = "blue"),

                        SingleValueParamConfig(name = "Param 3", connect_point_color = "red"),
                        SingleValueParamConfig(name = "Param 4", connect_point_color = "orange"),

                        BoolValueParamConfig(
                            key="bool_val_1", name="Bool tristate",
                            default_value = None, is_tristate = True
                        ),
                        BoolValueParamConfig(key="bool_val_2", name="Bool", default_value = True),

                        TextValueParamConfig(key="text", name="Text", default_value = "Test"),

                        FilePickerParamConfig(key="file_1", name="File 1"),
                        FilePickerParamConfig(
                            key="file_2", name="File 2",
                            default_value = File('D:\\POLITEH\\DATA_ANALYSIS_APP_V2\\DATA\\jpg\\grace.jpg')
                        ),

                        DropdownValueParamConfig(
                            key="dropdown_1", name="Dropdown 1",
                            # default_value = "A",
                            options = [
                                DropdownOptionItem(key="A", text="Aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"),
                                DropdownOptionItem(key="B", text="B"),
                                DropdownOptionItem(key="C", text="C"),
                            ]
                        ),
                        DropdownValueParamConfig(
                            key="dropdown_2", name="Dropdown 2",
                            include_none = True,
                            options = [
                                DropdownOptionItem(key="B", text="B"),
                                DropdownOptionItem(key="C", text="C"),
                            ]
                        )
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
                    function = open_image_file,
                    parameters = [
                        OutParamConfig(
                            key = "image", name = "Изображение",
                            connect_point_color=colors.DEEP_PURPLE_ACCENT_700
                        ),

                        FilePickerParamConfig(key="image_file", name="Файл", default_value = None),
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
                        OutParamConfig(
                            key = "image", name = "Image",
                            connect_point_color = colors.DEEP_PURPLE_ACCENT_700
                        ),

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
                        OutParamConfig(key = "sum", name = "Sum", connect_point_color = colors.BLUE_ACCENT_200),

                        SingleValueParamConfig(key = "a", name = "A"),
                        SingleValueParamConfig(key = "b", name = "B"),
                    ]
                ),
            ]
        ),

        Folder(
            name = "Лабораторные",
            icon = icons.ASSIGNMENT_OUTLINED,
            obj_list = [
                Folder(
                    name = "Лабораторная 1",
                    icon = icons.LABEL,
                    obj_list = [
                        NodeConfig(
                            key = "shift_image_by_constant",
                            name = "Сдвиг изображения",
                            icon = icons.IMAGE,
                            color = colors.GREEN_700,
                            function = shift_image_by_constant,
                            parameters = [
                                OutParamConfig(
                                    key="shifted_image", name="Shifted image",
                                    connect_point_color=colors.DEEP_PURPLE_ACCENT_700
                                ),
                                
                                FilePickerParamConfig(key="image", name="Фото", default_value = None),
                                SingleValueParamConfig(key="shift_constant", name="Сдвиг", default_value=30),
                            ]
                        ),

                        NodeConfig(
                            key = "multiply_image_by_constant",
                            name = "Умножение изображения",
                            icon = icons.IMAGE,
                            color = colors.GREEN_700,
                            function = multiply_image_by_constant,
                            parameters = [
                                OutParamConfig(
                                    key="multiply_image", name="Multiply_image",
                                    connect_point_color=colors.DEEP_PURPLE_ACCENT_700
                                ),

                                FilePickerParamConfig(key="image", name="Фото", default_value = None),
                                SingleValueParamConfig(key="multiply_constant", name="Умножить на", default_value=2),
                            ]
                        ),
                    ]
                ),

                Folder(
                    name = "Лабораторная 2",
                    icon = icons.LABEL,
                    obj_list = [
                        
                    ]
                ),

                Folder(
                    name = "Лабораторная 3",
                    icon = icons.LABEL,
                    obj_list = [
                        
                    ]
                ),

                Folder(
                    name = "Лабораторная 4",
                    icon = icons.LABEL,
                    obj_list = [
                        
                    ]
                ),

                Folder(
                    name = "Лабораторная 5",
                    icon = icons.LABEL,
                    obj_list = [
                        
                    ]
                )
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