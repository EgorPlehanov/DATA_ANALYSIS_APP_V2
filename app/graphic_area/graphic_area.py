import flet as ft
from flet import (
    Row,
    Page,
    TextField,
    Ref,
    Container,
    Column,
    Dropdown,
    dropdown,
    PopupMenuButton,
    PopupMenuItem,
    Text,
    Icon,
    colors,
    alignment,
    ScrollMode,
    border,
    Tabs,
)
# from .function import Function
from .function_attributes.view_function.function_parameters.checkboxes import *


class GraphicArea(Column):
    def __init__(self, app, page: Page):
        super().__init__()
        self.app = app
        self.page = page
        self.expand = True
        self.spacing = 0

        self.functions = self.get_functions()

        # Текущая выбранная функция
        self.ref_selected_function_card = Ref[Container]()

        # Список представлений карточек функций
        self.list_function_cards = []
        # Список представлений параметров функций
        self.list_function_parameters = []
        # Список представлений результатов
        self.list_results = []

        # Ссылки на элементы управления графической области
        self.ref_parameters_menu = Ref[Container]()
        self.ref_result_view = Ref[Container]()

        self.controls = self.create_graphic_area_controls()


    def get_functions(self) -> dict:
        '''Возвращает словарь с функциями'''
        return {
            'data': (
                'Данные', [
                    'Trend',
                    'Mean',
                    'Median',
                ]
            ),
            'edit': (
                'Обработка', [
                    'Trend',
                    'Mean',
                    'Median',
                ]
            ),
            'analysis': (
                'Анализ', [
                    'Correlation',
                    'Regression',
                    'Trend',
                ]
            )
        }
    
    
    def create_graphic_area_controls(self) -> list:
        '''Создает элементы управления графической области'''
        return [
            self.create_select_function_menu(),
            Row(
                expand=True,
                controls=[
                    self.create_function_card_menu(),
                    self.create_parameters_menu(),
                    self.create_result_view()
                ]
            )
        ]
    

    def create_select_function_menu(self) -> Container:
        '''Создает меню выбора функции'''
        return Container(
            content = Row(
                controls = [
                    PopupMenuButton(
                        content = Container(
                            content = Row(controls=[
                                Text(func_type, size=16), Icon(name='add')
                            ]),
                            bgcolor = ft.colors.WHITE10,
                            padding = 5,
                            border_radius = 5,
                        ),
                        items = [
                            PopupMenuItem(text=func_name, on_click=self.add_function)
                            for func_name in func_names
                        ]
                    )
                    for func_type, func_names in self.functions.values()
                ]
            ),
            bgcolor = ft.colors.BLACK26,
            padding = 5,
        )
    

    def create_function_card_menu(self) -> Container:
        '''Создает меню представления созданных функций'''
        return Container(
            width = 350,
            bgcolor = colors.BLACK26,
            alignment = alignment.top_center,
            content = Column(
                tight = True,
                scroll = ScrollMode.AUTO,
                spacing = 5,
                controls = self.list_function_cards
            )
        )
    

    def create_parameters_menu(self) -> Container:
        '''Создает меню параметров функции'''
        return Container(
            ref=self.ref_parameters_menu,
            alignment = alignment.top_center,
            bgcolor = colors.BLACK12,
            animate_size = 100,
            content = Column(
                tight = True,
                scroll = ScrollMode.AUTO,
                controls = self.list_function_parameters
            )
        )
    

    def create_result_view(self) -> Container:
        return Container(
            ref=self.ref_result_view,
            expand = True,
            border = border.all(colors.BLACK),
            content = Tabs(
                scrollable = False,
                ref = self.ref_result_view,
                animation_duration = 200,
                tabs=self.list_results
            ),
        )
    

    def add_function(self, e):
        '''Добавляет функцию в список'''
        function_name = e.control.text
        if not function_name:
            return
        
        function = CheckboxesEditor('D', 'param', [CBItem(True, 'a'), CBItem(False, 'b')])
        print(function.type)
        self.list_function_cards.append(function)
        self.update()
    

    def delite_function(self, function):
        '''Удаляет функцию из списка'''
        self.list_function_cards.remove(function)

        self.update()