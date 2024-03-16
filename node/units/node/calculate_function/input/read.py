from ....parameters.parameter_typing import File
from ..calculate_function_typing import *

from PIL import Image
import cv2
import numpy as np



def read_jpg_image(file_path):
    """
    Чтение jpg изображения
    """
    return cv2.imread(file_path)



def read_file(file: File | str = None):
    '''
    Чтение данных из файлов
    '''
    read_data = {
        'jpg': read_jpg_image,
        'jpg': read_jpg_image, 
        "jpeg": read_jpg_image,
        "png": read_jpg_image,
        "bmp": read_jpg_image,
        "gif": read_jpg_image,
    }

    
    if not isinstance(file, File):
        file = File(path=file)

    try:
        if file.extension in read_data:
            return read_data[file.extension](file.path)
        else: 
            raise ValueError(f"Формат {file.extension} не поддерживается")
    except Exception as e:
        raise ValueError(f"При чтении файла '{file.formatted_name}' произошла ошибка: {str(e)}")
    


def open_image_file(image_file: File) -> Image.Image:
    """
    Открывает изображение из файла
    """
    if image_file is None:
        return {'image': None}
    if isinstance(image_file, File):
        image_file = read_file(file=image_file)
    return {
        'image': NodeResult(image_file, ResultType.IMAGE_CV2),
    }