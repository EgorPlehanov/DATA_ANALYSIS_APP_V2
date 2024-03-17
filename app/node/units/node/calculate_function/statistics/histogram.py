from ....parameters.parameter_typing import File
from ..calculate_function_typing import *
from ..input.read import read_file
import cv2
import matplotlib.pyplot as plt
import plotly.graph_objects as go



def create_single_image_histogram_plot(image):
    """
    Создает датафрейм для построения гистограммы нескольких изображений
    """
    if image is None:
        return {"histogram_dataframe": None}
    if isinstance(image, File):
        image = read_file(image.path)

    fig, ax = plt.subplots()
    if len(image.shape) == 3:  # Check for color image
        if image.dtype == 'uint8':  # Check for image format
            color = ('b', 'g', 'r')
            for k, col in enumerate(color):
                hist_values = cv2.calcHist([image], [k], None, [256], [0, 256])
                ax.plot(hist_values, color=col, label=col)
    else:  # Grayscale image
        if image.dtype == 'uint8':  # Check for image format
            hist_values = cv2.calcHist([image], [0], None, [256], [0, 256])
            ax.plot(hist_values, label='grayscale')

    ax.set_xlim([0, 256])
    ax.legend()

    return {
        "histogram_fig": NodeResult(fig, ResultType.MATPLOTLIB_FIG),
    }