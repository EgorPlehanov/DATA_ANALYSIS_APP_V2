from ....function_typing import FunctionResult

import numpy as np
import pandas as pd
import csv


def data_download(
    input_data: list    # Список файлов
) -> FunctionResult:
    '''
    Обрабатывает данные из файлов
    '''
    if len(input_data) == 0:
        return FunctionResult()
    
    # result_list = []
    for file in input_data:
        file_name = file.name
        file_path = file.path

        # Определение формата файла на основе расширения
        file_extension = file_path.split('.')[-1].lower()
        
        try:
            match file_extension:
                case 'csv':
                    # Определение разделителя
                    with open(file_path, 'r', newline='') as csvfile:
                        sample_data = csvfile.read(1024)
                        sniffer = csv.Sniffer()
                        delimiter = sniffer.sniff(sample_data).delimiter
                    # Чтение CSV файла с указанием определенного разделителя
                    data = pd.read_csv(file_path, delimiter=delimiter)
                case 'xls' | 'xlsx' | 'xlsm' | 'xlsb' | 'odf' | 'ods' | 'odt':
                    data = pd.read_excel(file_path)

                case 'json':
                    data = pd.read_json(file_path)

                case 'txt':
                    data = pd.read_table(file_path, sep=';')

                case 'dat':
                    with open(file_path, "rb") as file:
                        binary_data = file.read()
                    float_data = np.frombuffer(binary_data, dtype=np.float32)

                    data = pd.DataFrame({'x': np.arange(0, len(float_data)), 'y': float_data})
                
                case _:
                    # result_list.append()
                    return FunctionResult(error_message=f"Формат {file_extension} не поддерживается")
                    continue
        except Exception as e:
            # result_list.append()
            return FunctionResult(error_message=f"При чтении файла '{file_name}' произошла ошибка: {str(e)}")
            continue

        if data.empty:
            # result_list.append()
            return FunctionResult(error_message=f"Файл '{file_name}' пуст")
            continue
        
        if len(data.columns) > 2:
            # result_list.append()
            return FunctionResult(error_message=f"Файл '{file_name}' содержит больше двух столбцов")
            continue
        
        return FunctionResult(main_data=data)

    # return FunctionResult(
    #     main_data = result_list[0].main_data if len(result_list) > 0 else None,
    #     extra_data = result_list[1:] if len(result_list) > 1 else None,
    #     error_message = '; '.join([r.error_message for r in result_list if r.error_message])
    # )
