from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .node import Node

from flet import *
from dataclasses import dataclass

from .parametr_typing import *



@dataclass
class OutParamConfig:
    """
    Конфигурация параметра с одним значением
    
    name - название параметра
    height - высота параметра
    connect_point_color - цвет точки подключения
    """
    name: str   = 'Untitled'
    height: int = 20
    has_connect_point: bool = True
    connect_point_color: str = 'green'

    @property
    def type(self) -> ParameterType:
        return ParameterType.OUT
    
    @property
    def connect_type(self) -> ParameterType:
        return ParameterConnectType.OUT


class OutParam(Container, ParamInterface):
    def __init__(self, node: 'Node', config: OutParamConfig = OutParamConfig()):
        super().__init__()
        self._type = ParameterType.OUT
        self._connect_type = ParameterConnectType.OUT
        self.node = node
        self._config: OutParamConfig = config

        self.set_style()

        self.content = self._create_content()

        if self._config.has_connect_point:
            self.connect_point = self._create_connect_point()

    
    def _create_content(self):
        '''
        Создает содержимое параметра
        '''
        return Container(
            content = Row(
                controls = [
                    Text(self._name + str(self.id)),
                ],
                alignment = MainAxisAlignment.END
            ),
            padding = padding.only(left = 5, right = 5),
        )
    

    def set_style(self):
        """
        Устанавливает стиль параметра
        """
        self._name = self._config.name
        self.height = self._config.height
        
        self.has_connect_point = self._config.has_connect_point
        self.connect_point_color = self._config.connect_point_color


    def _on_change(self) -> None:
        return super()._on_change()
    

    def set_connect_state(self, is_connected: bool) -> None:
        return super().set_connect_state(is_connected)