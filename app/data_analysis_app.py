from flet import (
    Page,
    UserControl,    
    AppBar,
    Container,
    Row,
    FilledButton,
    Icon,
    icons,
    Text,
    colors,
    AlertDialog,
    TextField,
    TextButton,
    MainAxisAlignment,
    Ref,
    Tab,
    IconButton,
    Tabs,
)
from collections import namedtuple
from functools import partial

from graphic_area.graphic_area import GraphicArea


class DataAnalysisApp(UserControl):
    def __init__(self, page: Page):
        super().__init__()
        self.page = page
        self.expand = True

        self.app_tab_mode = self.get_app_tab_modes()
        
        self.appbar = self.create_appbar()
        self.page.appbar = self.appbar

        self.dialog_modal_add_tab = self.create_dialog_modal_add_tab()
        self.page.dialog = self.dialog_modal_add_tab

        self.tabs_bar = Tabs(animation_duration=200)


    def build(self):
        '''Собирает вкладки'''
        return self.tabs_bar
    

    def get_app_tab_modes(self):
        '''
        Возвращает словарь режимов работы вкладок
        
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


    def create_dialog_modal_add_tab(self) -> AlertDialog:
        '''Создает и возвращает всплывающее диалоговое окно создания вкладки'''
        return AlertDialog(
            modal=True,
            title=Text("Добавить вкладку", text_align = "center"),
            content=TextField(label="Название вкладки", autofocus=True, on_submit=self.add_tab),
            actions = [
                TextButton("Добавить", on_click = self.add_tab),
                TextButton("Отмена", on_click = self.close_dialog)
            ],
            actions_alignment=MainAxisAlignment.END,
        )
    

    def create_appbar(self) -> AppBar:
        '''Создает и возвращает экземпляр класса AppBar'''
        appbar_actions = [
            Container(
                content = Row(
                    controls = [
                        FilledButton(
                            icon = "add", text = mode.name, data = mode.mode,
                            on_click = self.open_dialog
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


    def open_dialog(self, e) -> None:
        '''Открывает диалоговое окно для добавления вкладки'''
        button_name = e.control.data

        self.dialog_modal_add_tab.title.value = "Добавить вкладку"
        if button_name in self.app_tab_mode:
            self.dialog_modal_add_tab.title.value = self.app_tab_mode[button_name].dialog_title
        
        self.dialog_modal_add_tab.data = button_name
        self.dialog_modal_add_tab.open = True
        
        self.page.update()


    def close_dialog(self, e) -> None:
        '''Закрывает диалоговое окно для добавления вкладки'''
        self.dialog_modal_add_tab.open = False
        self.dialog_modal_add_tab.data = ''
        self.dialog_modal_add_tab.content.value = ''
        self.page.update()
        self.update()


    def add_tab(self, e) -> None:
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
        tab = self.crete_tab(
            ref=tab_ref,
            icon=tab_icon,
            title=tab_title,
            content=tab_content_widget
        )

        self.tabs_bar.tabs.append(tab)
        self.tabs_bar.selected_index = len(self.tabs_bar.tabs) - 1

        self.close_dialog(self)


    def crete_tab(self, ref, icon, title, content) -> Tab:
        '''Создает вкладку'''
        return Tab(
            ref=ref,
            tab_content=Row(
                controls=[
                    Icon(name=icon),
                    Text(value=title),
                    IconButton(icon=icons.CLOSE, data=ref, on_click = self.delete_tab),
                ]
            ),
            content=content
        )
    

    def delete_tab(self, e) -> None:
        '''Удаляет вкладку'''
        deleted_tab = e.control.data.current
        self.tabs_bar.tabs.remove(deleted_tab)
        self.update()
