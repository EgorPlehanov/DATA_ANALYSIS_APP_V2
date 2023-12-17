from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ....function import Function

import os
from flet import FilePicker, FilePickerResultEvent, FilePickerFileType, ControlEvent


class DialogSaveResultData(FilePicker):
    def __init__(self, function: "Function"):
        super().__init__()
        self.function = function

        self.on_result = self._save_result_data
    

    def open_dialog(self, e: ControlEvent) -> None:
        '''Открывает диалоговое окно cохранения результата'''
        parameters_text = self._create_parameters_text()
        self.save_file(
            dialog_title = f"Сохрание результата функции {self.function.formatted_name}",
            file_name = f"{self.function.name}({parameters_text}).csv",
            file_type = FilePickerFileType.CUSTOM,
            allowed_extensions = ['csv', 'json'],
        )


    def _create_parameters_text(self) -> str:
        '''Создает строку с параметрами'''
        parameters_text = "; ".join([
            f"{param}={value}".replace(': ', '-')
            for param, value in self.function.calculate.get_current_parameters_formatted().items()
            if 'show' not in param
        ])
        return (parameters_text[:100] + '...') if len(parameters_text) > 100 else parameters_text


    def _save_result_data(self, e: FilePickerResultEvent) -> None:
        '''Сохраняет результаты в файл'''
        path = e.path
        if not path:
            return
        file_format = os.path.splitext(path)[-1][1:].lower()

        if file_format not in ['csv', 'json']:
            path = f'{path}.csv'
            file_format = 'csv'

        try:
            with open(path, 'w') as file:
                data_to_save = self.function.get_result_main_data()
                match file_format:
                    case 'csv':
                        data_to_save.to_csv(file, index=False)
                    case 'json':
                        data_to_save.to_json(file, orient='records')
                    case _:
                        raise Exception(f'Неизвестный формат файла: {file_format}')
                        
        except Exception as ex:
            print(f'Ошибка при сохранении: {ex}')
