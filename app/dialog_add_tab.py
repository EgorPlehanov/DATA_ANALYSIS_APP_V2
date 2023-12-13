from .tabs_modes import TabMode

from flet import (
    AlertDialog, Text, TextField, TextButton,
    MainAxisAlignment, ControlEvent
)


class DialogAddTab(AlertDialog):
    def __init__(self, add_tab_function: callable):
        super().__init__()
        self._add_tab = add_tab_function

        self.modal = True,
        self.title = self._create_title()
        self.content = self._create_content()
        self.actions = self._create_actions_list()
        self.actions_alignment = MainAxisAlignment.END


    def _create_title(self) -> Text:
        '''Создает заголовок диалогового окна'''
        return Text("Добавить вкладку", text_align = "center")


    def _create_content(self) -> TextField:
        '''Создает содержимое диалогового окна'''
        return TextField(
            label = "Название вкладки",
            autofocus = True,
            on_submit = self._add_tab
        )
    

    def _create_actions_list(self) -> list:
        '''Создает список диалоговых кнопок'''
        return [
            TextButton("Добавить", on_click = self._add_tab),
            TextButton("Отмена", on_click = self.close_dialog)
        ]


    def open_dialog(self, e: ControlEvent, tab_mode: TabMode) -> None:
        '''Открывает диалоговое окно для добавления вкладки'''
        self.title.value = tab_mode.dialog_title
        self.data = tab_mode
        self.open = True
        self.page.update()


    def close_dialog(self, e: ControlEvent) -> None:
        '''Закрывает диалоговое окно для добавления вкладки'''
        self.open = False
        self.data = ''
        self.content.value = ''
        self.page.update()
        