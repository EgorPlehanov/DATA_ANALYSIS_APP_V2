from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .node import Node

from flet import *
from enum import Enum
from typing import Any

from .node_typing import NodeConnect

    

class ParameterConnectType(Enum):
    '''
    Типы подключения

    IN - входной
    OUT - выходной
    '''
    IN = 'in'
    OUT = 'out'

    def __str__(self):
        return self.value



class NodeConnectPoint(Container):
    POINT_BORDER_WIDTH = 1

    def __init__(
        self,
        node: "Node",
        parameter: Any,
        id: int,
        top: int = 0,
        left: int = 0,
        close_top: int = 0,
        close_left: int = 0,
        connect_type: ParameterConnectType = ParameterConnectType.OUT,
        color: str = colors.GREY_500,
        size: int = 12,
    ):
        super().__init__()
        self.node = node
        self.parameter = parameter

        self.node_id = self.node.id
        self.id = id
        
        self.connect_type = connect_type
        self.point_color = color
        self.point_size = size

        self.top = top
        self.left = left

        self.open_top = top
        self.open_left = left
        self.close_top = close_top
        self.close_left = close_left

        self.animate_position = animation.Animation(200, AnimationCurve.FAST_OUT_SLOWIN)

        self.point: Container = self.create_point()
        self.content = self.create_content()
        
        
    def create_point(self) -> Container:
        """
        Создает контакт
        """
        return Container(
            on_long_press = (
                lambda e: self.node.clear_contact_point(self.id)
                if self.connect_type == ParameterConnectType.IN else None
            ),
            bgcolor = self.point_color,
            width = self.point_size,
            height = self.point_size,
            shape = BoxShape.CIRCLE,
            border = border.all(self.POINT_BORDER_WIDTH, colors.BLACK),
            shadow = BoxShadow(
                spread_radius = 0,
                blur_radius = 5,
                color = colors.BLACK38,
                offset = Offset(0, 5),
                blur_style = ShadowBlurStyle.NORMAL,
            ),
        )


    def create_content(self) -> DragTarget | Draggable:
        """
        Создает контент контакта
        """
        if self.connect_type == ParameterConnectType.IN:
            return DragTarget(
                content = self.point,
                on_will_accept = self.drag_will_accept,
                on_accept = self.drag_accept,
                on_leave = self.drag_leave
            )
        else:
            return Draggable(
                data = {
                    'node_id': self.node_id,
                    'value_idx': self.id,
                    'color': self.point_color,
                    'type': 'out',
                },
                content = self.point,
            )
    

    def drag_will_accept(self, e: ControlEvent) -> None:
        """
        Показывает может ли узел принять контакт
        """
        self.point.border = border.all(
            self.POINT_BORDER_WIDTH,
            colors.GREEN if e.data == "true" else colors.RED
        )
        self.point.bgcolor = (colors.GREEN if e.data == "true" else colors.RED)
        self.update()
    

    def drag_leave(self, e: ControlEvent):
        """
        Отменяент изменения drag_will_accept(), когда курсор убирают с цели
        """
        if isinstance(self.content, Draggable):
            self.point.bgcolor = self.content.data.get('color')
        else:
            self.point.bgcolor = self.point_color
        self.point.border = border.all(self.POINT_BORDER_WIDTH, colors.BLACK)
        self.update()


    def drag_accept(self, e: DragTargetAcceptEvent):
        """
        Принимает контакт
        """
        src = self.page.get_control(e.src_id)
        # пропускаем связь с самим собой
        if src.data.get('node_id') == self.node_id:
            self.drag_leave(e)
            return
        
        # удаляет связь при перетаскивании входного параметра из другого контакта
        if src.data.get('type') == 'in':
            self.node.node_area.delete_node_connect(src.data.get('cur_node_id'), src.data.get('cur_param_idx'))

        connect = next((
            con for con in self.node.connects
            if con.to_param_idx == self.id
        ), None)
        if connect is None:
            self.node.connects.append(
                NodeConnect(
                    from_node_id = src.data.get('node_id'),
                    from_value_idx = src.data.get('value_idx'),
                    to_node_id = self.node_id,
                    to_param_idx = self.id,
                    color = src.data.get('color')
                )
            )
        elif (
            connect.from_node_id == src.data.get('node_id') 
            and connect.from_value_idx == src.data.get('value_idx')
        ):
            self.point.bgcolor = self.point.data.get('color')
            self.point.border = border.all(self.POINT_BORDER_WIDTH, colors.BLACK)
            self.update()
            return
        else:
            connect.from_node_id = src.data.get('node_id')
            connect.from_value_idx = src.data.get('value_idx')
            connect.color = src.data.get('color')
            
        # Обновление цвета и данных Точки контакта
        data = src.data.copy()
        data['type'] = 'in'
        data['cur_node_id'] = self.node_id
        data['cur_param_idx'] = self.id
        if not isinstance(self.content, Draggable):
            self.content = Draggable(
                content = self.content,
                data = data
            )
        else:
            self.content.data = data
        self.point.bgcolor = src.data.get('color')
        self.point.border = border.all(self.POINT_BORDER_WIDTH, colors.BLACK)
            
        self.node.node_area.paint_line()
        # self.update()
        self.parameter.set_connect_state(True)