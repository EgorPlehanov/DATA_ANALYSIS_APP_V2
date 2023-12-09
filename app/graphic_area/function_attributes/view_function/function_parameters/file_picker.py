from .parameter_editor_interface import ParamEditorInterface
from ...function_typing import ParameterType

from typing import List, Any
from dataclasses import dataclass, field
from collections import namedtuple
from flet import (
    Container, FilePickerFileType, FilePicker, Ref,
    Text, Column, ElevatedButton, Row, icons, MainAxisAlignment,
    FilePickerResultEvent, IconButton, colors, padding
)


@dataclass
class FPSettings:
    dialog_title: str               = 'Выбор набора данных'
    initial_directory: str          = None
    file_type: FilePickerFileType   = FilePickerFileType.CUSTOM
    allowed_extensions: List[str]   = field(default_factory=lambda: [
        'csv', 'xls', 'xlsx', 'xlsm', 'xlsb', 'odf', 'ods', 'odt', 'json', 'txt', 'dat'
    ])
    allow_multiple: bool            = True

@dataclass
class FPConfig:
    name: str               = ''
    title: str              = 'Набор данных'
    button_text: str        = 'Выбрать файл данных'
    settings: FPSettings    = FPSettings()
    default_value: Any      = field(default_factory=list)

    @property
    def type(self) -> ParameterType:
        return ParameterType.FILE_PICKER


class FilePickerEditor(ParamEditorInterface, Container):
    FileData = namedtuple('FileData', ['name', 'path', 'size'])

    def __init__(self, function, config: FPConfig = FPConfig()):
        self._type = ParameterType.FILE_PICKER
        self.function = function

        self._name = config.name
        self.title = config.title
        self.button_text = config.button_text
        self.settings = config.settings
        self.default_value = config.default_value

        self.ref_files = Ref[Column]()
        self.list_picked_files = []
        self.file_picker_dialog = self._create_file_picker_dialog()

        super().__init__()
        self._set_styles()
        self.content = self._create_content()


    def _create_file_picker_dialog(self) -> FilePicker:
        '''Создает диалоговое окно выбора файлов'''
        file_picker_dialog = FilePicker(
            on_result=self._on_change,
        )
        self.function.page.overlay.append(file_picker_dialog)
        self.function.page.update()
        return file_picker_dialog
    

    def _create_content(self) -> Column:
        '''Создает содержимое редактора'''
        return Column([
            Row(
                alignment = MainAxisAlignment.SPACE_BETWEEN,
                controls = [
                    Text(self.title),
                    ElevatedButton(
                        text = self.button_text,
                        icon = icons.UPLOAD_FILE,
                        on_click = self._open_file_picker
                    )
                ],
            ),
            Row([Column(ref = self.ref_files)])
        ])
    

    def _open_file_picker(self, e):
        '''Открывает диалоговое окно выбора файлов'''
        self.file_picker_dialog.pick_files(
            dialog_title        = self.settings.dialog_title,
            initial_directory   = self.settings.initial_directory,
            file_type           = self.settings.file_type,
            allowed_extensions  = self.settings.allowed_extensions,
            allow_multiple      = self.settings.allow_multiple,
        )
    

    def _on_change(self, e: FilePickerResultEvent) -> None:
        '''Обновляет список файлов в параметре экземпляра класса Function'''
        self.list_picked_files = []
        if e.files is not None:
            for file in e.files:
                self.list_picked_files.append(
                    self.FileData(
                        name = file.name,
                        path = file.path,
                        size = file.size,
                    )
                )
            self.function.calculate.set_parameter_value(self._name, self.list_picked_files)
            self._update_picked_files()
    

    def _update_picked_files(self):
        '''Обновляет список файлов в редакторе'''
        self.ref_files.current.controls = [
            Container(
                bgcolor = colors.WHITE10,
                border_radius = 20,
                padding = padding.only(right=15),
                content = Row(
                    spacing = 0,
                    controls = [
                        IconButton(
                            icon = icons.CLOSE,
                            icon_size = 14,
                            tooltip = "Удалить",
                            data = idx,
                            on_click = self._delete_file,
                        ),
                        Text(f"{file.name} ({self._convert_size(file.size)})")
                    ]
                )
            )
            for idx, file in enumerate(self.list_picked_files) 
        ]
        self.update()


    
    def _delete_file(self, e):
        '''Удаляет выбранный файл'''
        file_idx = e.control.data
        self.list_picked_files.remove(self.list_picked_files[file_idx])
        self.function.calculate.set_parameter_value(self._name, self.list_picked_files)
        self._update_picked_files()
    

    def _convert_size(self, size):
        '''Конвертирует размер файла в байтах в строку'''
        if not size:
            return "0 байт"
        elif size < 1024:
            return f"{size} байт"
        elif size < 1024 * 1024:
            return f"{size / 1024:.2f} КБ"
        elif size < 1024 * 1024 * 1024:
            return f"{size / (1024 * 1024):.2f} МБ"
        else:
            return f"{size / (1024 * 1024 * 1024):.2f} ГБ"
    