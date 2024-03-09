from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .node_area import NodeArea

from flet import *
from itertools import count
from typing import Callable, List, Dict
from dataclasses import dataclass, field
import math

from .node_typing import Color
from .node_connect_point import NodeConnectPoint
from .node_typing import NodeConnect 
from ..parameters.parametrs_dict import *



@dataclass
class NodeConfig:
    """
    Конфигурация узла
    
    key - ключ узла
    name - название узла
    group - группа узла
    color - цвет узла
    left - позиция узла по оси x
    enabled - активен ли узел
    function - функция узла
    parameters - параметры узла
    x - координата x узла
    y - координата y узла
    """
    key: str                = "unknown"
    name: str               = "Untitled"
    icon: str               = None
    group: str              = "Default"
    color: str              = Color.random()
    left: int               = 20
    top: int                = 20
    width: int              = 250
    enabled: bool           = True
    function: Callable      = lambda: None
    parameters: Dict | List = field(default_factory=list)
    
    
    def __post_init__(self):
        for attr in ("key", "name", "group"):
            value = getattr(self, attr)
            if not isinstance(value, str) or not value:
                try:
                    setattr(self, attr, str(value))
                except ValueError:
                    raise ValueError(f"Недопустимый тип {attr}: {type(value)}")
        # if not isinstance(self.parameters, dict):
        #     if isinstance(self.parameters, list):
        #         self.parameters = {param.name: param for param in self.parameters}
        #     else:
        #         raise ValueError(f'Недопустимый тип parameters функции: {type(self.parameters)}')



