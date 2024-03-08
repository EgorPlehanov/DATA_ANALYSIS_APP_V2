from enum import Enum
from random import choice
from typing import List, Dict
from dataclasses import dataclass, field
from flet import colors, Ref
import flet.canvas as cv
from itertools import count



class Color(Enum):
    '''Цвет'''
    RED         = "#ff0000"
    PINK        = "#ff0072"
    PURPLE      = "#AA00FF"
    DEEP_PURPLE = "#6a00ff"
    INDIGO      = "#0026ff"
    BLUE        = "#2962FF"
    LIGHT_BLUE  = "#0091EA"
    CYAN        = "#00ddff"
    TEAL        = "#00ffdc"
    GREEN       = "#00ff69"
    LIGHT_GREEN = "#63ff00"
    LIME        = "#bdff00"
    YELLOW      = "#FFD600"
    AMBER       = "#FFAB00"
    ORANGE      = "#FF6D00"
    DEEP_ORANGE = "#DD2C00"

    def __str__(self):
        return str(self.value)
    
    @classmethod
    def random(cls):
        '''Возвращает случайное значение цвета'''
        return choice(list(cls))



@dataclass
class NodeConnect:
    '''Связь'''
    id_counter = count()

    from_node_id: int   = 0
    from_value_idx: int = 0
    to_node_id: int     = 0
    to_param_idx: int   = 0
    color: str          = colors.RED
    ref_path: Ref[cv.Path] = field(default_factory=Ref[cv.Path])

    def __post_init__(self):
        self.id = next(self.id_counter)

    def __str__(self) -> str:
        return f"{self.id}: ({self.from_node_id}-{self.from_value_idx})->({self.to_node_id}-{self.to_param_idx})"
