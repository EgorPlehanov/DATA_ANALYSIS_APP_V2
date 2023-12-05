from flet import *
from flet import (Container, colors, padding, border, Column)


class FunctionResultView(Container):
    def __init__(self, function):
        super().__init__()
        self.function = function
        self.key = self.function.id

        self.content = self.create_content()
        self.border_radius = 10
        self.bgcolor = colors.BLACK26
        self.padding = padding.only(left=10, top=10, right=20, bottom=10)
        self.on_click = self.function._on_click


    def change_selection(self):
        '''Изменяет выделение результата'''
        self.border = border.all(color=colors.BLUE) if self.function.selected else None


    def create_content(self) -> Column:
        return Column(controls=[])
