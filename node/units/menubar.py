from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .workplace import Workplace

from flet import *

from .node import *



class FunctionMenuBar(MenuBar):
    def __init__(self, page: Page, workplace: "Workplace"):
        super().__init__()
        self.page = page
        self.workplace = workplace

        self.expand = True
        self.controls = self.create_controls()

        self.menu_style = MenuStyle(
            # bgcolor = colors.RED,
            shadow_color = colors.BLACK38,
            bgcolor={
                MaterialState.HOVERED: colors.WHITE,
                MaterialState.FOCUSED: colors.BLUE,
                MaterialState.DEFAULT: colors.BLACK,
            }
        )

    def create_controls(self):
        return [
            SubmenuButton(
                content = Row([Icon(icons.ADD_CARD), Text("Добавить ноду")]),
                controls = [
                    SubmenuButton(
                        content = Text("Данные"),
                        leading = Icon(icons.DATA_OBJECT),
                        controls = [
                            
                            SubmenuButton(
                                content = Text("TEST"),
                                leading = Icon(icons.QUESTION_MARK),
                                controls = [
                                    MenuItemButton(
                                        content = Text("Тестовая 0->2"),
                                        style = ButtonStyle(bgcolor={MaterialState.HOVERED: colors.BLUE}),
                                        on_click = lambda e: self.workplace.node_area.add_node(
                                            config=NodeConfig(
                                                name = "Тестовая 0->2",
                                                parameters = [
                                                    OutParamConfig(name = "Param ", connect_point_color = "green"),
                                                    OutParamConfig(name = "Param ", connect_point_color = "blue", has_connect_point = False),
                                                ]
                                            )
                                        ),
                                        # on_hover=handle_on_hover,
                                    ),
                                    MenuItemButton(
                                        content = Text("Тестовая 3->0"),
                                        style = ButtonStyle(bgcolor={MaterialState.HOVERED: colors.BLUE}),
                                        on_click = lambda e: self.workplace.node_area.add_node(
                                            config=NodeConfig(
                                                name = "Тестовая 3->0",
                                                parameters = [
                                                    SVParamConfig(name = "Param ", connect_point_color = "red"),
                                                    SVParamConfig(name = "Param ", connect_point_color = "orange", has_connect_point = False),
                                                    SVParamConfig(name = "Param ", connect_point_color = "purple"),
                                                ]
                                            )
                                        ),
                                        # on_hover=handle_on_hover,
                                    ),
                                    MenuItemButton(
                                        content = Text("Тестовая 3->2"),
                                        style = ButtonStyle(bgcolor={MaterialState.HOVERED: colors.BLUE}),
                                        on_click = lambda e: self.workplace.node_area.add_node(
                                            config=NodeConfig(
                                                name = "Тестовая 3->2",
                                                parameters = [
                                                    OutParamConfig(name = "Param ", connect_point_color = "green", has_connect_point = False),
                                                    OutParamConfig(name = "Param ", connect_point_color = "blue"),

                                                    SVParamConfig(name = "Param ", connect_point_color = "red"),
                                                    SVParamConfig(name = "Param ", connect_point_color = "orange"),
                                                    SVParamConfig(name = "Param ", connect_point_color = "purple", has_connect_point = False),
                                                ]
                                            )
                                        ),
                                        # on_hover=handle_on_hover,
                                    ),
                                ]
                            ),

                            MenuItemButton(
                                content = Text("Открыть изображение"),
                                style = ButtonStyle(bgcolor={MaterialState.HOVERED: colors.BLUE}),
                                # on_click=handle_color_click,
                                # on_hover=handle_on_hover,
                            ),
                            MenuItemButton(
                                content = Text("Библиотека изображений"),
                                style = ButtonStyle(bgcolor={MaterialState.HOVERED: colors.BLUE}),
                                # on_click=handle_color_click,
                                # on_hover=handle_on_hover,
                            ),
                        ]
                    ),
                    SubmenuButton(
                        content = Text("Обработка"),
                        leading = Icon(icons.EDIT_NOTE),
                        controls = [
                            MenuItemButton(
                                content=Text("Фильтр"),
                                style=ButtonStyle(bgcolor={MaterialState.HOVERED: colors.GREEN}),
                                # on_click=handle_color_click,
                                # on_hover=handle_on_hover,
                            )
                        ]
                    )
                ]
            ),
            SubmenuButton(
                content = Row([Icon(icons.HARDWARE), Text("Инструменты")]),
                controls = [
                    SubmenuButton(
                        content = Row([Icon(icons.SEARCH), Text("Масштабирование")]),
                        controls = [
                            MenuItemButton(
                                content = Row([Icon(icons.ZOOM_IN), Text("Увеличить")]),
                                style = ButtonStyle(bgcolor={MaterialState.HOVERED: colors.BLUE}),
                                # on_click=handle_color_click,
                                # on_hover=handle_on_hover,
                            ),
                            MenuItemButton(
                                content = Row([Icon(icons.ZOOM_OUT), Text("Уменьшить")]),
                                style = ButtonStyle(bgcolor={MaterialState.HOVERED: colors.BLUE}),
                                # on_click=handle_color_click,
                                # on_hover=handle_on_hover,
                            ),
                            MenuItemButton(
                                content = Row([Icon(icons.SETTINGS_OVERSCAN), Text("Сбросить масштаб")]),
                                style = ButtonStyle(bgcolor={MaterialState.HOVERED: colors.BLUE}),
                                # on_click=handle_color_click,
                                # on_hover=handle_on_hover,
                            )
                        ]
                    ),
                    SubmenuButton(
                        content = Row([Icon(icons.CONTROL_POINT_DUPLICATE), Text("Выделение")]),
                        controls = [
                            MenuItemButton(
                                content = Row([Icon(icons.SELECT_ALL), Text("Выбрать все")]),
                                style = ButtonStyle(bgcolor={MaterialState.HOVERED: colors.BLUE}),
                                on_click = self.workplace.node_area.select_all,
                                # on_hover=handle_on_hover,
                            ),
                            MenuItemButton(
                                content = Row([Icon(icons.DESELECT), Text("Снять выделение")]),
                                style = ButtonStyle(bgcolor={MaterialState.HOVERED: colors.BLUE}),
                                on_click = self.workplace.node_area.clear_selection,
                                # on_hover=handle_on_hover,
                            ),
                            MenuItemButton(
                                content = Row([Icon(icons.SWAP_HORIZ), Text("Инвертировать выделение")]),
                                style = ButtonStyle(bgcolor={MaterialState.HOVERED: colors.BLUE}),
                                on_click = self.workplace.node_area.invert_selection,
                                # on_hover=handle_on_hover,
                            ),
                            MenuItemButton(
                                content = Row([Icon(icons.CENTER_FOCUS_STRONG_SHARP), Text("Переместить выделеные в начало")]),
                                style = ButtonStyle(bgcolor={MaterialState.HOVERED: colors.BLUE}),
                                on_click = self.workplace.node_area.move_selection_to_start,
                                # on_hover=handle_on_hover,
                            ),
                            MenuItemButton(
                                content = Row([Icon(icons.DELETE_SWEEP), Text("Удалить выбранные")]),
                                style = ButtonStyle(bgcolor={MaterialState.HOVERED: colors.BLUE}),
                                on_click = self.workplace.node_area.delete_selected_nodes,
                                # on_hover=handle_on_hover,
                            ),
                        ]
                    ),
                ]
            )
        ]
    