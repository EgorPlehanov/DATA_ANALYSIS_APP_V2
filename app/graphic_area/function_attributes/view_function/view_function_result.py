from flet import *
from flet import (Container, colors, padding, border, Column)


class FunctionResultView(Container):
    def __init__(self, function):
        super().__init__()
        self.function = function
        self.key = self.function.id

        self.content = self.create_content()
        self.border_radius = 10
        self.bgcolor = colors.BLACK26
        self.padding = padding.only(left=10, top=10, right=20, bottom=10)
        self.on_click = self.function._on_click


    def change_selection(self):
        '''Изменяет выделение результата'''
        self.border = border.all(color=colors.BLUE) if self.function.selected else None


    def create_content(self) -> Column:
        return None
        result_data = self.function.get_result()
        result_view = None

        if not result_data:
            result_view = Row(
                alignment=MainAxisAlignment.CENTER,
                controls=[
                    Text(value='Нет данных для построения графиков функции ' + self.function_name, weight=FontWeight.BOLD, size=20),
                ]
            )
            return result_view
        
        colors_list = ['green', 'blue', 'red', 'yellow', 'purple',
                       'orange', 'pink', 'brown', 'cyan', 'magenta',
                       'teal', 'gray', 'black', 'lime', 'olive',
                       'violet']

        graphs_cnt = len(result_data)
        grid = []
        row = []
        for idx in range(1, graphs_cnt + 1):
            row.append(self._get_result_element_view(result_data[idx - 1], colors_list[(idx - 1) % len(colors_list)]))

            if (
                graphs_cnt <= 3 or len(row) == 3 or idx == graphs_cnt
                or (graphs_cnt % 3 == 1 and graphs_cnt - idx < 3 and len(row) == 2)
            ):
                grid.append(Row(controls=row, vertical_alignment=CrossAxisAlignment.START))
                row = []
        
        result_view = Column(
            controls=[
                Row(
                    alignment=MainAxisAlignment.CENTER,
                    controls=[
                        Text(value=f"График{'и' if graphs_cnt > 1 else ''} функции {self.function_name}", weight=FontWeight.BOLD, size=20),
                    ]
                ),
                Column(controls=grid),
            ]
        )
        return result_view













    def _get_result_element_view(self, dataframe, color='green') -> Container:
        if not dataframe:
            return None
        
        element_controls = []
        error_message = dataframe.get('error_message')
        if error_message:
            element_controls.append(
                self._get_result_error_message(error_message)
            )
            
        if dataframe.get('data') is not None:
            view_list = dataframe.get('view', [])
            if 'chart' in view_list:
                element_controls.append(self._get_function_result_graphic(dataframe, color=color))
            if 'histogram' in view_list:
                element_controls.append(self._get_function_result_histogram(dataframe, color=color))
            if 'table_data' in view_list:
                element_controls.append(self._get_datatable_data(dataframe))
            if 'table_statistics' in view_list:
                element_controls.append(self._get_datatable_statistics(dataframe))

        extra_data = dataframe.get('extra_data')
        if extra_data:
            for data in extra_data:
                extra_data_name = data.get('type')
                extra_data_control = self._get_result_element_view(data, color=color)
                extra_data_view = self._get_dropdown_conteiner_for_control(
                    control=extra_data_control,
                    button_name=f"Показать дополнительные данные:{(f' ***{extra_data_name.strip()}***')}",
                    is_open=False,
                )
                element_controls.append(extra_data_view)

        initial_data = dataframe.get('initial_data')
        if initial_data:
            for data in initial_data:
                initial_data_name = data.get('type')
                initial_data_control = self._get_result_element_view(data, color=color)
                initial_data_view = self._get_dropdown_conteiner_for_control(
                    control=initial_data_control,
                    button_name=f"Показать исходные данные:{(f' ***{initial_data_name.strip()}***')}",
                    is_open=False,
                )
                element_controls.append(initial_data_view)

        return Column(expand=True, controls=element_controls)
    

    def _get_result_error_message(self, error_message):
        error_message_view = Container(
            content=Row(
                controls=[
                    Icon(name=icons.ERROR_OUTLINE, color=colors.RED),
                    Row(
                        expand=True,
                        wrap=True,
                        controls=[
                            Text(
                                value=f'Ошибка: {error_message}', 
                                color=colors.RED, 
                                weight=FontWeight.BOLD, 
                                size=16, 
                                max_lines=3,
                                selectable=True
                            ),
                        ]
                    )
                ],
                expand=True,
            ),
            bgcolor=colors.with_opacity(0.05, colors.RED),
            border=border.all(width=1,color=colors.RED),
            border_radius=10,
            padding=10,
            margin=margin.only(left=10),
        )
        return error_message_view
    

    def _get_function_result_graphic(self, dataframe, column_names=None, color=None, graphic_curved=False, max_points_count = 1500) -> Container:
        df = dataframe.get('data')
        graphic_title = dataframe.get('type')

        data_series = []

        if color is None:
            color = colors.LIGHT_GREEN

        if column_names is None:
            column_names = df.columns.tolist()  # Получаем названия столбцов из датафрейма

        if len(df) > max_points_count:
            step = round(len(df) / max_points_count)
            df = df.iloc[::int(step)]

        data_points = [
            LineChartDataPoint(x, y)
            for x, y in zip(df.iloc[:, 0], df.iloc[:, 1])
        ]

        data_series.append(
            LineChartData(
                data_points=data_points,
                stroke_width=1,
                color=color,
                curved=graphic_curved,
                stroke_cap_round=True,
                selected_below_line=ChartPointLine(
                    color=colors.ON_SURFACE,
                    width=1,
                    dash_pattern=[10, 5],
                )
            )
        )

        chart = LineChart(
            data_series=data_series,
            left_axis=ChartAxis(
                title=Text(value=column_names[1]),
                title_size=20,
                labels_size=50,
            ),
            bottom_axis=ChartAxis(
                title=Text(column_names[0]),
                title_size=20,
                labels_size=30
            ),
            top_axis=ChartAxis(
                title=Text(value=graphic_title, size=20),
                title_size=30,
                show_labels=False,
            ),
            border=border.all(1, colors.with_opacity(0.5, colors.ON_SURFACE)),
            horizontal_grid_lines=ChartGridLines(
                width=1, color=colors.with_opacity(0.2, colors.ON_SURFACE),
            ),
            vertical_grid_lines=ChartGridLines(
                width=1, color=colors.with_opacity(0.2, colors.ON_SURFACE),
            ),
            tooltip_bgcolor=colors.with_opacity(0.8, colors.BLACK38),
            expand=True,
        )

        chart_view = Row(controls=[chart])
        if dataframe.get('main_view') != 'chart':
            chart_view = self._get_dropdown_conteiner_for_control(
                control=chart,
                button_name=f"Показать график:{(f' ***{graphic_title.strip()}***')}"
            )
        return chart_view
    

    def _get_function_result_histogram(self, dataframe, color=None):
        df = dataframe.get('data')
        graphic_title = dataframe.get('type')

        if color is None:
            color = colors.LIGHT_GREEN

        column_names = df.columns.tolist()

        bar_groups = [
            BarChartGroup(
                x=round(x_value),
                bar_rods=[
                    BarChartRod(
                        to_y=y_value,
                        color=color,
                    )
                ]
            )
            for x_value, y_value in zip(df.iloc[:, 0], df.iloc[:, 1])
        ]

        histogram = BarChart(
            bar_groups=bar_groups,
            left_axis=ChartAxis(
                title=Text(value=column_names[1]),
                title_size=20,
                labels_size=50,
            ),
            bottom_axis=ChartAxis(
                title=Text(column_names[0]),
                title_size=20,
                labels_size=30
            ),
            top_axis=ChartAxis(
                title=Text(value=graphic_title, size=20),
                title_size=30,
                show_labels=False,
            ),
            border=border.all(1, colors.with_opacity(0.5, colors.ON_SURFACE)),
            horizontal_grid_lines=ChartGridLines(
                width=1, color=colors.with_opacity(0.2, colors.ON_SURFACE),
            ),
            vertical_grid_lines=ChartGridLines(
                width=1, color=colors.with_opacity(0.2, colors.ON_SURFACE),
            ),
            tooltip_bgcolor=colors.with_opacity(0.8, colors.BLACK38),
            interactive=True,
            expand=True,
        )

        histogram_view = Row(controls=[histogram])
        if dataframe.get('main_view') != 'histogram':
            histogram_view = self._get_dropdown_conteiner_for_control(
                control=histogram,
                button_name=f"Показать график:{(f' ***{graphic_title.strip()}***')}"
            )
        return histogram_view


    def _get_datatable_data(self, dataframe) -> Container:
        '''
        Сзодает горизонтальную таблицу данных с прокруткой значений по горизонтали
        '''
        df = dataframe.get('data')
        df_name = dataframe.get('type')
        transposed_df = df.transpose()

        # Создайте таблицу с заголовками (первый столбец)
        header_table = DataTable(
            columns=[DataColumn(Text(""))],
            rows=[
                DataRow([DataCell(Text(str(idx)))])
                for idx in transposed_df.index
            ],
            border=border.only(right=BorderSide(1, color=colors.with_opacity(0.2, colors.ON_SURFACE))),
            horizontal_margin=10,
            heading_row_height=40,
            data_row_max_height=40,
        )

        # Создайте таблицу с данными (остальные столбцы)
        data_table = DataTable(
            columns=[
                DataColumn(Text(str(col)), numeric=True)
                for col in transposed_df.columns
            ],
            rows=[
                DataRow(
                    cells=[
                        DataCell(content=Text(str(value)) if not pd.isna(value) else '')
                        for value in transposed_df.loc[idx]
                    ]
                )
                for idx in transposed_df.index
            ],
            column_spacing=15,
            heading_row_height=40,
            data_row_max_height=40,
            vertical_lines=BorderSide(1, color=colors.with_opacity(0.05, colors.ON_SURFACE))
        )
        
        datatable = Container(
            expand=True,
            content=Row(
                spacing=0,
                controls=[
                    header_table,
                    Row(
                        expand=True,
                        tight=True,
                        scroll=ScrollMode.ADAPTIVE,
                        controls=[data_table]
                    )
                ]
            ),
            border=border.all(1, colors.with_opacity(0.5, colors.ON_SURFACE)),
            border_radius=10,
        )
        # data_table = Markdown(    # ПОПЫТКА ОТОБРАЖАТЬ ТАБЛИЦЫ, ТАКОЙ СПОСОБ БЫ УСКОРИЛ РАБОТУ, ОДНАКО СЕЙЧАС ОТОБРАЖАЕТСЯ НЕКОРРЕКТНО
        #     expand=True,
        #     value=transposed_df.to_markdown(),
        #     extension_set=MarkdownExtensionSet.GITHUB_WEB,
        # )

        datatable_viwe = Row(controls=[datatable])
        if dataframe.get('main_view') != 'table_data':
            datatable_viwe = self._get_dropdown_conteiner_for_control(
                control=datatable,
                button_name=f"Показать таблицу данных:{(f' ***{df_name.strip()}***')}"
            )
        return datatable_viwe
    

    def _get_datatable_statistics(self, dataframe) -> Container:
        '''
        Сзодает вертикальную таблицу для вывода данных
        '''
        df = dataframe.get('data')
        df_name = dataframe.get('type')
        columns = [DataColumn(Text(col)) for col in df.columns]
        rows = []

        for _, row in df.iterrows():
            cells = [DataCell(Text(str(value))) for value in row]
            rows.append(DataRow(cells=cells))

        datatable = DataTable(
            columns=columns,
            rows=rows,
            border=border.all(1, colors.with_opacity(0.5, colors.ON_SURFACE)),
            vertical_lines=BorderSide(1, color=colors.with_opacity(0.05, colors.ON_SURFACE)),
            border_radius=10,
            expand=True,
        )

        datatable_viwe = Row(controls=[datatable])
        if dataframe.get('main_view') != 'table_statistics':
            datatable_viwe = self._get_dropdown_conteiner_for_control(
                control=datatable,
                button_name=f"Показать таблицу статистических параметров:{(f' ***{df_name.strip()}***')}"
            )
        return datatable_viwe
    

    def _get_dropdown_conteiner_for_control(self, control, button_name='Показать', is_open=True) -> Container:
        '''
        Создает контейнер с кнопкой для скрытия/открытия переданного виджета
        '''
        ref_control = Ref[Container]()

        button = IconButton(
            icon=icons.KEYBOARD_ARROW_UP,
            data={
                'control': ref_control,
                'name': button_name,
            },
            on_click=self._change_control_visible
        )
        if not is_open:
            button.icon = None
            button.expand = True
            button.content = Row(
                controls=[
                    Icon(name='KEYBOARD_ARROW_DOWN'),
                    Row(
                        expand=True,
                        wrap=True,
                        controls=[Markdown(value=button_name)]
                    )
                ]
            )

        dropdown_conteiner = Container(
            content=Row(
                controls=[
                    button,
                    Container(
                        ref=ref_control,
                        expand=True,
                        content=control,
                        visible=is_open
                    )
                ],
                vertical_alignment=CrossAxisAlignment.START,
                spacing=0,
            ),
            animate_size=animation.Animation(200, AnimationCurve.FAST_OUT_SLOWIN),
            border_radius=10,
            border=border.only(left=BorderSide(1, colors.with_opacity(0.5, colors.ON_SURFACE))),
        )
        return dropdown_conteiner


    def _change_control_visible(self, e) -> None:
        data = e.control.data
        control = data.get('control').current
        button = e.control
        button_name = data.get('name')

        control.visible = not control.visible

        if control.visible:
            button.icon = icons.KEYBOARD_ARROW_UP
            button.expand = False
            button.content = None
        else:
            button.icon = None
            button.expand = True
            button.content = Row(
                controls=[
                    Icon(name='KEYBOARD_ARROW_DOWN'),
                    Row(
                        expand=True,
                        wrap=True,
                        controls=[
                            Markdown(value=button_name),
                            # Text(value=button_name, max_lines=3),
                        ]
                    )
                ]
            )
        self.graphic_area.update()