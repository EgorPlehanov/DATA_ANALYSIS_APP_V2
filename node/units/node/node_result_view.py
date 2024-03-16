from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .node import Node

from flet import *
import cv2
import base64

from .calculate_function.calculate_function_typing import *



class NodeResultView(Container):
    '''
    Виджет для отображения результата вычисления узла
    '''
    def __init__(self, node: "Node", result_dict: dict = {}):
        super().__init__()
        self.node = node
        self.result_dict = result_dict

        self.set_style()

        self.content = self._create_content()


    def set_style(self):
        '''
        Устанавливает стиль
        '''
        self.set_result_value()
        

        self.border_radius = 10
        self.bgcolor = colors.BLACK26
        self.padding = padding.only(left=10, top=10, right=10, bottom=10)


    def set_result_value(self):
        """
        Устанавливает значение результата
        """
        self.current_time = self.result_dict.get("current_time", None) if self.result_dict is not None else None
        self.label = self.result_dict.get("label", None) if self.result_dict is not None else None
        self.result: NodeResult = self.result_dict.get("result", None) if self.result_dict is not None else None
        self.result_type = self.result.type if isinstance(self.result, NodeResult) else ResultType.NONE
        self.result_value = self.result.value if isinstance(self.result, NodeResult) else None


    def _create_content(self):
        '''
        Создает содержимое
        '''
        value_type_to_view = {
            ResultType.NONE:         self.create_none_view_element,
            ResultType.STR_VALUE:    self.create_str_view_element,
            ResultType.NUMBER_VALUE: self.crate_num_view_element,
            ResultType.IMAGE_CV2:    self.crate_image_cv2_view_element,
            ResultType.IMAGE_BASE64: self.crate_image_base64_view_element,
            ResultType.HISTOGRAM:    self.crate_histogram_view_element,
        }
        result_title = self.create_result_title()
        result_body = value_type_to_view[self.result_type]()
        return Column([
            result_title,
            result_body
        ])
    

    def create_result_title(self):
        """
        Создает заголовок результата
        """
        title = (self.current_time if self.current_time else "") + (": " + self.label if self.label else "")
        return Container(
            content = Row(
                alignment = MainAxisAlignment.CENTER,
                controls = [Text(
                    value = title,
                    weight = FontWeight.BOLD,
                    size = 20,
                    text_align = TextAlign.CENTER
                )]
            ),
        )
    

    def create_none_view_element(self):
        """
        Создает элемент для отображения None
        """
        return Container(
            content = Text(
                value = "Нет данных",
            )
        )
    

    def create_str_view_element(self):
        """
        Создает элемент для отображения строки
        """
        return Container(
            content = Text(
                value = self.result_value,
            )
        )


    def crate_num_view_element(self):
        """
        Создает элемент для отображения числа
        """
        return self.create_str_view_element()
    

    def crate_image_cv2_view_element(self):
        """
        Создает элемент для отображения изображения
        """
        print("crate_image_cv2_view_element", self.result_value)
        return Image(
            src_base64 = self.image_to_base64(self.result_value),
            border_radius = border_radius.all(10),
            fit = ImageFit.FIT_WIDTH
        )
    
    def crate_image_base64_view_element(self):
        """
        Создает элемент для отображения изображения
        """
        return Image(
            src_base64 = self.result_value,
            border_radius = border_radius.all(10),
            fit = ImageFit.FIT_WIDTH,
        )
    

    def crate_histogram_view_element(self):
        """
        Создает элемент для отображения гистограммы
        """
        return Row([])


    def image_to_base64(self, image):
        # Загрузка изображения
        if image is None:
            return None
        if isinstance(image, str):
            image = cv2.imread(image)
        
        # Кодирование изображения в формате base64
        _, buffer = cv2.imencode('.jpg', image)
        base64_image = base64.b64encode(buffer).decode('utf-8')
        
        return base64_image
    

    def update_result(self, result_dict: dict):
        """
        Обновляет содержимое
        """
        self.result_dict = result_dict
        self.set_result_value()
        self.content = self._create_content()
