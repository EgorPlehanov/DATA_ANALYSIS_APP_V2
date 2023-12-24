from pandas import DataFrame, isna
from typing import List
from flet import (
    Row, colors, Container, ScrollMode, border, DataTable,
    DataColumn, Text, DataCell, DataRow, BorderSide
)


class ResultTableHorizontal(Row):
    '''Горизонтальная таблица для отображения набора данных'''
    def __init__(self, data: DataFrame):
        super().__init__()
        self.data = data
        self.transposed_data = data.transpose()

        self.controls = self.create_controls()


    def create_controls(self) -> List[Container]:
        '''Создает таблицу'''
        return [Container(
            expand = True,
            content = Row(
                spacing = 0,
                controls = [
                    self._create_header_table(),
                    Row(
                        expand = True,
                        tight = True,
                        scroll = ScrollMode.ADAPTIVE,
                        controls = [self._create_data_table()]
                    )
                ]
            ),
            border = border.all(1, colors.with_opacity(0.5, colors.ON_SURFACE)),
            border_radius = 10,
        )]


    def _create_header_table(self) -> DataTable:
        '''Coздает таблицу с заголовками (первый столбец)'''
        return DataTable(
            columns = [DataColumn(Text(""))],
            rows=[
                DataRow([DataCell(Text(str(idx)))])
                for idx in self.transposed_data.index
            ],
            border = border.only(right=BorderSide(1, color=colors.with_opacity(0.2, colors.ON_SURFACE))),
            horizontal_margin = 10,
            heading_row_height = 40,
            data_row_max_height = 40,
        )


    def _create_data_table(self) -> Container:
        '''Создает таблицу с данными (остальные столбцы)'''
        return DataTable(
            columns = [
                DataColumn(Text(str(col)), numeric=True)
                for col in self.transposed_data.columns
            ],
            rows = [
                DataRow(
                    cells = [
                        DataCell(Text(str(value)) if not isna(value) else '')
                        for value in self.transposed_data.loc[idx]
                    ]
                )
                for idx in self.transposed_data.index
            ],
            column_spacing = 15,
            heading_row_height = 40,
            data_row_max_height = 40,
            vertical_lines = BorderSide(1, color=colors.with_opacity(0.05, colors.ON_SURFACE))
        )
    

    # def create_controls(self) -> List[Markdown]:
    #     '''Создает таблицу'''
    #     # ПОПЫТКА ОТОБРАЖАТЬ ТАБЛИЦЫ, ТАКОЙ СПОСОБ БЫ УСКОРИЛ РАБОТУ, ОДНАКО СЕЙЧАС ОТОБРАЖАЕТСЯ НЕКОРРЕКТНО
    #     return [Markdown(    
    #         expand = True,
    #         value = self.transposed_data.to_markdown(),
    #         extension_set = MarkdownExtensionSet.GITHUB_WEB,
    #     )]
    

    def update_values(self) -> None:
        '''Обновляет таблицу'''
        # TODO: добавить логику обновления
        pass
