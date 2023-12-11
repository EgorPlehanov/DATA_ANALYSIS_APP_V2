from .parameter_editor_interface import ParamEditorInterface
from ...function_typing import ResultData, ParameterType

from typing import List, Any
from dataclasses import dataclass, field
from flet import Container, Dropdown, dropdown, Ref


@dataclass
class DDFDOptionItem:
    function_name: str  = 'Не задана'
    function: Any       = None

@dataclass
class DDFDConfig:
    name: str   = 'data'
    title: str  = 'Выбор набора данных'

    @property
    def type(self) -> ParameterType:
        return ParameterType.DROPDOWN_FUNCTION_DATA


class DropdownFunctionDataEditor(ParamEditorInterface, Container):
    def __init__(self, function, config: DDFDConfig = DDFDConfig()):
        self._type = ParameterType.DROPDOWN_FUNCTION_DATA
        self.function = function
        
        self._name = config.name
        self.title = config.title
        self.options = self._get_current_options()

        self.ref_dropdown_function_data = Ref[Dropdown]()

        super().__init__()
        self._set_styles()
        self.content = self._create_content()


    def _create_content(self) -> Dropdown:
        '''Создает виджет с выпадающим списком функций'''
        return Dropdown(
            ref = self.ref_dropdown_function_data,
            dense = True,
            label = self.title,
            options = self._get_options_formatted(),
            on_change = self._on_change
        )
    

    def _get_current_options(self) -> List[dropdown.Option]:
        '''Возвращает список конфигов функций для выпадающего списка'''
        return [
            DDFDOptionItem(function.formatted_name, function)
            for function in self.function._graphic_area.get_functions_list()
            if function != self.function
        ]
    

    def _get_options_formatted(self) -> List[dropdown.Option]:
        '''Возвращает список функций для выпадающего списка'''
        return [
            dropdown.Option(key=option.function_name, text=option.function_name)
            for option in self.options
        ]


    def _on_change(self, e) -> None:
        '''Обновляет значение параметра в экземпляре класса Function и карточке функции'''
        key = e.control.value
        new_function = next((option.function for option in self.options if option.function_name == key), None)
        if not self._update_dependencies(new_function):
            return
        
        self.function.calculate.set_parameter_value(self.name, new_function)
        self.update()


    def _update_dependencies(self, new_function) -> bool:
        '''Устанавливает зависимость текущей функции и выбранной в выпадающем списке'''
        last_function = self.function.calculate.get_current_parameter_value(self.name)
        if new_function == last_function:
            return False
        if last_function is not None:
            last_function.list_dependent_out.remove(self.function)
            self.function.list_dependent_in.remove(last_function)
        if new_function is not None:
            new_function.list_dependent_out.append(self.function)
            self.function.list_dependent_in.append(new_function)
        return True

    
    def update_values(self) -> None:
        '''Обновляет значения выпадающего списка'''
        self.options = self._get_current_options()
        self.ref_dropdown_function_data.current.options = self._get_options_formatted()

        current_value = self.ref_dropdown_function_data.current.value
        if (
            current_value is not None
            and not any(current_value == option.function_name for option in self.options)
        ):
            self.function.calculate.set_parameter_value(self._name, None)
        self.update()
    