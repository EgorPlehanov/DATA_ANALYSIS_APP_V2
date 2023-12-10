from flet import (
    Container, Row, Icon, Text, colors, Ref,
    icons, FontWeight, border, margin,
)


class ResultErrorMessage(Container):
    def __init__(self, error_message: str):
        super().__init__()
        self.error_message = error_message

        self.ref_error_message = Ref[Text]()

        self.content = self.create_content()

        self.bgcolor = colors.with_opacity(0.05, colors.RED)
        self.border = border.all(width=1,color=colors.RED)
        self.border_radius = 10
        self.padding = 10
        self.margin = margin.only(left=10)


    def create_content(self) -> Row:
        '''Создает карточку с ошибкой'''
        return Row(
            controls = [
                Icon(name=icons.ERROR_OUTLINE, color=colors.RED),
                Row(
                    expand = True,
                    wrap = True,
                    controls = [
                        Text(
                            ref = self.ref_error_message,
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
    

    def update_values(self, new_error_message: str = '') -> None:
        '''Обновляет значение текстового поля с ошибкой'''
        self.ref_error_message.current.value = f"Ошибка: {new_error_message}"
        self.update()
        