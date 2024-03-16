from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .workplace import Workplace

from flet import *
from copy import deepcopy

from .node.node import *
from .menubar_tools import *
from .node.node_library import *



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
                content = Row([Icon(icons.ADD_CARD), Text("Ноды")]),
                controls = self.create_submenu(
                    NodeLibrary.get_nodes_configs()
                )
            ),
            SubmenuButton(
                content = Row([Icon(icons.HARDWARE), Text("Инструменты")]),
                controls = self.create_submenu(
                    MenubarTools.get_menubar_tools()
                )
            )
        ]
    

    def create_submenu(self, obj_list):
        items = []
        for obj in obj_list:
            if isinstance(obj, Folder):
                items.append(
                    SubmenuButton(
                        content = Row([Icon(obj.icon), Text(obj.name)]),
                        controls = self.create_submenu(obj.obj_list)
                    )
                )
            else:
                items.append(
                    MenuItemButton(
                        content = Row(
                            [Icon(obj.icon), Text(obj.name)] if obj.icon else [Text(obj.name)]
                        ),
                        style = ButtonStyle(bgcolor={MaterialState.HOVERED: colors.BLUE}),
                        on_click = (lambda obj: lambda e: (
                            obj.function(self) if isinstance(obj, Tool)
                            else self.workplace.node_area.add_node(config=obj)
                        ))(obj),
                    )
                )
        return items
    