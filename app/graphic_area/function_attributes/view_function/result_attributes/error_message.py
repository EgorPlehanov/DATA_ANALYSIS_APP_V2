from typing import List
from flet import (
    Container, Row, Icon, Text, colors, Ref,
    icons, FontWeight, border, margin, CrossAxisAlignment
)


class ResultErrorMessage(Row):
    '''Карточка с ошибкой'''
    def __init__(self, error_message: str):
        super().__init__()
        self.error_message = error_message

        self.controls = self.create_controls()


    def create_controls(self) -> List[Container]:
        '''Создает карточку с ошибкой'''
        self.ref_error_message = Ref[Text]()
        return [Container(
            content = Row(
                controls = [
                    Icon(name=icons.ERROR_OUTLINE, color=colors.RED),
                    Text(
                        ref = self.ref_error_message,
                        value = f'Ошибка: {self.error_message}', 
                        color = colors.RED, 
                        weight = FontWeight.BOLD, 
                        size = 16, 
                        max_lines = 3,
                        selectable = True,
                        expand = True
                    ),
                ],
                expand=True,
                vertical_alignment = CrossAxisAlignment.START
            ),
            expand = True,
            bgcolor = colors.with_opacity(0.05, colors.RED),
            border = border.all(width=1,color=colors.RED),
            border_radius = 10,
            padding = 10,
            margin = margin.only(left=10),
        )]
    

    def update_values(self, new_error_message: str = '') -> None:
        '''Обновляет значение текстового поля с ошибкой'''
        self.ref_error_message.current.value = f"Ошибка: {new_error_message}"
        self.update()
        