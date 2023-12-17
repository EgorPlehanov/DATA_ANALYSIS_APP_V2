from ...function_typing import Color
from .color_picker import ColorPicker

from typing import List
from flet import (
    AlertDialog, TextButton, MainAxisAlignment, ControlEvent
)


class DialogColorPicker(AlertDialog):
    def __init__(self, color: Color, update_color: callable):
        super().__init__()
        self.color = str(color)
        self.update_color = update_color

        self.content = self._create_content()
        self.actions = self._create_actions()
        self.actions_alignment = MainAxisAlignment.SPACE_BETWEEN
        self.on_dismiss = self.close_dialog


    def _create_content(self) -> ColorPicker:
        '''Создает содержимое карточки функции'''
        return ColorPicker(self.color) # color=self.color, width=300)
    

    def _create_actions(self) -> List[TextButton]:
        '''Создает действия карточки функции'''
        return [
            TextButton("Отмена", on_click = self.close_dialog),
            TextButton("Применить", on_click = self.change_color),
        ]


    def open_dialog(self, e: ControlEvent) -> None:
        '''Открывает диалог'''
        self.content.color = self.color
        self.open = True
        self.page.update()


    def close_dialog(self, e: ControlEvent) -> None:
        '''Закрывает диалог'''
        self.open = False
        self.page.update()


    def change_color(self, e: ControlEvent) -> None:
        '''Срабатывает при изменении цвета'''
        self.color = self.content.color
        self.update_color(self.color)

        self.open = False
        self.page.update()
