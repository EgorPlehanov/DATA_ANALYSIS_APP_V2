from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ....view_function.function_parameters.data_library import DLFile

from ....function_typing import FunctionResult
from .download import read_data


def data_library(
    library_data: 'DLFile'    # файл
) -> FunctionResult:
    '''
    Обрабатывает данные из файлов
    '''
    if library_data is None:
        return FunctionResult()

    path = library_data.path
    return read_data(path)
