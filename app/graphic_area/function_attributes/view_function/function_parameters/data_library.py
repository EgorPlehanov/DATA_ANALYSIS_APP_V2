from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ....function import Function

from .parameter_editor_interface import ParamEditorInterface
from .parameters_utils import convert_size
from ...function_typing import ParameterType

from typing import List
from dataclasses import dataclass, field
import os
from flet import (
    Container, ControlEvent, Column, PopupMenuButton, Row, border, IconButton,
    PopupMenuItem, Text, Icon, icons, MainAxisAlignment, colors, Ref
)



@dataclass
class DLFile:
    path: str = None

    def __post_init__(self):
        self.name = os.path.basename(self.path)
        self.extension = self.path.split('.')[-1].lower()
        self.size = convert_size(os.path.getsize(self.path))
        self.fomatted_name = f"{self.name} ({self.size})"



@dataclass
class DLFolder:
    name: str           = None
    items: List[DLFile] = field(default_factory=list)

    def __post_init__(self):
        self.items = self._sort_folders_and_files()
        self.folder_count = self._count_items(count_folders=True)
        self.file_count = self._count_items(count_folders=False)


    def _sort_folders_and_files(self):
        '''Сортировка папок и файлов'''
        folders = [item for item in self.items if isinstance(item, DLFolder)]
        files = [item for item in self.items if isinstance(item, DLFile)]
        sorted_folders = sorted(folders, key=lambda x: x.name)
        sorted_files = sorted(files, key=lambda x: x.name)
        return sorted_folders + sorted_files


    def _count_items(self, count_folders: bool):
        '''Подсчет количества папок или файлов в списке'''
        return sum(
            1 for item in self.items
            if (
                (count_folders and isinstance(item, DLFolder))
                or (not count_folders and isinstance(item, DLFile))
            )
        )



@dataclass
class DLConfig:
    name: str                   = 'library_data'
    title: str                  = 'Выбор набора данных'
    valid_folders: List[str]    = field(default_factory=list)
    default_value: str | DLFile = None

    @property
    def type(self) -> ParameterType:
        return ParameterType.DATA_LIBRARY
    
    def __post_init__(self):
        self.folders_files = self._create_folder().items
        self.default_value = self.find_file_by_name(self.default_value) \
            if isinstance(self.default_value, str) else None


    def _create_folder(self, root: str = 'DATA') -> DLFolder:
        '''Создает структуру папок и файлов'''
        items = []
        for file in os.listdir(root):
            path = os.path.join(root, file)
            if os.path.isfile(path):
                items.append(DLFile(path))
            elif os.path.isdir(path):
                if os.path.basename(path) in self.valid_folders:
                    items.append(self._create_folder(path))
        return DLFolder(name=os.path.basename(root), items=items)
    

    def find_file_by_name(self, file_name: str) -> DLFile:
        '''Поиск файла по имени'''
        return self._find_file_by_name(self.folders_files, file_name)


    def _find_file_by_name(self,
        items: List[DLFile | DLFolder],
        file_name: str
    ) -> DLFile:
        '''Поиск файла по имени'''
        for item in items:
            if isinstance(item, DLFile) and item.name == file_name:
                return item
            elif isinstance(item, DLFolder):
                if item.name not in self.valid_folders:
                    continue
                found_file = self._find_file_by_name(item.items, file_name)
                if found_file:
                    return found_file
        return None



class DataLibraryEditor(ParamEditorInterface, Container):
    def __init__(self, function: 'Function', config: DLConfig = DLConfig()):
        self._type = ParameterType.DATA_LIBRARY
        self.function = function
        
        self._name = config.name
        self.title = config.title
        self.valid_folders = config.valid_folders
        self.folders_files = config.folders_files
        self.default_value = config.default_value

        self.ref_title = Ref[Text]()
        self.ref_cancel = Ref[IconButton]()

        super().__init__()
        self._set_styles()
        self.content = self._create_content()


    def _create_content(self) -> Column:
        return Row(
            spacing=0,
            controls=[
                PopupMenuButton(
                    expand = True,
                    tooltip = None,
                    animate_size = 1000,
                    content = Container(
                        content = Row(
                            controls=[
                                Icon(icons.FILE_OPEN_OUTLINED),
                                Text(
                                    ref = self.ref_title,
                                    value = self.title if self.default_value is None else self.default_value.fomatted_name,
                                    size = 16
                                ),
                            ],
                        ),
                        tooltip = None,
                        border = border.all(1, colors.BLACK),
                        padding = 5,
                        border_radius = 5,
                    ),
                    items = self._create_menu(self.folders_files)
                ),
                IconButton(
                    ref = self.ref_cancel,
                    visible = self.default_value is not None,
                    icon = icons.CLOSE,
                    tooltip = "Отменить выбор",
                    on_click = self._on_cancel
                )
            ]
        )
    

    def _create_menu(self, structure: List[DLFolder | DLFile]):
        '''Создание элементов оснровного меню'''
        menu_items = []

        for item in structure:
            if isinstance(item, DLFile):
                menu_items.append(PopupMenuItem(
                    content = Row(
                        alignment = MainAxisAlignment.SPACE_BETWEEN,
                        controls = [
                            Text(f"{item.name}"),
                            Text(f"({item.size})"),
                        ]
                    ),
                    data = item,
                    on_click = self._on_change
                ))
            elif isinstance(item, DLFolder):
                submenu = self._create_menu(item.items)
                menu_items.append(PopupMenuItem(
                    content=self._create_menu_item(item, submenu)
                ))

        return menu_items
    

    def _create_menu_item(self, item: DLFolder, submenu: List[DLFolder | DLFile]):
        '''Создание подменю'''
        return PopupMenuButton(
            items = submenu,
            content = Row(
                alignment = MainAxisAlignment.SPACE_BETWEEN,
                controls = [
                    Row([
                        Icon(icons.FOLDER),
                        Text(item.name),
                    ]),
                    self._create_folders_and_files_count(item),
                ],
            ),
        )
    

    def _create_folders_and_files_count(self, item: DLFolder) -> Column:
        '''Создание столбца с количеством папок и файлов'''
        controls = []
        if item.folder_count > 0:
            controls.append(Text(f"папки:\t{item.folder_count}"))
        if item.file_count > 0:
            controls.append(Text(f"файлы:\t{item.file_count}"))
        return Column(controls=controls, spacing=0)
    

    def _on_cancel(self, e: ControlEvent) -> None:
        '''Отмена выбора'''
        self.ref_title.current.value = self.title
        self.ref_cancel.current.visible = False
        self.function.calculate.set_parameter_value(self._name, None)
        self.update()


    def _on_change(self, e: ControlEvent) -> None:
        '''Обновляет значение параметр в экземпляре класса Function'''
        value = e.control.data
        self.ref_cancel.current.visible = value is not None
        self.ref_title.current.value = value.fomatted_name
        self.function.calculate.set_parameter_value(self._name, value)
        self.update()
