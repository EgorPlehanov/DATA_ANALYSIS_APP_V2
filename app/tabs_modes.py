from .graphic_area.graphic_area import GraphicArea

from dataclasses import dataclass
from typing import Any


@dataclass
class TabMode:
    type: str               = "unknown"          # Код режима
    name: str               = "Не задано"        # Название режима
    dialog_title: str       = "Добавить вкладку" # Название в диалоговом окне создания вкладки
    tab_icon: str           = "question_mark"    # Иконка вкладки
    default_tab_title: str  = "Новая вкладка"    # Название вкладки по умолчанию
    tab_content: Any        = None               # Ф-ция для создания обекта в кладки


class TabsModes:
    @staticmethod
    def get_tabs_modes() -> dict[str, TabMode]:
        '''Возвращает словарь режимов работы вкладок'''
        return {
            mode.type: mode
            for mode in TabsModes.modes
        }
    

    modes = [
        TabMode(
            type = "graphic",
            name = "Графики",
            dialog_title = "Добавить вкладку\nдля работы с графиками",
            tab_icon = "area_chart",
            default_tab_title = 'Графики',
            tab_content = GraphicArea
        ),
        TabMode(
            type = "image",
            name = "Изображения",
            dialog_title = "Добавить вкладку\nдля работы с изображениями",
            tab_icon = "image",
            default_tab_title = 'Изображения',
            tab_content = lambda app, page: None
        )
    ]
