from .param_editor_interface import ParamEditorInterface
from ...function_typing import ResultData

from typing import List
from dataclasses import dataclass, field
from flet import Container, Dropdown, dropdown, Ref


@dataclass
class DFDOptionItem:
    function_name: str      = 'Не выбраны'
    value: List[ResultData] = field(default_factory=list)

    def __str__(self) -> str:
        return f"{self.function_name}: {self.value}"


class DropdownFunctionDataEditor(ParamEditorInterface, Container):
    def __init__(self,
        param_name: str                 = '',
        title: str                      = 'Выбор набора данных',
        options: DFDOptionItem          = DFDOptionItem(),
        default_value: DFDOptionItem    = DFDOptionItem(),
    ):
        self._type = 'dropdown_function_data'
        self._param_name = param_name
        self.title = title
        self.options = options
        self.default_value = default_value
        self.default_value_to_print = str(default_value)

        super().__init__()
        self.set_styles()
        self.content = self.create_content()


    def create_control(self) -> Dropdown:
        ref_dropdown_function_data = Ref[Dropdown]()
        return None
        # self.list_ref_params_to_update.append({
        #     'ref': ref_dropdown_function_data,
        #     'param_type': 'dropdown_function_data',
        #     'param_name': param_name,
        #     'param': param,
        # })

        # function_card_list = []
        # if self.function.type in ['edit', 'analytic']:
        #     function_card_list.extend(self.graphic_area.list_functions_data)
        # if self.function.type == 'analytic':
        #     function_card_list.extend(self.graphic_area.list_functions_edit)

        # options = param.get('options', {'Не выбраны': {'function_name': 'Не выбраны', 'value': []}}).copy()
        # options.update({
        #     function_card.function_name_formatted: {
        #         'function_name': function_card.function_name_formatted,
        #         'value': function_card
        #     }
        #     for function_card in function_card_list
        # })
        
        # dropdown_value = 'Не выбраны'
        # value_to_print = 'Не выбраны []'
        # # Проверка не удаленно ли текущее значение из списка
        # if current_value in options.values():
        #     dropdown_value = current_value.get('function_name')
        #     function_card = current_value.get('value')

        #     if isinstance(function_card, FunctionCard):
        #         function_card = function_card.function.result
        #     value_to_print = f"{dropdown_value}: {[elem.get('type') for elem in function_card]}"
        # self.function.set_parameter_value(param_name, options[dropdown_value], value_to_print)
        
        # # editor_dropdown_function_data = Dropdown(
        # #     ref=ref_dropdown_function_data,
        # #     dense=True,
        # #     label=param.get('title'),
        # #     on_change=self._on_change_dropdown_function_value,
        # # )
        # # if update_control is not None:
        # #     editor_dropdown_function_data = update_control

        # # editor_dropdown_function_data.options = [
        # #     dropdown.Option(key=key, text=key) for key in options.keys()
        # # ],
        # # editor_dropdown_function_data.value = dropdown_value
        # # editor_dropdown_function_data.data = {
        # #     'param_name': param_name, 'data': options
        # # }

        # editor_dropdown_function_data = Dropdown(
        #     ref=ref_dropdown_function_data,
        #     dense=True,
        #     label=param.get('title'),
        #     options=[
        #         dropdown.Option(key=key, text=key)
        #         for key in options.keys()
        #     ],
        #     value=dropdown_value,
        #     data={
        #         'param_name': param_name,
        #         'data': options
        #     },
        #     on_change=self._on_change_dropdown_function_value,
        # )
        # return editor_dropdown_function_data
    

    def on_change(self, e) -> None:
        '''
        Обновляет значение параметра в экземпляре класса Function и карточке функции
        '''
        dropdown_value = e.control.value
        param_value = e.control.data.get('data').get(dropdown_value)

        # function_card = param_value.get('value')
        # if isinstance(function_card, FunctionCard):
        #     function_card.list_dependent_functions.append(self)
        #     self.provider_function = function_card

        #     function_card = function_card.function.result

        # self.function.set_parameter_value(
        #     param_name, param_value, f"{param_value.get('function_name')}: {[elem.get('type') for elem in function_card]}"
        # )
        # self.update_function_card()
    