from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ....function import Function

from .parameter_editor_interface import ParamEditorInterface
from ...function_typing import ParameterType, File

from typing import List
from dataclasses import dataclass, field
import os
import re
from flet import (
    Container, ControlEvent, Column, PopupMenuButton, Row,
    border, Ref, PopupMenuItem, Icon, MainAxisAlignment,
    icons, colors, IconButton, TextField, Markdown, Text,
    ScrollMode, animation
)



@dataclass
class DLFolder:
    name: str           = None
    items: List[File] = field(default_factory=list)

    def __post_init__(self):
        self.items = self._sort_folders_and_files()

    def _sort_folders_and_files(self):
        '''Сортировка папок и файлов'''
        folders = [item for item in self.items if isinstance(item, DLFolder)]
        files = [item for item in self.items if isinstance(item, File)]
        sorted_folders = sorted(folders, key=lambda x: x.name)
        sorted_files = sorted(files, key=lambda x: x.name)
        return sorted_folders + sorted_files


    @property
    def folder_count(self):
        return self._count_items(count_folders=True)

    @property
    def file_count(self):
        return self._count_items(count_folders=False)

    def _count_items(self, count_folders: bool):
        '''Подсчет количества папок или файлов в списке'''
        return sum(
            1 for item in self.items
            if (
                (count_folders and isinstance(item, DLFolder))
                or (not count_folders and isinstance(item, File))
            )
        )



@dataclass
class DLConfig:
    name: str                   = 'library_data'
    title: str                  = 'Выбор набора данных'
    valid_folders: List[str]    = field(default_factory=list)
    # TODO: add valid_file_types
    default_value: str | File = None

    @property
    def type(self) -> ParameterType:
        return ParameterType.DATA_LIBRARY
    
    def __post_init__(self):
        main_folder = self._create_folder()
        self.folders_files = main_folder.items
        self.all_files = self.get_all_files(main_folder)
        self.default_value = self.find_file_by_name(self.default_value) \
            if isinstance(self.default_value, str) else None

    def _create_folder(self, root: str = 'DATA') -> DLFolder:
        '''Создает структуру папок и файлов'''
        items = []
        for file in os.listdir(root):
            path = os.path.join(root, file)
            if os.path.isfile(path):
                items.append(File(path))
            elif os.path.isdir(path):
                if os.path.basename(path) in self.valid_folders:
                    folder = self._create_folder(path)
                    if folder.file_count > 0 or folder.folder_count > 0:
                        items.append(folder)
        return DLFolder(name=os.path.basename(root), items=items)
    
    def get_all_files(self, folder: DLFolder) -> List[File]:
        '''Получение всех файлов в папке'''
        files = [item for item in folder.items if isinstance(item, File)]
        for item in folder.items:
            if isinstance(item, DLFolder):
                files.extend(self.get_all_files(item))
        return files

    def find_file_by_name(self, file_name: str) -> File:
        '''Поиск файла по имени'''
        return next((
            item for item in self.all_files
            if (item.name == file_name and item.folder in self.valid_folders)
        ), None)
    


