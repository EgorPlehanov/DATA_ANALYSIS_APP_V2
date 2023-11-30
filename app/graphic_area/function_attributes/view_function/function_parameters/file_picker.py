from .param_editor_interface import ParamEditorInterface

from typing import List, Any
from dataclasses import dataclass, field
from flet import (
    Container, FilePickerFileType, FilePicker, Ref, Text, Column, ElevatedButton, Row, icons
)


@dataclass
class FilePickerSettings:
    dialog_title: str               = 'Выбор набора данных'
    initial_directory: str          = None
    file_type: FilePickerFileType   = FilePickerFileType.ANY
    allowed_extensions: List[str]   = field(default_factory=lambda: [
        'csv', 'xls', 'xlsx', 'xlsm', 'xlsb', 'odf', 'ods', 'odt', 'json', 'txt', 'dat'
    ])
    allow_multiple: bool            = True


class FilePickerEditor(ParamEditorInterface, Container):
    def __init__(self,
        param_name: str                             = '',
        title: str                                  = 'Набор данных',
        button_text: str                            = 'Выбрать файл данных',
        pick_files_parameters: FilePickerSettings   = FilePickerSettings(),
        default_value: Any                          = []
    ):
        self._type = 'file_picker'
        self._param_name = param_name
        self.title = title
        self.button_text = button_text
        self.pick_files_parameters = pick_files_parameters
        self.default_value = default_value

        super().__init__()
        self.set_styles()
        self.content = self.create_content()


    def create_control(self) -> Row:
        ref_files = Ref[Column]()
        pick_files_dialog = FilePicker(
            data={'ref_files': ref_files},
            on_result=self.on_change,
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
                            ref=ref_files,
                        ),
                        ElevatedButton(
                            text=self.button_text,
                            icon=icons.UPLOAD_FILE,
                            on_click=lambda _: pick_files_dialog.pick_files(
                                dialog_title = self.pick_files_parameters.dialog_title,
                                initial_directory = self.pick_files_parameters.initial_directory,
                                file_type = self.pick_files_parameters.file_type
                                    if self.pick_files_parameters.file_type is None else FilePickerFileType.CUSTOM,
                                allowed_extensions = self.pick_files_parameters.allowed_extensions,
                                allow_multiple = self.pick_files_parameters.allow_multiple,
                            ),
                        ),
                    ]
                )
            ],
            expand=True,
        )
        return editor_file_picker
    

    def on_change(self, e) -> None:
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
    