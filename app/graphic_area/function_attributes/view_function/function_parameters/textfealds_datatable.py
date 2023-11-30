from .parameter_editor_interface import ParamEditorInterface
from function_typing import ValueType

from dataclasses import dataclass
from typing import Dict, Any
from flet import (
    Container, Column, DataTable, DataColumn, DataCell, IconButton, Ref,
    TextField, Text, DataRow, TextAlign, colors, KeyboardType, Markdown,
    border, BorderSide, animation, AnimationCurve, Row, icons, MainAxisAlignment
)


@dataclass
class TFDTColumn:
    name: str             = ''
    tooltip: str          = ''
    value_type: ValueType = ValueType.FLOAT

@dataclass
class TFDTItem:
    values: Dict[str, str | int | float] = None

@dataclass
class TFDTConfig:
    name: str           = ''
    title: str          = ''
    columns: Dict[str, TFDTColumn]      = {}
    default_value: Dict[int, TFDTItem]  = {}


class TextFealdsDataTableEditor(ParamEditorInterface, Container):
    def __init__(self, config: TFDTConfig = TFDTConfig()):
        self._type = 'textfields_datatable'
        self._name = config.name
        self.title = config.title
        self.columns = config.columns
        self.default_value = config.default_value

        super().__init__()
        self._set_styles()
        self.content = self._create_content()


    def _create_content(self) -> Column:
        ref_data_table = Ref[DataTable]()
        ref_delete_button = Ref[IconButton]()

        column_names = self.columns
        columns = [
            DataColumn(
                label = Text(values.get('name', key)),
                tooltip = values.get('tooltip')
            )
            for key, values in column_names.items()
        ]
        rows = [
            DataRow(
                cells = [
                    DataCell(TextField(
                        value = str(value),
                        expand = True,
                        border_radius = 0,
                        border_color = colors.with_opacity(0.0, colors.PRIMARY),
                        text_align = TextAlign.CENTER,
                        keyboard_type = KeyboardType.NUMBER,
                        focused_color = colors.BLUE,
                        data = {
                            'text_type': 'number',
                            'ref_data_table': ref_data_table,
                            'column_name': column_name
                        },
                        on_change = None, #self._is_text_field_value_valid,
                        on_blur = self.on_change,
                        on_submit = self.on_change,
                    ))
                    for column_name, value in row_values.items()
                ],
                data = {
                    'ref_data_table': ref_data_table,
                    'ref_delete_button': ref_delete_button,
                },
                on_select_changed = None, #self.on_textfields_datatable_select_changed
            )
            for row_idx, row_values in self.default_value.items()
        ]

        editor_textfields_datatable = Column(
            controls = [
                Markdown(self.title),
                DataTable(
                    columns = columns,
                    rows = rows,
                    ref = ref_data_table,
                    width = 310,
                    column_spacing = 0,
                    horizontal_margin = 0,
                    border_radius = 10,
                    border = border.all(1, colors.with_opacity(0.5, colors.ON_SURFACE)),
                    vertical_lines = BorderSide(1, colors.with_opacity(0.3, colors.ON_SURFACE)),
                    horizontal_lines = BorderSide(1, colors.with_opacity(0.3, colors.ON_SURFACE)),
                    show_checkbox_column = True,
                    checkbox_horizontal_margin = 0,
                    animate_size = animation.Animation(200, AnimationCurve.FAST_OUT_SLOWIN),
                ),
                Row(
                    controls = [
                        IconButton(
                            icon = icons.PLAYLIST_ADD,
                            tooltip = "Добавить строку",
                            data = {
                                'ref_data_table': ref_data_table,
                                "ref_delete_button": ref_delete_button,
                                'column_names': column_names.keys(),
                            },
                            on_click = None, #self.add_textfields_datatable_row,
                        ),
                        IconButton(
                            icon = icons.DELETE_SWEEP,
                            tooltip = "Удалить выбранные строки",
                            ref = ref_delete_button,
                            disabled = True,
                            data = {
                                'ref_data_table': ref_data_table,
                            },
                            on_click = None, #self.delete_textfields_datatable_rows,
                        )
                    ],
                    alignment = MainAxisAlignment.SPACE_BETWEEN,
                )
            ],
        )
        return editor_textfields_datatable
    
    
    def on_change(self, e) -> None:
        pass
    