from .tabs_modes import TabsModes
from .dialog_add_tab import DialogAddTab

from flet import (
    Page, AppBar, Container, Row, FilledButton, Icon,
    icons, Text, colors, Ref, Tab, IconButton, Tabs, Container
)


class DataAnalysisApp(Container):
    def __init__(self, page: Page):
        super().__init__()
        self.page = page
        self.expand = True

        self.tabs_modes = TabsModes.get_tabs_modes()

        self.dialog_add_tab = DialogAddTab(self._add_tab)
        self.page.dialog = self.dialog_add_tab
        
        self.appbar = self._create_appbar()
        self.page.appbar = self.appbar

        self.ref_tabs_bar = Ref[Tab]()
        self.content = self._create_content()


    def _create_content(self) -> Tabs:
        return Tabs(
            ref = self.ref_tabs_bar,
            animation_duration = 200,
            tabs = []
        )
    

    def _create_appbar(self) -> AppBar:
        '''Создает и возвращает экземпляр класса AppBar'''
        appbar_actions = [
            Container(
                content = Row(
                    controls = [
                        FilledButton(
                            icon = "add",
                            text = mode.name,
                            data = mode.type,
                            on_click = self.open_dialog
                        )
                        for mode in self.tabs_modes.values()
                    ],
                ),
                margin = 10
            )
        ]
        appbar = AppBar(
            leading = Icon(icons.ANALYTICS),
            leading_width = 40,
            title = Text(value = "Data Analysis App", text_align = "start"),
            center_title = False,
            bgcolor = colors.SURFACE_VARIANT,
            actions = appbar_actions,
        )
        return appbar
    

    def open_dialog(self, e) -> None:
        tab_mode = self.tabs_modes[e.control.data]
        self.dialog_add_tab.open_dialog(e, tab_mode)


    def _add_tab(self, e) -> None:
        '''Добавляет вкладку в список вкладок tabs_bar'''
        mode = self.dialog_add_tab.data

        icon = mode.tab_icon
        content = mode.tab_content(self, self.page)

        title = self.dialog_add_tab.content.value
        if not title:
            title = 'Вкладка ' + mode.default_tab_title
        
        tab_ref = Ref[Tab]()
        tab = self._create_tab(
            ref = tab_ref,
            icon = icon,
            title = title,
            content = content
        )

        tabs_control: Tabs = self.ref_tabs_bar.current
        tabs_control.tabs.append(tab)
        tabs_control.selected_index = len(tabs_control.tabs) - 1

        self.dialog_add_tab.close_dialog(self)


    def _create_tab(self, ref, icon, title, content) -> Tab:
        '''Создает вкладку'''
        return Tab(
            ref=ref,
            tab_content=Row([
                    Icon(name=icon),
                    Text(value=title),
                    IconButton(icon=icons.CLOSE, data=ref, on_click = self._delete_tab),
            ]),
            content=content
        )
    

    def _delete_tab(self, e) -> None:
        '''Удаляет вкладку'''
        deleted_tab = e.control.data.current
        self.ref_tabs_bar.current.tabs.remove(deleted_tab)
        self.update()
