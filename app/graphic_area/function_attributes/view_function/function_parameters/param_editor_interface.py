from abc import ABC, abstractmethod
from typing import Any
from flet import border, colors, margin


class ParamEditorInterface(ABC):
    _type: str = None
    _name: str = None

    @property
    def type(self) -> str:
        return self._type
    
    @property
    def name(self) -> str:
        return self._name
    
    @abstractmethod
    def create_content(self) -> Any:
        pass
    
    @abstractmethod
    def on_change(self) -> None:
        pass

    def update_content(self) -> None:
        pass
    
    def set_styles(self) -> None:
        params = {
            'data': self._type,
            'padding': 10,
            'border_radius': 10,
            'border': border.all(1, colors.with_opacity(0.05, colors.SECONDARY)),
            'bgcolor': colors.BLACK12,
            'margin': margin.only(left=5, right=5, top=5),
        }
        for key, value in params.items():
            setattr(self, key, value)