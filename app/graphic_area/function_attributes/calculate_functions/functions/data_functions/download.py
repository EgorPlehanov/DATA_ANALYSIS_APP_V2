from ....function_typing import FunctionResult, File

from typing import List
import numpy as np
import pandas as pd
import csv
import wave


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
    with wave.open(path, 'rb') as wav_file:
        sample_width = wav_file.getsampwidth()
        n_channels = wav_file.getnchannels()
        framerate = wav_file.getframerate()
        n_frames = wav_file.getnframes()
        frames = wav_file.readframes(n_frames)
        audio_data = np.frombuffer(frames, dtype=np.int16)

    time = np.arange(0, n_frames) / framerate
    return pd.DataFrame({'Time': time, 'Amplitude': audio_data})


def read_data(path: str) -> FunctionResult:
    '''Чтение данных из файлов'''
    read_data = {
        'csv': read_csv,
        'xls': lambda path: pd.read_excel(path),
        'xlsx': lambda path: pd.read_excel(path),
        'xlsm': lambda path: pd.read_excel(path),
        'xlsb': lambda path: pd.read_excel(path),
        'odf': lambda path: pd.read_excel(path),
        'ods': lambda path: pd.read_excel(path),
        'odt': lambda path: pd.read_excel(path),
        'json': lambda path: pd.read_json(path),
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
    
    if data.empty:
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
