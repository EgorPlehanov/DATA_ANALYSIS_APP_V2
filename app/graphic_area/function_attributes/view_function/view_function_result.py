from flet import *
from flet import (Container)


class FunctionResultView(Container):
    def __init__(self, function):
        super().__init__()

        self.content = self.create_content()
        # self.ref = self.ref_result_view
        self.data = self
        self.border_radius = 10
        self.bgcolor = colors.BLACK26
        self.padding = padding.only(left=10, top=10, right=20, bottom=10)
        # self.key = self.function_id
        # self.on_click = self.on_change_selected


    def create_content(self) -> Column:
        return Column(controls=[])
