from flet import (
    Container, Row, Icon, Text, colors,
    icons, FontWeight, border, margin,
)


class ResultErrorMessage(Container):
    def __init__(self, error_message: str):
        super().__init__()
        self.error_message = error_message

        self.content = self.create_content()

        self.bgcolor = colors.with_opacity(0.05, colors.RED)
        self.border = border.all(width=1,color=colors.RED)
        self.border_radius = 10
        self.padding = 10
        self.margin = margin.only(left=10)


    def create_content(self) -> Row:
        return Row(
            controls = [
                Icon(name=icons.ERROR_OUTLINE, color=colors.RED),
                Row(
                    expand = True,
                    wrap = True,
                    controls = [
                        Text(
                            value = f'Ошибка: {self.error_message}', 
                            color = colors.RED, 
                            weight = FontWeight.BOLD, 
                            size = 16, 
                            max_lines = 3,
                            selectable = True
                        ),
                    ]
                )
            ],
            expand = True,
        )