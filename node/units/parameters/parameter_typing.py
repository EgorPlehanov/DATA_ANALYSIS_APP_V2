from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..node.node import Node

from abc import ABC, abstractmethod
from typing import Any
from enum import Enum
from itertools import count
from dataclasses import dataclass
from flet import colors

from ..node.node_connect_point import NodeConnectPoint, ParameterConnectType



class ParameterType(Enum):
    '''
    Типы параметров
    '''
    OUT = 'out'
    SINGLE_VALUE = 'single_value'
    TAKE_VALUE = 'take_value'
    BOOL_VALUE = 'bool_value'
    TEXT_VALUE = 'text_value'

    def __str__(self):
        return self.value



@dataclass
class ParameterConfigInterface:
    '''
    Интерфейс конфигурации параметра

    key - уникальный ключ параметра
    name - название параметра
    height - высота параметра
    connect_point_color - цвет точки подключения
    '''
    key: str = 'unknown'
    name: str = 'Untitled'
    height: int = 20
    default_value: Any = None
    has_connect_point: bool = True
    connect_point_color: str = colors.GREY_500
    tooltip: str = None

    def __post_init__(self):
        if self.key == 'unknown':
            self.key = self.name.lower().replace(" ", "_")



class ParamInterface(ABC):
    '''
    Интерфейс параметра
    '''
    id_counter = count()

    PADDING_VERTICAL_SIZE = 1
    
    MAIN_COLOR = colors.with_opacity(0.05, colors.WHITE)
    HOVER_COLOR = colors.with_opacity(0.2, colors.WHITE)
    ACCENT_COLOR = colors.DEEP_ORANGE_ACCENT_400
    
    _type: ParameterType = None
    _connect_type: ParameterConnectType = None
    _config: Any = None

    node: 'Node' = None

    _key: str = None
    name: str = None
    has_connect_point: bool = False
    connect_point_color: str = None
    
    connect_point = None

    def __init__(self):
        self.id = next(self.id_counter)

        self._key = self._config.key
        self.name = self._config.name
        self.has_connect_point = self._config.has_connect_point
        self.connect_point_color = self._config.connect_point_color
        self.is_connected = False
        self.value = self._config.default_value

    def __post_init__(self):
        self.height = self._config.height
        self.control_height = self.height - self.PADDING_VERTICAL_SIZE * 2
        self.tooltip = self._config.tooltip

    @property
    def type(self) -> str:
        return self._type
    
    @abstractmethod
    def _create_content(self) -> Any:
        pass

    def set_connect_state(self, is_connected: bool) -> None:
        self.is_connected = is_connected
        self._on_change()
    
    def _on_change(self) -> None:
        self.node.calculate()

    def _create_connect_point(self) -> NodeConnectPoint:
        return NodeConnectPoint(
            node = self.node,
            parameter = self,
            id = self.id,
            connect_type = self._connect_type,
            color = self.connect_point_color,
        )

    def set_connect_point_coordinates(
        self,
        open_top: int,
        open_left: int,
        close_top: int,
        close_left: int
    ) -> None:
        connect_point = self.connect_point
        if connect_point is not None:
            connect_point.top = open_top
            connect_point.left = open_left
            connect_point.open_top = open_top
            connect_point.open_left = open_left
            connect_point.close_top = close_top
            connect_point.close_left = close_left