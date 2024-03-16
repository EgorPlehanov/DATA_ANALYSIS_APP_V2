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
                    function = lambda bool_val_2: {"param_1": bool_val_2},
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

                                FilePickerParamConfig(key="image", name="Фото"),
                                SingleValueParamConfig(key="multiply_constant", name="Умножить на", default_value=2),
                            ]
                        ),

                        NodeConfig(
                            key = "shift_image",
                            name = "Сдвиг изображения по осям",
                            icon = icons.IMAGE,
                            color = colors.GREEN_700,
                            function = shift_image,
                            parameters = [
                                OutParamConfig(
                                    key="shifted_image", name="Shifted image",
                                    connect_point_color=colors.DEEP_PURPLE_ACCENT_700
                                ),

                                FilePickerParamConfig(key="image", name="Фото"),
                                SingleValueParamConfig(
                                    key="dx", name="Горизонтальный сдвиг",
                                    default_value=30, min_value=0, decimal_accuracy=0
                                ),
                                SingleValueParamConfig(
                                    key="dy", name="Вертикальный сдвиг",
                                    default_value=30, min_value=0, decimal_accuracy=0
                                ),
                            ]

                        )
                    ]
                ),

                Folder(
                    name = "Лабораторная 2",
                    icon = icons.LABEL,
                    obj_list = [
                        NodeConfig(
                            key = "apply_grayscale_scaling",
                            name = "Шкалирование серого цвета",
                            icon = icons.IMAGE,
                            color = colors.LIME,
                            function = apply_grayscale_scaling,
                            parameters = [
                                OutParamConfig(
                                    key="grayscale_image", name="Grayscale image",
                                    connect_point_color=colors.DEEP_PURPLE_ACCENT_700
                                ),

                                FilePickerParamConfig(key="image", name="Фото"),
                                SingleValueParamConfig(
                                    key="scale_size", name="Масштаб",
                                    min_value=0, decimal_accuracy=0, default_value=255, 
                                ),
                            ]
                        )
                    ]
                ),

                Folder(
                    name = "Лабораторная 3",
                    icon = icons.LABEL,
                    obj_list = [
                        NodeConfig(
                            key = "resize_nearest_neighbor",
                            name = "Масштабирование методом ближайшего соседа (ПАКЕТНАЯ)",
                            icon = icons.IMAGE,
                            color = colors.TEAL,
                            function = resize_nearest_neighbor,
                            parameters = [
                                OutParamConfig(
                                    key="resized_image", name="Resized image",
                                    connect_point_color=colors.DEEP_PURPLE_ACCENT_700
                                ),

                                FilePickerParamConfig(key="image", name="Фото"),
                                SingleValueParamConfig(
                                    key="scale_factor", name="Масштаб",
                                    min_value=0.00001, default_value=2
                                ),
                            ]
                        ),

                        
                        NodeConfig(
                            key = "resize_nearest_neighbor_manual",
                            name = "Масштабирование методом ближайшего соседа (АЛГОРИТМ)",
                            icon = icons.IMAGE,
                            color = colors.TEAL,
                            function = resize_nearest_neighbor_manual,
                            parameters = [
                                OutParamConfig(
                                    key="resized_image", name="Resized image",
                                    connect_point_color=colors.DEEP_PURPLE_ACCENT_700
                                ),

                                FilePickerParamConfig(key="image", name="Фото"),
                                SingleValueParamConfig(
                                    key="scale_factor", name="Масштаб",
                                    min_value=0.00001, default_value=2
                                ),
                            ]
                        ),
                        
                        NodeConfig(
                            key = "resize_bilinear_interpolation",
                            name = "Масштабирование методом билинейной интерполяции (ПАКЕТНАЯ)",
                            icon = icons.IMAGE,
                            color = colors.TEAL,
                            function = resize_bilinear_interpolation,
                            parameters = [
                                OutParamConfig(
                                    key="resized_image", name="Resized image",
                                    connect_point_color=colors.DEEP_PURPLE_ACCENT_700
                                ),

                                FilePickerParamConfig(key="image", name="Фото"),
                                SingleValueParamConfig(
                                    key="scale_factor", name="Масштаб",
                                    min_value=0.00001, default_value=2
                                ),
                            ]
                        ),

                        NodeConfig(
                            key = "resize_bilinear_interpolation_manual",
                            name = "Масштабирование методом билинейной интерполяции (АЛГОРИТМ)",
                            icon = icons.IMAGE,
                            color = colors.TEAL,
                            function = resize_bilinear_interpolation_manual,
                            parameters = [
                                OutParamConfig(
                                    key="resized_image", name="Resized image",
                                    connect_point_color=colors.DEEP_PURPLE_ACCENT_700
                                ),

                                FilePickerParamConfig(key="image", name="Фото"),
                                SingleValueParamConfig(
                                    key="scale_factor", name="Масштаб",
                                    min_value=0.00001, default_value=2
                                ),
                            ]
                        ),

                        NodeConfig(
                            key = "rotate_image_90_degrees",
                            name = "Повернуть изображение кратно 90°",
                            icon = icons.IMAGE,
                            color = colors.TEAL,
                            function = rotate_image_90_degrees,
                            parameters = [
                                OutParamConfig(
                                    key="rotate_image", name="Rotated image",
                                    connect_point_color=colors.DEEP_PURPLE_ACCENT_700
                                ),

                                FilePickerParamConfig(key="image", name="Фото"),
                                # SingleValueParamConfig(
                                #     key="angle", name="Угол (°)",
                                #     decimal_accuracy=0, default_value = 90
                                # ),
                                DropdownValueParamConfig(
                                    key="angle", name="Угол",
                                    default_value = 90,
                                    options = [
                                        DropdownOptionItem(key=90, text="90°"),
                                        DropdownOptionItem(key=180, text="180°"),
                                        DropdownOptionItem(key=270, text="270°"),
                                        DropdownOptionItem(key=360, text="360°"),
                                    ]
                                ),
                            ]
                        ),

                        NodeConfig(
                            key = "rotate_image",
                            name = "Повернуть изображение (ПАКЕТНАЯ)",
                            icon = icons.IMAGE,
                            color = colors.TEAL,
                            function = rotate_image,
                            parameters = [
                                OutParamConfig(
                                    key="rotate_image", name="Rotated image",
                                    connect_point_color=colors.DEEP_PURPLE_ACCENT_700
                                ),

                                FilePickerParamConfig(key="image", name="Фото"),
                                SingleValueParamConfig(
                                    key="angle", name="Угол (°)",
                                    default_value = 90
                                ),
                            ]
                        ),

                        NodeConfig(
                            key = "rotate_image_manual",
                            name = "Повернуть изображение (АЛГОРИТМ)",
                            icon = icons.IMAGE,
                            color = colors.TEAL,
                            function = rotate_image_manual,
                            parameters = [
                                OutParamConfig(
                                    key="rotate_image", name="Rotated image",
                                    connect_point_color=colors.DEEP_PURPLE_ACCENT_700
                                ),

                                FilePickerParamConfig(key="image", name="Фото"),
                                SingleValueParamConfig(
                                    key="angle", name="Угол (°)",
                                    default_value = 90
                                ),
                                BoolValueParamConfig(key="resize", name="Изменять размер", default_value = False),
                            ]
                        ),
                        
                    ]
                ),

                Folder(
                    name = "Лабораторная 4",
                    icon = icons.LABEL,
                    obj_list = [
                        NodeConfig(
                            key = "negative_transformation",
                            name = "Негативное градационное преобразование",
                            icon = icons.IMAGE,
                            color = colors.PINK,
                            function = negative_transformation,
                            parameters = [
                                OutParamConfig(
                                    key="negative_image", name="Negative image",
                                    connect_point_color=colors.DEEP_PURPLE_ACCENT_700
                                ),

                                FilePickerParamConfig(key="image", name="Фото"),
                            ]
                        ),
                        
                        NodeConfig(
                            key = "gamma_correction",
                            name = "Гамма-преобразование",
                            icon = icons.IMAGE,
                            color = colors.PINK,
                            function = gamma_correction,
                            parameters = [
                                OutParamConfig(
                                    key="gamma_image", name="Gamma image",
                                    connect_point_color=colors.DEEP_PURPLE_ACCENT_700
                                ),

                                FilePickerParamConfig(key="image", name="Фото"),
                                SingleValueParamConfig(
                                    key="gamma", name="Гамма", default_value = 1.0
                                ),
                                SingleValueParamConfig(
                                    key="constant", name="Константа", default_value = 1
                                )
                            ]
                        ),
                        
                        NodeConfig(
                            key = "logarithmic_transformation",
                            name = "Логарифмическое градационное преобразование",
                            icon = icons.IMAGE,
                            color = colors.PINK,
                            function = logarithmic_transformation,
                            parameters = [
                                OutParamConfig(
                                    key="logarithmic_image", name="Logarithmic image",
                                    connect_point_color=colors.DEEP_PURPLE_ACCENT_700
                                ),

                                FilePickerParamConfig(key="image", name="Фото"),
                                SingleValueParamConfig(
                                    key="constant", name="Константа", default_value = 1
                                )
                            ]
                        ),
                        
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