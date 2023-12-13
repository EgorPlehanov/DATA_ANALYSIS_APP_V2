from .tabs_modes import TabMode

from flet import (
    AppBar, Container, Row, colors,
    FilledButton, Icon, Text, icons
)


class ApplicationBar(AppBar):
    def __init__(self, tabs_modes: dict[str, TabMode], open_dialog: callable):
        super().__init__()
        self._tabs_modes = tabs_modes
        self._open_dialog = open_dialog
        
        self.leading = self._create_leading()
        self.leading_width = 40
        self.title = self._create_title()
        self.center_title = False
        self.bgcolor = colors.SURFACE_VARIANT
        self.actions = self._create_appbar_actions()


    def _create_leading(self):
        '''Создает левую часть AppBar'''
        return Icon(icons.ANALYTICS)


    def _create_title(self):
        '''Создает заголовок AppBar'''
        return Text(value = "Data Analysis App", text_align = "start")


    def _create_appbar_actions(self):
        '''Создает набор кнопок для создания '''
        return [Container(
            content = Row([
                FilledButton(
                    icon = "add",
                    text = mode.name,
                    data = mode,
                    on_click = self._open_dialog
                )
                for mode in self._tabs_modes.values()
            ]),
            margin = 10
        )]
