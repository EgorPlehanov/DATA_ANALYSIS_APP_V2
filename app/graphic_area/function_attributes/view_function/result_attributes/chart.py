from pandas import DataFrame
from typing import List, Tuple
from flet import (
    Row, LineChart, ChartAxis, Text, border, colors, ChartGridLines,
    LineChartData, LineChartDataPoint, ChartPointLine,
)


class ResultChart(Row):
    def __init__(self,
        data: DataFrame,
        title: str,
        color: str = colors.LIGHT_GREEN,
        column_names: List[str] = None,
        graphic_curved: bool = False,
        max_points_count: int = 1500
    ):
        super().__init__()
        self.data = data
        self.title = title
        self.color = color
        self.column_names = column_names
        self.graphic_curved = graphic_curved
        self.max_points_count = max_points_count

        self.controls = self.create_controls()


    def create_controls(self) -> List[LineChart]:
        '''Создает график'''
        x_title, y_title = self._get_column_names()
        return [LineChart(
            data_series = self._create_data_series(),
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
            expand = True,
        )]
    

    def _get_column_names(self) -> Tuple[str, str]:
        '''Возвращает названия столбцов'''
        column_names = self.column_names
        if column_names is None:
            column_names = self.data.columns.tolist()
        return column_names[0], column_names[1]
    

    def _create_data_series(self) -> List[LineChartData]:
        '''Создает данные для графика'''
        if len(self.data) > self.max_points_count:
            step = round(len(self.data) / self.max_points_count)
            self.data = self.data.iloc[::int(step)]

        data_points = [
            LineChartDataPoint(x, y)
            for x, y in zip(self.data.iloc[:, 0], self.data.iloc[:, 1])
        ]

        return [LineChartData(
            data_points = data_points,
            stroke_width = 1,
            color = self.color,
            curved = self.graphic_curved,
            stroke_cap_round = True,
            selected_below_line = ChartPointLine(
                color = colors.ON_SURFACE,
                width = 1,
                dash_pattern = [10, 5],
            )
        )]
