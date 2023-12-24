from .tabs_modes import TabsModes, TabMode
from .dialog_add_tab import DialogAddTab
from .appbar import ApplicationBar

from flet import (
    Page, Container, Row, Icon, icons, Text, Tab, 
    ControlEvent, Ref, IconButton, Tabs, Container
)


class DataAnalysisApp(Container):
    def __init__(self, page: Page):
        super().__init__()
        self.page = page
        self.expand = True

        self.tabs_modes = TabsModes.get_tabs_modes()

        self.dialog_add_tab = DialogAddTab(self._add_tab)
        self.page.dialog = self.dialog_add_tab
        
        self.appbar = ApplicationBar(self.tabs_modes, self.dialog_add_tab.open_dialog)
        self.page.appbar = self.appbar
        
        self.content = self._create_content()


    def _create_content(self) -> Tabs:
        '''Создает содержимое приложения'''
        self.ref_tabs_bar = Ref[Tab]()
        return Tabs(
            ref = self.ref_tabs_bar,
            animation_duration = 200,
            tabs = []
        )
    

    def _add_tab(self, e: ControlEvent) -> None:
        '''Добавляет вкладку в список вкладок tabs_bar'''
        mode: TabMode = self.dialog_add_tab.data
        title = self.dialog_add_tab.content.value

        tab = self._create_tab(mode, title)

        tabs_control: Tabs = self.ref_tabs_bar.current
        tabs_control.tabs.append(tab)
        tabs_control.selected_index = len(tabs_control.tabs) - 1

        self.dialog_add_tab.close_dialog(self)


    def _create_tab(self, tab_mode: TabMode, title: str = '') -> Tab:
        '''Создает вкладку'''
        ref = Ref[Tab]()
        if not title:
            title = 'Вкладка ' + tab_mode.default_tab_title
        return Tab(
            ref = ref,
            tab_content = Row([
                    Icon(name=tab_mode.tab_icon),
                    Text(value=title),
                    IconButton(icon=icons.CLOSE, data=ref, on_click = self._delete_tab),
            ]),
            content = tab_mode.tab_content(self, self.page)
        )
    

    def _delete_tab(self, e: ControlEvent) -> None:
        '''Удаляет вкладку'''
        deleted_tab = e.control.data.current
        self.ref_tabs_bar.current.tabs.remove(deleted_tab)
        self.update()
