import re
import ast
import sympy as sp


def validate_textfield_value(self, e) -> None:
        '''Проверка валидности значения текстового поля'''
        text_type = e.control.data.get('value_type')
        text_field_value = e.control.value
        
        error_message = ''
        if text_field_value != '':
            match text_type:
                case 'function':
                    if text_field_value:
                        if not re.match(f"^[a-z0-9+\-*/()., ]*$", text_field_value):
                            error_message = f"Ошибка: Недопустимые символы в функции"
                        else:
                            try:
                                ast.parse(text_field_value)
                                sp.sympify(text_field_value, evaluate=False)
                                sp.parse_expr(text_field_value)
                            except Exception as exeption:
                                error_message = f"Ошибка: {exeption}"
                case 'int_number':
                    if not text_field_value.isnumeric():
                        error_message = f"Не целое число"
                case 'number':
                    try:
                        float(text_field_value)
                    except ValueError:
                        error_message = f"Неверный формат числа"

            min_value = e.control.data.get('min')
            max_value = e.control.data.get('max')
            if (
                error_message == ''
                and min_value and max_value 
                and text_type in ('int_number', 'number')
                and (float(text_field_value) < min_value or float(text_field_value) > max_value)
            ):
                error_message = f"За границами [{min_value}, {max_value}]"

        e.control.error_text = error_message
        e.control.update()