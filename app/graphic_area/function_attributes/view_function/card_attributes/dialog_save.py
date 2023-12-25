from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ....function import Function

import os
import numpy as np
import soundfile as sf
from scipy.io import wavfile
from flet import (
    FilePicker, FilePickerResultEvent, FilePickerFileType, ControlEvent
)


class DialogSaveResultData(FilePicker):
    def __init__(self, function: "Function"):
        super().__init__()
        self.function = function

        self.initial_directory = os.path.join(
            os.path.abspath(__file__).split('\\app')[0],
            'DATA\\User_Saved_Data\\'
        )
        self.on_result = self._save_result_data
    

    def open_dialog(self, e: ControlEvent) -> None:
        '''Открывает диалоговое окно cохранения результата'''
        parameters_text = self._create_parameters_text()
        self.save_file(
            dialog_title = f"Сохрание результата функции {self.function.formatted_name}",
            file_name = f"{self.function.name}({parameters_text}).csv",
            file_type = FilePickerFileType.CUSTOM,
            allowed_extensions = ['csv', 'json', 'wav'],
            initial_directory = self.initial_directory,
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

        if file_format not in ['csv', 'json', 'wav']:
            path = f'{path}.csv'
            file_format = 'csv'

        try:
            data_to_save = self.function.get_result_main_data()
            with open(path, 'w') as file:
                match file_format:
                    case 'csv':
                        data_to_save.to_csv(file, index=False)
                    case 'json':
                        data_to_save.to_json(file, orient='records')
                    case 'wav':
                            self.save_dataframe_as_wav(data_to_save, path)
                    case _:
                        raise Exception(f'Неизвестный формат файла: {file_format}')
                        
        except Exception as ex:
            print(f'Ошибка при сохранении: {ex}')


    def save_dataframe_as_wav(self, df, path):
        '''Сохраняет DataFrame в WAV файл'''
        time_column = df.iloc[:, 0].copy()
        amp_column = df.iloc[:, 1].copy()
        
        amp_column_normalized = (
            (amp_column - amp_column.min()) 
            / (amp_column.max() - amp_column.min())
        )

        audio_data = amp_column_normalized.to_numpy(dtype=np.float32)
        sample_rate = int(1 / np.mean(np.diff(time_column)))
        wavfile.write(path, sample_rate, audio_data)
