from random import random



def random_value(min_value: int | float, max_value: int | float, decimal_accuracy: int) -> int | float:
    """
    Возвращает случайное значение в заданном диапазоне
    """
    rand_value = min_value + (max_value - min_value) * random()
    if decimal_accuracy != -1:
        rand_value = int(rand_value) if decimal_accuracy == 0 else round(float(rand_value), decimal_accuracy)
    return {
        "value": rand_value   
    }