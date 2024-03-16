from ....parameters.parameter_typing import File
from ..input.read import read_file
from ..calculate_function_typing import *
import cv2
import numpy as np



def apply_grayscale_scaling(image, scale_size: int = 255):
    """
    Применяет шкалирование серого цвета к входному изображению и возвращает результат
    """
    if image is None:
        return {"grayscale_image": None}
    if isinstance(image, File):
        image = read_file(image.path)

    min_val, max_val = np.min(image), np.max(image)
    scaled_image = ((image - min_val) / (max_val - min_val)) * scale_size
    return {
        "grayscale_image": NodeResult(scaled_image.astype(np.uint8), ResultType.IMAGE_CV2)
    }



def negative_transformation(image):
    """
    Применяет негативное градационное преобразование к изображению.
    """
    if image is None:
        return {"negative_image": None}
    if isinstance(image, File):
        image = read_file(image.path)

    L = np.iinfo(image.dtype).max
    negative_image = L - 1 - image
    return {
        "negative_image": NodeResult(negative_image, ResultType.IMAGE_CV2)
    }



def gamma_correction(image, gamma: float = 1.0, constant: float = 1.0):
    """
    Применяет гамма-преобразование к изображению.
    """
    if image is None:
        return {"gamma_image": None}
    if isinstance(image, File):
        image = read_file(image.path)

    gamma_image = constant * np.power(image, gamma)
    return {
        "gamma_image": NodeResult(gamma_image, ResultType.IMAGE_CV2)
    }



def logarithmic_transformation(image, constant=1):
    """
    Применяет логарифмическое градационное преобразование к изображению.
    """
    if image is None:
        return {"logarithmic_image": None}
    if isinstance(image, File):
        image = read_file(image.path)

    logarithmic_image = np.uint8(constant * np.log1p(image + 1))
    return {
        "logarithmic_image": NodeResult(logarithmic_image, ResultType.IMAGE_CV2)
    }
