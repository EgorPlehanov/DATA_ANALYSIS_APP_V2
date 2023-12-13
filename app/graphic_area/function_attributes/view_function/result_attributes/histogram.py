from pandas import DataFrame
from typing import List, Tuple
from flet import (
    Row, colors, BarChartGroup, BarChartRod, BarChart,
    ChartAxis, Text, border, ChartGridLines
)


class ResultHistogram(Row):
    def __init__(self,
        data: DataFrame,
        title: str,
        color: str = colors.BLACK,
        column_names: List[str] = None
    ):
        super().__init__()
        self.data = data
        self.title = title
        self.color = color
        self.column_names = column_names

        self.controls = self.create_controls()


    def create_controls(self) -> List[BarChart]:
        x_title, y_title = self._get_column_names()
        return [BarChart(
            bar_groups = self._create_bar_groups(),
            left_axis = ChartAxis(
                title = Text(y_title),
                title_size = 20,
                labels_size = 50,
            ),
            bottom_axis = ChartAxis(
                title = Text(x_title),
                title_size = 20,
                labels_size = 30
            ),
            top_axis = ChartAxis(
                title = Text(self.title, size=20),
                title_size = 30,
                show_labels = False,
            ),
            border = border.all(1, colors.with_opacity(0.5, colors.ON_SURFACE)),
            horizontal_grid_lines = ChartGridLines(
                width=1, color=colors.with_opacity(0.2, colors.ON_SURFACE),
            ),
            vertical_grid_lines = ChartGridLines(
                width=1, color=colors.with_opacity(0.2, colors.ON_SURFACE),
            ),
            tooltip_bgcolor = colors.with_opacity(0.8, colors.BLACK38),
            interactive = True,
            expand = True,
        )]
    

    def _get_column_names(self) -> Tuple[str, str]:
        '''Возвращает названия столбцов'''
        column_names = self.column_names
        if column_names is None:
            column_names = self.data.columns.tolist()
        return column_names[0], column_names[1]
    

    def _create_bar_groups(self):
        '''Создает группы баров'''
        return [
            BarChartGroup(
                x = round(x_value),
                bar_rods = [
                    BarChartRod(
                        to_y = y_value,
                        color = self.color,
                    )
                ]
            )
            for x_value, y_value in zip(self.data.iloc[:, 0], self.data.iloc[:, 1])
        ]
    

    def update_values(self) -> None:
        '''Обновляет гистограмму'''
        # TODO: добавить логику обновления
        pass