class DataLibraryEditor(ParamEditorInterface, Container):
    def __init__(self, function: 'Function', config: DLConfig = DLConfig()):
        self._type = ParameterType.DATA_LIBRARY
        self.function = function
        
        self._name = config.name
        self.title = config.title
        self.valid_folders = config.valid_folders
        self.all_files = config.all_files
        self.folders_files = config.folders_files
        self.default_value = config.default_value

        self.selected_file = self.default_value

        self.ref_selected_file_option = Ref[Container]()

        super().__init__()
        self._set_styles()
        self.content = self._create_content()


    def _create_content(self) -> Column:
        '''Создает содержимое элемента'''
        return Column(
            controls=[
                self._create_popup_menu_button(),
                self._create_textfield_search(),
            ]
        )
    

    def _create_popup_menu_button(self) -> Row:
        '''Создание меню выбора'''
        self.ref_title = Ref[Text]()
        self.ref_cancel = Ref[IconButton]()
        menu_button = PopupMenuButton(
            expand = True,
            tooltip = None,
            content = Container(
                content = Row(
                    controls=[
                        Icon(icons.FILE_OPEN_OUTLINED),
                        Text(
                            ref = self.ref_title,
                            value = self.title if self.default_value is None \
                                else self.default_value.formatted_name,
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
        )
        cancel_button = IconButton(
            ref = self.ref_cancel,
            visible = self.default_value is not None,
            icon = icons.CLOSE,
            tooltip = "Отменить выбор",
            on_click = self._on_cancel
        )
        return Row(
            spacing=0,
            controls=[
                menu_button,
                cancel_button
            ]
        )


    def _create_menu(self, structure: List[DLFolder | File]):
        '''Создание элементов оснровного меню'''
        menu_items = []
        for item in structure:
            if isinstance(item, File):
                menu_items.append(self._create_manu_items(item))
            elif isinstance(item, DLFolder):
                submenu = self._create_menu(item.items)
                menu_items.append(PopupMenuItem(
                    content=self._create_submenu(item, submenu)
                ))
        return menu_items
    

    def _create_manu_items(self, file: File) -> PopupMenuItem:
        '''Создание элемента меню'''
        return PopupMenuItem(
            content = Row(
                alignment = MainAxisAlignment.SPACE_BETWEEN,
                controls = [
                    Text(file.name),
                    Text(f"({file.size_formatted})"),
                ]
            ),
            data = file,
            on_click = self._on_change
        )
    

    def _create_submenu(self, item: DLFolder, submenu: List[DLFolder | File]):
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
    

    def _create_textfield_search(self) -> Column:
        '''Создание элемента поиска'''
        self.ref_textfield = Ref[TextField]()
        self.ref_files_options = Ref[Column]()
        return Column([
            TextField(
                ref = self.ref_textfield,
                label = "Поиск файла",
                hint_text = "Введите имя файла",
                border_radius = 5,
                dense = True,
                on_change = self._on_change_textfield
            ),
            Column(
                ref = self.ref_files_options,
                scroll = ScrollMode.AUTO,
            )
        ])
    

    def _on_change_textfield(self, e: ControlEvent) -> None:
        '''Обработка изменения текстового поля'''
        self._set_files_options()


    def _set_files_options(self) -> None:
        '''Создание списка опций выбора файла'''
        input_str = self.ref_textfield.current.value
        files_options = self.suggest_files(input_str)

        options_control = self.ref_files_options.current
        options_control.height = 400 if len(files_options) > 10 else None
        options_control.controls = [
            self._create_file_option(file, input_str)            
            for file in files_options
        ]
        if self.selected_file is not None:
            options_control.scroll_to(
                key = self.selected_file.path,
                duration = 500,
                curve = animation.AnimationCurve.FAST_OUT_SLOWIN
            )
        self._set_textfield_counter_text()
        options_control.update()


    def _set_textfield_counter_text(self) -> None:
        '''Обновление текста счетчика'''
        count = len(self.ref_files_options.current.controls)
        textfield = self.ref_textfield.current
        textfield.counter_text = f"Найдено: {count}" if count > 0 else None
        textfield.update()


    def suggest_files(self, input_str: str) -> List[File]:
        '''Поиск файла по имени'''
        if input_str == "":
            return []
        input_str = input_str.lower()
        matching_files = [
            file for file in self.all_files
            if input_str in file.data_path.lower()
        ]
        matching_files.sort(
            key=lambda x: abs(len(x.data_path)) - len(input_str) - x.data_path.lower().count(input_str)
        )
        return matching_files


    def _create_file_option(self, file: File, input_str: str) -> Container:
        '''Создание опции выбора файла'''
        formatted_name = re.sub(f"(?i){re.escape(input_str)}", r"**\g<0>**", file.data_path)
        border_color = colors.WHITE38
        if (self.selected_file is not None and file.path == self.selected_file.path):
            border_color = colors.BLUE
        return Container(
            content = Row(
                alignment = MainAxisAlignment.SPACE_BETWEEN,
                controls = [
                    Markdown(formatted_name, expand=True),
                    Text(f"({file.size_formatted}, {file.extension})"),
                ]
            ),
            key = file.path,
            width = 320,
            padding = 5,
            border_radius = 5,
            border = border.all(1, border_color),
            data = file,
            on_hover = self._on_hover,
            on_click = self._on_change,
        )
    

    def _on_hover(self, e: ControlEvent):
        '''Устанавливает тень вокруг индикатора'''
        e.control.bgcolor = colors.WHITE12 \
            if e.data == "true" and e.control.data != self.selected_file else None
        e.control.update()
    

    def _on_cancel(self, e: ControlEvent) -> None:
        '''Отмена выбора'''
        self.ref_title.current.value = self.title
        self.ref_cancel.current.visible = False
        self.selected_file = None

        self._set_files_options()

        self.function.calculate.set_parameter_value(self._name, None)
        self.update()


    def _on_change(self, e: ControlEvent) -> None:
        '''Обновляет значение параметр в экземпляре класса Function'''
        value = e.control.data
        self.ref_cancel.current.visible = value is not None
        self.ref_title.current.value = value.formatted_name

        self.selected_file = value
        if self.ref_selected_file_option.current is not None: 
            self.ref_selected_file_option.current.bgcolor = None
        
        self._set_files_options()

        self.function.calculate.set_parameter_value(self._name, value)
        self.update()
