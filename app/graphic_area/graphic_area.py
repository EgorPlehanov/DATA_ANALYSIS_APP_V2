from flet import (
    Row, Page, Ref, Container, Column, PopupMenuButton, PopupMenuItem,
    Text, Icon, colors, alignment, ScrollMode, border, Tabs, padding
)

from .function import Function
from .function_attributes.calculate_functions.function_library import FunctionLibrary


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
        self.list_function_results = []

        # Ссылки на элементы управления графической области
        self.ref_parameters_menu = Ref[Container]()
        self.ref_result_view = Ref[Container]()

        self.controls = self.create_graphic_area_controls()


    def get_functions(self) -> dict:
        '''Возвращает словарь с функциями'''
        return FunctionLibrary.get_function_dict()
    
    
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
                            content = Row(controls = [
                                Text(type, size=16), Icon('add')
                            ]),
                            tooltip = type,
                            bgcolor = colors.WHITE10,
                            padding = 5,
                            border_radius = 5,
                        ),
                        items = [
                            PopupMenuItem(
                                text = func.name,
                                data = func.key,
                                on_click = self.add_function
                            )
                            for func in functions
                        ]
                    )
                    for type, functions in self.functions.items()
                ]
            ),
            bgcolor = colors.BLACK26,
            padding = 5,
        )
    

    def create_function_card_menu(self) -> Container:
        '''Создает меню представления созданных функций'''
        return Container(
            width = 350,
            bgcolor = colors.BLACK12,
            alignment = alignment.top_center,
            padding = padding.only(left=5, right=5),
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
            content = Column(
                tight = True,
                expand = True,
                scroll = ScrollMode.AUTO,
                controls = self.list_function_results
            ) 
            # Tabs(
            #     scrollable = False,
            #     ref = self.ref_result_view,
            #     animation_duration = 200,
            #     tabs=
            # ),
        )
    

    def add_function(self, e):
        '''Добавляет функцию в список'''
        key = e.control.data
        if not key:
            return
        
        function = Function(self.page, self, key)
        
        self.list_function_cards.append(function.view.card_view)
        self.list_function_parameters.append(function.view.parameters_view)
        self.list_function_results.append(function.view.results_view)
        self.update()
    

    def delete_function(self, function):
        '''Удаляет функцию из графической области'''
        self.list_function_cards.remove(function.view.card_view)
        self.list_function_parameters.remove(function.view.parameters_view)
        self.list_function_results.remove(function.view.results_view)

        self.update()