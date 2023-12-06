from .parameter_editor_interface import ParamEditorInterface
from ...function_typing import ValueType, ParameterType
from .parameters_utils import validate_textfield_value

from dataclasses import dataclass, field
from typing import Dict, List
from flet import (
    Container, Column, DataTable, DataColumn, DataCell, IconButton, Ref,
    TextField, Text, DataRow, TextAlign, colors, KeyboardType, Markdown,
    border, BorderSide, animation, AnimationCurve, Row, icons, MainAxisAlignment,
    ControlEvent
)


@dataclass
class TFDTItem:
    column_name: str         = None
    row_index: int           = None
    value: str | int | float = ''

@dataclass
class TFDTColumn:
    name: str             = ''
    tooltip: str          = None
    value_type: ValueType = ValueType.FLOAT

@dataclass
class TFDTConfig:
    name: str                     = ''
    title: str                    = ''
    columns: Dict[str, TFDTColumn] | List[TFDTColumn] = field(default_factory=dict)
    default_value: List[TFDTItem] = field(default_factory=list)

    @property
    def type(self) -> ParameterType:
        return ParameterType.TEXTFIELDS_DATATABLE
    
    def __post_init__(self):
        if isinstance(self.columns, list):
            self.columns = {column.name: column for column in self.columns}
        for item in self.default_value:
            if item.column_name not in self.columns.keys():
                raise ValueError(f"Неизвестный столбец: {item.column_name}, были заданы столбцы: {TFDTConfig.columns.keys()}")


class TextFieldsDataTableEditor(ParamEditorInterface, Container):
    def __init__(self, function, config: TFDTConfig = TFDTConfig()):
        self.function = function
        
        self._type = ParameterType.TEXTFIELDS_DATATABLE
        self._name = config.name
        self.title = config.title
        self.columns = config.columns
        self.default_value = config.default_value

        self.ref_data_table = Ref[DataTable]()
        self.ref_delete_button = Ref[IconButton]()

        super().__init__()
        self._set_styles()
        self.content = self._create_content()


    def _create_content(self) -> Column:
        return Column(
            controls = [
                Markdown(self.title),
                self._create_datatable(),
                self._create_datatable_edit_button()
            ],
        )
    

    def _create_datatable(self) -> DataTable:
        row_count = max([item.row_index for item in self.default_value]) + 1
        return DataTable(
            columns                    = self._create_datatable_columns(),
            rows                       = self._create_datatable_rows(row_count),
            ref                        = self.ref_data_table,
            width                      = 310,
            column_spacing             = 0,
            horizontal_margin          = 0,
            border_radius              = 10,
            border                     = border.all(1, colors.with_opacity(0.5, colors.ON_SURFACE)),
            vertical_lines             = BorderSide(1, colors.with_opacity(0.3, colors.ON_SURFACE)),
            horizontal_lines           = BorderSide(1, colors.with_opacity(0.3, colors.ON_SURFACE)),
            animate_size               = animation.Animation(200, AnimationCurve.FAST_OUT_SLOWIN),
            show_checkbox_column       = True,
            checkbox_horizontal_margin = 0,
        )
    

    def _create_datatable_columns(self) -> List[DataColumn]:
        '''Создает колонки таблицы'''
        return [
            DataColumn(
                label = Text(column.name),
                tooltip = column.tooltip,
            )
            for column in self.columns.values()
        ]
    

    def _create_datatable_rows(self, row_count: int, current_row_idx: int = 0, is_default: bool = True) -> List[DataRow]:
        '''Создает строки таблицы'''
        return [
            DataRow(
                cells = [
                    self._create_datatable_cell(column_name, row_idx, is_default)
                    for column_name in self.columns.keys()
                ],
                on_select_changed = self.on_datatable_select_changed
            )
            for row_idx in range(current_row_idx, current_row_idx + row_count)
        ]
    

    def _create_datatable_cell(self, column_name: str, row_idx, is_default: bool) -> DataCell:
        '''Создает ячейку таблицы'''
        cell_config = self._get_item_config_by_column_name_row_index(column_name, row_idx, is_default)
        return DataCell(TextField(
            value = str(cell_config.value),
            expand = True,
            border_radius = 0,
            border_color = colors.with_opacity(0.0, colors.PRIMARY),
            text_align = TextAlign.CENTER,
            keyboard_type = KeyboardType.NUMBER,
            focused_color = colors.BLUE,
            data = {
                'value_type': self.columns[cell_config.column_name].value_type,
                'column_name': cell_config.column_name,
            },
            on_change = validate_textfield_value,
            on_blur = self._on_change,
            on_submit = self._on_change,
        ))
    

    def _get_item_config_by_column_name_row_index(self, column_name: str, row_idx: int, is_default: bool) -> TFDTItem:
        '''Возвращает конфигурацию ячейки по имени столбца и индексу строки, если такой нет возвращает дефолтную'''
        if is_default:
            return next((
                    item for item in self.default_value
                    if item.column_name == column_name and item.row_index == row_idx
                ),
                TFDTItem(column_name, row_idx)
            )
        return TFDTItem(column_name, row_idx)
    

    def _create_datatable_edit_button(self) -> Row:
        '''Создает кнопку добавления и удаления строк в таблице'''
        return Row(
            controls = [
                IconButton(
                    icon = icons.PLAYLIST_ADD,
                    tooltip = "Добавить строку",
                    on_click = self.add_datatable_row,
                ),
                IconButton(
                    icon = icons.DELETE_SWEEP,
                    tooltip = "Удалить выбранные строки",
                    ref = self.ref_delete_button,
                    disabled = True,
                    on_click = self.delete_datatable_rows,
                )
            ],
            alignment = MainAxisAlignment.SPACE_BETWEEN,
        )
    

    def on_datatable_select_changed(self, e) -> None:
        '''Изменяет выделение нажатой строки в таблице'''
        e.control.selected = not e.control.selected
        e.control.update()

        table = self.ref_data_table.current
        button = self.ref_delete_button.current
        
        select_rows_count = len([row for row in table.rows if row.selected])
        button.disabled = select_rows_count == 0
        button.update()


    def add_datatable_row(self, e) -> None:
        '''Добавляет строку в таблицу'''
        table = self.ref_data_table.current
        table.rows.extend(self._create_datatable_rows(
            row_count = 1,
            current_row_idx = len(table.rows),
            is_default = False
        ))
        table.update()


    def delete_datatable_rows(self, e: ControlEvent) -> None:
        '''Удаляет выбранные строки в таблице'''
        table = self.ref_data_table.current
        table.rows = [row for row in table.rows if not row.selected]
        table.update()

        e.control.disabled = True
        e.control.update()

        self._on_change(e)


    def _on_change(self, e) -> None:
        '''Обновляет значение параметра при обновлении значения ячейки таблицы'''
        rows = self.ref_data_table.current.rows
        values = {
            idx: {
                cell.content.data.get('column_name'): float(cell.content.value)
                for cell in row.cells
            }
            for idx, row in enumerate(rows)
            if (
                all(cell.content.value != '' for cell in row.cells)         # Только строки где все ячейки заполнены
                and not any(cell.content.error_text for cell in row.cells)  # Все ячейки строки заполнены без ошибок
            )
        }
        self.function.calculate.set_parameter_value(self._name, values)
        self.update()
    