from ....function_typing import FunctionResult, File

from typing import List
import numpy as np
import pandas as pd
import csv
import soundfile as sf



def read_csv(path: str) -> pd.DataFrame:
    '''Возвращает DataFrame из CSV-файла'''
    with open(path, 'r', newline='') as csvfile:
        sample_data = csvfile.read(1024)
        sniffer = csv.Sniffer()
        delimiter = sniffer.sniff(sample_data).delimiter
    return pd.read_csv(path, delimiter=delimiter)


def read_dat(path: str) -> pd.DataFrame:
    '''Возвращает DataFrame из DAT-файла'''
    with open(path, "rb") as file:
        binary_data = file.read()
    float_data = np.frombuffer(binary_data, dtype=np.float32)
    return pd.DataFrame({'x': np.arange(0, len(float_data)), 'y': float_data})


def read_wav(path: str) -> pd.DataFrame:
    '''Возвращает DataFrame из WAV-файла'''
    audio_data, sample_rate = sf.read(path)
    
    if len(audio_data.shape) > 1:
        audio_data = audio_data[:, 0]

    time_array = np.arange(len(audio_data)) / sample_rate
    return pd.DataFrame({
        'time': time_array,
        'amp': audio_data
    })



def read_data(path: str) -> FunctionResult:
    '''Чтение данных из файлов'''
    read_data = {
        'csv': read_csv,
        'xls': pd.read_excel,
        'xlsx': pd.read_excel,
        'xlsm': pd.read_excel,
        'xlsb': pd.read_excel,
        'odf': pd.read_excel,
        'ods': pd.read_excel,
        'odt': pd.read_excel,
        'json': pd.read_json,
        'txt': lambda path: pd.read_table(path, sep=';'),
        'dat': read_dat,
        'wav': read_wav,
    }

    name = path.split('\\')[-1]
    extension = path.split('.')[-1].lower()

    try:
        if extension in read_data:
            data: pd.DataFrame = read_data[extension](path)
        else: 
            raise ValueError(f"Формат {extension} не поддерживается")
    except Exception as e:
        raise ValueError(f"При чтении файла '{name}' произошла ошибка: {str(e)}")
    
    if data is None or data.empty:
        raise ValueError(f"Файл '{name}' пуст")
    if len(data.columns) != 2:
        raise ValueError(f"Файл '{name}' должен содержать 2 столбца, а не {len(data.columns)}")
    
    return FunctionResult(main_data=data)


def data_download(
    input_data: List[File]    # Список файлов
) -> FunctionResult:
    '''
    Обрабатывает данные из файлов
    '''
    if len(input_data) == 0:
        return FunctionResult()
    
    # result_list = []
    for file in input_data:
        return read_data(file.path)
