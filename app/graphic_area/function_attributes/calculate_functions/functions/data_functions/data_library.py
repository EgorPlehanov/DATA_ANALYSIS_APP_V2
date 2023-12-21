from ....function_typing import FunctionResult, File
from .download import read_data


def data_library(
    library_data: File    # файл
) -> FunctionResult:
    '''
    Обрабатывает данные из файлов
    '''
    if library_data is None:
        return FunctionResult()

    path = library_data.path
    return read_data(path)
