from graphic_area.graphic_area import GraphicArea
from flet import (
    Page, AppBar, Container, Row, FilledButton, Icon,
    icons, Text, colors, AlertDialog, TextField, TextButton,
    MainAxisAlignment, Ref, Tab, IconButton, Tabs, Container
)
from collections import namedtuple
from functools import partial


class DataAnalysisApp(Container):
    def __init__(self, page: Page):
        super().__init__()
        self.page = page
        self.expand = True

        self.app_tab_mode = self._get_app_tab_modes()
        
        self.appbar = self._create_appbar()
        self.page.appbar = self.appbar

        self.dialog_modal_add_tab = self._create_dialog_modal_add_tab()
        self.page.dialog = self.dialog_modal_add_tab

        self.ref_tabs_bar = Ref[Tab]()
        self.content = self._create_content()


    def _create_content(self) -> Tabs:
        return Tabs(
            ref = self.ref_tabs_bar,
            animation_duration = 200,
            tabs = []
        )


    def _get_app_tab_modes(self) -> dict:
        '''Возвращает словарь режимов работы вкладок
        
        AppTabMode attributs:
            mode - Код режима
            name - Название режима
            dialog_title - Название в диалоговом окне создания вкладки
            tab_icon - Иконка вкладки
            default_tab_title - Название вкладки по умолчанию
            create_tab_content - Ф-ция для создания обекта в кладки
        '''
        AppTabMode = namedtuple('AppTabMode', [
            'mode', 'name', 'dialog_title', 'tab_icon',
            'default_tab_title', 'create_tab_content'
        ])
        return {
            'graphic': AppTabMode(
                "graphic",
                "Работа с гафиками",
                "Добавить вкладку\nдля работы с графиками",
                "area_chart",
                'Графики',
                partial(GraphicArea, self, self.page)
            ),
            'image': AppTabMode(
                "image",
                "Работа с изображениями",
                "Добавить вкладку\nдля работы с изображениями",
                "image",
                'Изображения',
                partial(Text, "Работа с изображениями")
            ),
        }


    def _create_dialog_modal_add_tab(self) -> AlertDialog:
        '''Создает и возвращает всплывающее диалоговое окно создания вкладки'''
        return AlertDialog(
            modal=True,
            title=Text("Добавить вкладку", text_align = "center"),
            content=TextField(label="Название вкладки", autofocus=True, on_submit=self._add_tab),
            actions = [
                TextButton("Добавить", on_click = self._add_tab),
                TextButton("Отмена", on_click = self._close_dialog)
            ],
            actions_alignment=MainAxisAlignment.END,
        )
    

    def _create_appbar(self) -> AppBar:
        '''Создает и возвращает экземпляр класса AppBar'''
        appbar_actions = [
            Container(
                content = Row(
                    controls = [
                        FilledButton(
                            icon = "add", text = mode.name, data = mode.mode,
                            on_click = self._open_dialog
                        )
                        for mode in self.app_tab_mode.values()
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


    def _open_dialog(self, e) -> None:
        '''Открывает диалоговое окно для добавления вкладки'''
        button_name = e.control.data

        self.dialog_modal_add_tab.title.value = "Добавить вкладку"
        if button_name in self.app_tab_mode:
            self.dialog_modal_add_tab.title.value = self.app_tab_mode[button_name].dialog_title
        
        self.dialog_modal_add_tab.data = button_name
        self.dialog_modal_add_tab.open = True
        
        self.page.update()


    def _close_dialog(self, e) -> None:
        '''Закрывает диалоговое окно для добавления вкладки'''
        self.dialog_modal_add_tab.open = False
        self.dialog_modal_add_tab.data = ''
        self.dialog_modal_add_tab.content.value = ''
        self.page.update()
        self.update()


    def _add_tab(self, e) -> None:
        '''Добавляет вкладку в список вкладок tabs_bar'''
        tab_type = self.dialog_modal_add_tab.data
        tab_icon = "question_mark"
        tab_content_widget = None

        if tab_type in self.app_tab_mode:
            tab_icon = self.app_tab_mode[tab_type].tab_icon
            tab_content_widget = self.app_tab_mode[tab_type].create_tab_content()
            default_tab_title = self.app_tab_mode[tab_type].default_tab_title

        tab_title = self.dialog_modal_add_tab.content.value
        if not tab_title:
            tab_title = 'Вкладка ' + default_tab_title
        
        tab_ref = Ref[Tab]()
        tab = self._create_tab(
            ref = tab_ref,
            icon = tab_icon,
            title = tab_title,
            content = tab_content_widget
        )

        tabs_control = self.ref_tabs_bar.current
        tabs_control.tabs.append(tab)
        tabs_control.selected_index = len(tabs_control.tabs) - 1

        self._close_dialog(self)


    def _create_tab(self, ref, icon, title, content) -> Tab:
        '''Создает вкладку'''
        return Tab(
            ref=ref,
            tab_content=Row(
                controls=[
                    Icon(name=icon),
                    Text(value=title),
                    IconButton(icon=icons.CLOSE, data=ref, on_click = self._delete_tab),
                ]
            ),
            content=content
        )
    

    def _delete_tab(self, e) -> None:
        '''Удаляет вкладку'''
        deleted_tab = e.control.data.current
        self.ref_tabs_bar.current.tabs.remove(deleted_tab)
        self.update()
