from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ....view_function.function_parameters.data_library import DLFile

from ....function_typing import FunctionResult

import numpy as np
import pandas as pd
import csv
import wave


def data_library(
    library_data: 'DLFile'    # файл
) -> FunctionResult:
    '''
    Обрабатывает данные из файлов
    '''
    if library_data is None:
        return FunctionResult()

    name = library_data.name
    path = library_data.path
    extension = library_data.extension

    try:
        match extension:
            case 'csv':
                # Определение разделителя
                with open(path, 'r', newline='') as csvfile:
                    sample_data = csvfile.read(1024)
                    sniffer = csv.Sniffer()
                    delimiter = sniffer.sniff(sample_data).delimiter
                # Чтение CSV файла с указанием определенного разделителя
                data = pd.read_csv(path, delimiter=delimiter)
            case 'xls' | 'xlsx' | 'xlsm' | 'xlsb' | 'odf' | 'ods' | 'odt':
                data = pd.read_excel(path)

            case 'json':
                data = pd.read_json(path)

            case 'txt':
                data = pd.read_table(path, sep=';')

            case 'dat':
                with open(path, "rb") as file:
                    binary_data = file.read()
                float_data = np.frombuffer(binary_data, dtype=np.float32)

                data = pd.DataFrame({'x': np.arange(0, len(float_data)), 'y': float_data})
            
            case 'wav':
                with wave.open(path, 'rb') as wav_file:
                    sample_width = wav_file.getsampwidth()
                    n_channels = wav_file.getnchannels()
                    framerate = wav_file.getframerate()
                    n_frames = wav_file.getnframes()
                    frames = wav_file.readframes(n_frames)
                    audio_data = np.frombuffer(frames, dtype=np.int16)

                time = np.arange(0, n_frames) / framerate
                data = pd.DataFrame({'Time': time, 'Amplitude': audio_data})
            case _:
                return FunctionResult(error_message=f"Формат {extension} не поддерживается")
                
    except Exception as e:
        return FunctionResult(error_message=f"При чтении файла '{name}' произошла ошибка: {str(e)}")

    if data.empty:
        return FunctionResult(error_message=f"Файл '{name}' пуст")
    
    if len(data.columns) > 2:
        return FunctionResult(error_message=f"Файл '{name}' содержит больше двух столбцов")
    
    return FunctionResult(main_data=data)