class Node(GestureDetector):
    id_counter = count()

    HEADER_HEIGHT = 30
    BORDER_RADIUS = HEADER_HEIGHT // 2
    BORDER_WIDTH = 1

    POINT_SIZE = 12
    POINT_BORDER_WIDTH = 1

    CONTENT_MARGIN = POINT_SIZE // 2
    PARAM_PADDING = 5

    NODE_BGCOLOR = colors.with_opacity(0.90, colors.GREY_900)
    NODE_BORDER_COLOR = colors.BLACK87
    NODE_SELECT_BGCOLOR = colors.GREY_800
    NODE_SELECT_BORDER_COLOR = colors.DEEP_ORANGE_ACCENT_400
    NODE_SHADOW_COLOR = colors.BLACK38

    HEADER_ICON_COLOR = colors.WHITE
    HEADER_SHADOW_COLOR = colors.BLACK26


    def __init__(self, page: Page, node_area: "NodeArea", scale = 1,
        config: NodeConfig = NodeConfig()
    ):
        super().__init__()
        self.page = page
        self.node_area = node_area
        self.config = config

        self.setup_values()

        self.scale = scale
        
        self.connects: List[NodeConnect] = []

        self.header = self.create_header()
        self.parameters = self.create_parameters()
        
        self.height = self.get_height()

        self.connect_points = self.create_contact_points_list()
        self.content = self.create_content()


    def setup_values(self):
        """
        Устанавливает значения по умолчанию
        """
        self.id = next(Node.id_counter)
        self.mouse_cursor = MouseCursor.CLICK
        self.drag_interval = 20
        self.on_pan_update = self.on_drag
        self.on_tap = self.toggle_selection

        self.is_open = True
        self.is_selected = False

        self.name = self.config.name

        self.left = self.config.left
        self.top = self.config.top

        self.width = self.config.width

        self.header_color = self.config.color

        self.function = self.config.function


    def get_height(self):
        """
        Возвращает высоту карточки узла
        """
        if self.is_open:
            return self.get_height_content() + self.POINT_SIZE * 1.5
        else:
            return self.HEADER_HEIGHT + self.POINT_SIZE
            
    
    def get_height_content(self):
        """
        Возвращает высоту контента карточки узла
        """
        return self.HEADER_HEIGHT + self.PARAM_PADDING * 2 + self.get_height_parameters()


    def get_height_parameters(self):
        """
        Возвращает высоту параметров
        """
        return sum(param.height for param in self.parameters_list)
    

    def get_width_content(self):
        """
        Возвращает ширину контента карточки узла
        """
        return self.width - self.POINT_SIZE
    

    def create_content(self):
        """
        Создает карточку узла
        """
        self.ref_content_conteiner = Ref[Container]()
        return Stack(
            [
                Container(
                    ref = self.ref_content_conteiner,
                    content = Column(
                        controls = [
                            self.header,
                            self.parameters
                        ],
                        spacing = 0,
                    ),
                    # height = self.get_height_content(),
                    width = self.get_width_content(),
                    left = self.CONTENT_MARGIN,
                    top = self.CONTENT_MARGIN,
                    visible = self.is_open,
                    bgcolor = self.NODE_BGCOLOR,
                    border_radius = border_radius.all(self.BORDER_RADIUS),
                    border = border.all(self.BORDER_WIDTH, self.NODE_BORDER_COLOR),
                    animate_size = animation.Animation(200, AnimationCurve.FAST_OUT_SLOWIN),
                    shadow = BoxShadow(
                        spread_radius = 0,
                        blur_radius = 5,
                        color = self.NODE_SHADOW_COLOR,
                        offset = Offset(0, 5),
                        blur_style = ShadowBlurStyle.NORMAL,
                    )
                ),
                *self.connect_points
            ]
        )
    

    def create_header(self):
        """
        Создает шапку узла
        """
        self.ref_open_button = Ref[IconButton]()
        return Container(
            height = self.HEADER_HEIGHT,
            content = Row(
                controls = [
                    IconButton(
                        ref = self.ref_open_button,
                        icon = icons.KEYBOARD_ARROW_DOWN,
                        icon_color = self.HEADER_ICON_COLOR,
                        on_click = self.toggle_parameters,
                        icon_size = 15,
                    ),
                    Text(f'{self.id}: {self.name}'),
                    IconButton(
                        icon = icons.CLOSE,
                        icon_color = self.HEADER_ICON_COLOR,
                        on_click = self.delete,
                        icon_size = 15,
                    )
                ],
                alignment = MainAxisAlignment.SPACE_BETWEEN,
            ),
            bgcolor = colors.with_opacity(0.5, self.header_color),
            border_radius = border_radius.only(
                top_left = self.BORDER_RADIUS, top_right = self.BORDER_RADIUS
            ),
            shadow = BoxShadow(
                spread_radius = 0,
                blur_radius = 5,
                color = self.HEADER_SHADOW_COLOR,
                offset = Offset(0, 3),
                blur_style = ShadowBlurStyle.NORMAL,
            ),
        )


    def toggle_parameters(self, e):
        """
        Открывает/закрывает параметры узла
        """
        self.is_open = not self.is_open
        self.parameters.visible = self.is_open
        self.ref_open_button.current.icon = (
            icons.KEYBOARD_ARROW_DOWN
            if self.is_open
            else icons.KEYBOARD_ARROW_RIGHT
        )
        self.header.border_radius = (
            border_radius.only(top_left = self.BORDER_RADIUS, top_right = self.BORDER_RADIUS)
            if self.is_open
            else border_radius.all(self.BORDER_RADIUS)
        )
        for point in self.connect_points:
            if self.is_open:
                point.top, point.left = point.open_top, point.open_left
            else:
                point.top, point.left = point.close_top, point.close_left

        # self.height = self.get_height()
        self.node_area.paint_line()
        self.update()
    

    def delete(self, e):
        """
        Удаляет узел
        """
        self.node_area.delete_node(self)
    

    def create_parameters(self):
        """
        Создает параметры узла
        """
        self.parameters_list = self.create_parameters_list(self.config.parameters)
        self.set_connect_points_coordinates()

        return Container(
            width = self.width,
            content = Column(
                controls = self.parameters_list,
                spacing = 0,
            ),
            padding = padding.all(self.PARAM_PADDING),
        )
    

    def create_parameters_list(self, config_list: list) -> list:
        '''
        Создает список параметров
        '''
        return [
            type_to_param[config.type](node=self, config=config)
            for config in config_list
        ]
    

    def set_connect_points_coordinates(self):
        """
        Устанавливает координаты точек связи
        """
        
        out_value_count = len([
            param for param in self.config.parameters
            if param.connect_type == ParameterConnectType.OUT and param.has_connect_point
        ])
        in_param_count = len([
            param for param in self.config.parameters
            if param.connect_type == ParameterConnectType.IN and param.has_connect_point
        ])

        out_center_x = self.width - self.POINT_SIZE // 2 - self.BORDER_RADIUS
        in_center_x = self.POINT_SIZE // 2 + self.BORDER_RADIUS
        center_y = self.HEADER_HEIGHT // 2

        out_close_coord = self.get_points_close_coordinates(
            center_x = out_center_x,
            center_y = center_y,
            radius = self.BORDER_RADIUS,
            num_objects = out_value_count,
            angle_start = -90,
            angle_end = 90,
        )
        in_close_coord = self.get_points_close_coordinates(
            center_x = in_center_x,
            center_y = center_y,
            radius = self.BORDER_RADIUS,
            num_objects = in_param_count,
            angle_start = -90,
            angle_end = -270,
        )

        top = self.HEADER_HEIGHT + self.POINT_SIZE // 2 + self.PARAM_PADDING
        left_out = self.width - 12

        for param in self.parameters_list:
            if param.has_connect_point:
                if param._connect_type == ParameterConnectType.OUT:
                    left = left_out
                    cords = out_close_coord.pop(0)
                else:
                    left = 0
                    cords = in_close_coord.pop(0)

                close_top = cords[1]
                close_left = cords[0] - self.POINT_SIZE // 2

                param.set_connect_point_coordinates(
                    open_top = top + self.POINT_SIZE // 2,
                    open_left = left,
                    close_top = close_top,
                    close_left = close_left
                )

            top += param.height
    

    def create_contact_points_list(self):
        """
        Создает точки контакта
        """
        return [
            param.connect_point for param in self.parameters_list
            if param.has_connect_point or param.connect_point is not None
        ]
    

    def get_points_close_coordinates(
        self,
        center_x, center_y,
        radius,
        num_objects,
        angle_start = 0,
        angle_end = 360,
        point_idx = None
    ):
        """
        Возвращает координаты точек контакта с окружностью
        (0 градусов справа на оси X, по часовой)

        center_x, center_y - координаты центра окружности
        radius - радиус окружности
        num_objects - количество точек
        angle_start - начальный угол
        angle_end - конечный угол
        point_idx - индекс точки, если None, то возвращает координаты всех точек
        """
        if num_objects < 1:
            return []
        step_angle = (angle_end - angle_start) / num_objects
        points = [
            (
                center_x + radius * math.cos(math.radians(angle_start + idx * step_angle + step_angle / 2)),
                center_y + radius * math.sin(math.radians(angle_start + idx * step_angle + step_angle / 2))
            )
            for idx in range(num_objects)
        ]
        return points if point_idx is None else points[point_idx]
    

    def clear_contact_point(self, param_idx: int):
        """
        Очищает точку контакта и удаляет соединение
        """
        con_p: NodeConnectPoint = next(con_p for con_p in self.connect_points if con_p.id == param_idx)
        if not isinstance(con_p.content, Draggable):
            return
        con_p.content = con_p.content.content

        con_p.drag_leave(None)

        connect = next(con for con in self.connects if con.to_param_idx == param_idx)
        self.connects.remove(connect)

        param = next(param for param in self.parameters_list if param.id == param_idx)
        param.set_connect_state(False)

        self.node_area.paint_line()


    def on_drag(self, e: DragUpdateEvent):
        """
        Обработка перемещения узла
        """
        if not self.is_selected:
            self.is_selected = True
            self.node_area.clear_selection(None)
            self.set_selection()

        self.node_area.drag_selection(top_delta = e.delta_y, left_delta = e.delta_x)

        # for con in self.connects:
        #     path: cv.Path = con.ref_path.current
        #     for el in path.elements:
        #         if isinstance(el, (cv.Path.MoveTo, cv.Path.LineTo, cv.Path.CubicTo)):
        #             el.x += e.delta_x
        #             el.y += e.delta_y
        #         if isinstance(el, cv.Path.CubicTo):
        #             el.cp1x += e.delta_x
        #             el.cp1y += e.delta_y
        #             el.cp2x += e.delta_x
        #             el.cp2y += e.delta_y

        self.node_area.paint_line()
        self.node_area.update()


    def drag_node(self, left_delta = 0, top_delta = 0):
        """
        Переместить узел
        """
        self.top = max(0, self.top + top_delta * self.scale)
        self.left = max(0, self.left + left_delta * self.scale)


    def toggle_selection(self, e):
        """
        Переключает выделение узла
        """
        self.is_selected = not self.is_selected
        self.set_selection()
        self.update()


    def set_selection(self):
        """
        Включает выделение узла
        """
        conteiner: Container = self.ref_content_conteiner.current
        if self.is_selected:
            conteiner.bgcolor = self.NODE_SELECT_BGCOLOR
            conteiner.border = border.all(self.BORDER_WIDTH, self.NODE_SELECT_BORDER_COLOR)
            self.node_area.add_selection_node(self)
        else:
            conteiner.bgcolor = self.NODE_BGCOLOR
            conteiner.border = border.all(self.BORDER_WIDTH, self.NODE_BORDER_COLOR)
            self.node_area.remove_selection_node(self)
