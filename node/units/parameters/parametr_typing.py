from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..node.node import Node

from abc import ABC, abstractmethod
from typing import Any
from enum import Enum
from itertools import count

from ..node.node_connect_point import NodeConnectPoint, ParameterConnectType



class ParameterType(Enum):
    '''
    Типы параметров
    '''
    OUT = 'out'
    SINGLE_VALUE = 'single_value'

    def __str__(self):
        return self.value


class ParamInterface(ABC):
    id_counter = count()

    PADDING_VERTICAL_SIZE = 1

    _type: ParameterType = None
    _connect_type: ParameterConnectType = None
    _name: str = None
    _config: Any = None
    connect_point = None

    def __init__(self):
        self.id = next(self.id_counter)

    @property
    def type(self) -> str:
        return self._type
    
    @property
    def name(self) -> str:
        return self._name
    
    @abstractmethod
    def _create_content(self) -> Any:
        pass
    
    @abstractmethod
    def _on_change(self) -> None:
        pass

    @abstractmethod
    def set_connect_state(self, is_connected: bool) -> None:
        pass
    
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