from .parameter_editor_interface import ParamEditorInterface
from ...function_typing import ParameterType

from typing import List, Any
from dataclasses import dataclass, field
from flet import (
    Container, FilePickerFileType, FilePicker, Ref,
    Text, Column, ElevatedButton, Row, icons
)


@dataclass
class FPSettings:
    dialog_title: str               = 'Выбор набора данных'
    initial_directory: str          = None
    file_type: FilePickerFileType   = FilePickerFileType.ANY
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
    def __init__(self, function, config: FPConfig = FPConfig()):
        self.function = function

        self._type = ParameterType.FILE_PICKER
        self._name = config.name
        self.title = config.title
        self.button_text = config.button_text
        self.settings = config.settings
        self.default_value = config.default_value

        super().__init__()
        self._set_styles()
        self.content = self._create_content()

        self.ref_files = Ref[Column]()


    def _create_content(self) -> Row:
        pick_files_dialog = FilePicker(
            data={'ref_files': self.ref_files},
            on_result=self._on_change,
        )
        self.page.overlay.append(pick_files_dialog)
        self.page.update()

        editor_file_picker = Row(
            controls=[
                Column(
                    controls=[
                        Text(value=self.title),
                        Column(
                            # controls=[
                            #     Text(f"{file['name']} ({self._convert_size(file['size'])})")
                            #     for file in (current_value if current_value is None else [])
                            # ],
                            ref=self.ref_files,
                        ),
                        ElevatedButton(
                            text=self.button_text,
                            icon=icons.UPLOAD_FILE,
                            on_click=lambda _: pick_files_dialog.pick_files(
                                dialog_title = self.settings.dialog_title,
                                initial_directory = self.settings.initial_directory,
                                file_type = self.settings.file_type
                                    if self.settings.file_type is None else FilePickerFileType.CUSTOM,
                                allowed_extensions = self.settings.allowed_extensions,
                                allow_multiple = self.settings.allow_multiple,
                            ),
                        ),
                    ]
                )
            ],
            expand=True,
        )
        return editor_file_picker
    

    def _on_change(self, e) -> None:
        '''
        Обновляет список файлов в параметре экземпляра класса Function
        '''
        files_list = []
        if e.files is not None:
            for file in e.files:
                files_list.append({
                    'name': file.name,
                    'path': file.path,
                    'size': file.size,
                })

            files = e.control.data.get('ref_files').current
            files.controls = [
                Text(f"{file['name']} ({self._convert_size(file['size'])})")
                for file in files_list
            ]

            # self.function.set_parameter_value(
            #     self._param_name, files_list, [file['name'] for file in files_list]
            # )
            # self.update_function_card()
    