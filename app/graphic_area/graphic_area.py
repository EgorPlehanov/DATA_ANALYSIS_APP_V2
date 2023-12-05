from flet_core.scrollable_control import ScrollableControl
from flet import (
    Row, Page, Ref, Container, Column, PopupMenuButton, PopupMenuItem,
    Text, Icon, colors, alignment, ScrollMode, border, padding, animation
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
        self.selected_function: Function = None

        # Список представлений карточек / параметров / результатов функций
        self.list_cards = []
        self.list_parameters = []
        self.list_results = []

        # Ссылки на элементы управления графической области
        self.ref_result_view = Ref[Column]()
        self.ref_cards_view = Ref[Column]()

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
                    self.create_cards_menu(),
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
    

    def create_cards_menu(self) -> Container:
        '''Создает меню представления созданных функций'''
        return Container(
            width = 350,
            bgcolor = colors.BLACK12,
            alignment = alignment.top_center,
            padding = padding.only(left=10, right=10),
            content = Column(
                tight = True,
                spacing = 10,
                scroll = ScrollMode.AUTO,
                ref = self.ref_cards_view,
                controls = self.list_cards
            )
        )
    

    def create_parameters_menu(self) -> Container:
        '''Создает меню параметров функции'''
        return Container(
            alignment = alignment.top_center,
            bgcolor = colors.BLACK12,
            animate_size = 100,
            content = Column(
                tight = True,
                scroll = ScrollMode.AUTO,
                controls = self.list_parameters
            )
        )
    

    def create_result_view(self) -> Container:
        return Container(
            expand = True,
            border = border.all(colors.BLACK),
            content = Column(
                tight = True,
                expand = True,
                scroll = ScrollMode.AUTO,
                ref = self.ref_result_view,
                controls = self.list_results
            ) 
        )
    

    def add_function(self, e) -> None:
        '''Добавляет функцию в список'''
        key = e.control.data
        if not key:
            return
        
        function = Function(self.page, self, key)
        
        self.list_cards.append(function.view.card_view)
        self.list_parameters.append(function.view.parameters_view)
        self.list_results.append(function.view.results_view)
        self.update()
    

    def delete_function(self, function: Function) -> None:
        '''Удаляет функцию из графической области'''
        self.list_cards.remove(function.view.card_view)
        self.list_parameters.remove(function.view.parameters_view)
        self.list_results.remove(function.view.results_view)
        self.update()


    def change_selected_function(self, clicked_function: Function) -> None:
        '''Изменяет текущую выбранную функцию'''
        clicked_function.change_selection()

        if clicked_function == self.selected_function:
            # Если нажата выбраная функция очищаем ссылку
            self.selected_function = None
        else:
            # Снимаем выделение с предыдущей выбранной функции, если она есть
            if self.selected_function is not None:
                self.selected_function.change_selection()
            # Устанавливаем ссылку на новую выбранную функцию
            self.selected_function = clicked_function
            
            self._scroll_view_to(self.ref_cards_view.current, clicked_function.id)
            self._scroll_view_to(self.ref_result_view.current, clicked_function.id)
        self.update()


    def _scroll_view_to(self, view: ScrollableControl, key: str | int) -> None:
        '''Прокручивает вью до элемента с заданным ключом'''
        view.scroll_to(
            key = str(key),
            duration = 500,
            curve = animation.AnimationCurve.FAST_OUT_SLOWIN
        )