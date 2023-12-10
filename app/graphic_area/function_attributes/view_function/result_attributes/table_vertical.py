from pandas import DataFrame
from typing import List
from flet import (
    Row, colors, border, DataTable, DataColumn,
    Text, DataCell, DataRow, BorderSide
)


class ResultTableVertical(Row):
    def __init__(self, data: DataFrame):
        super().__init__()
        self.data = data

        self.controls = self.create_controls()


    def create_controls(self) -> List[DataTable]:
        columns = [
            DataColumn(Text(col))
            for col in self.data.columns
        ]
        rows = [
            DataRow([
                DataCell(Text(str(value)))
                for value in row
            ])
            for _, row in self.data.iterrows()
        ]
        return [DataTable(
            columns = columns,
            rows = rows,
            border = border.all(1, colors.with_opacity(0.5, colors.ON_SURFACE)),
            vertical_lines = BorderSide(1, color=colors.with_opacity(0.05, colors.ON_SURFACE)),
            border_radius = 10,
            expand = True,
        )]
