from flet import Container, Column


class FunctionParametersView(Container):
    def __init__(self, function):
        super().__init__()
        self.function = function

        self.content = self.create_content()
        self.visible = False
        self.padding = 10
        self.width = 350


    def create_content(self) -> Column:
        return Column(
            controls = [], #self._get_parameters_view_list(),
            # ref = self.ref_parameters_view,
            tight = True,
        )