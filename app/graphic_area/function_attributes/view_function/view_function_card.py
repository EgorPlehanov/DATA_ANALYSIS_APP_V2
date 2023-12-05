import os
from flet import (
    Page, Container, border, colors, Ref, Column, IconButton,
    Row, MainAxisAlignment, CrossAxisAlignment, Markdown,
    MarkdownExtensionSet, icons, animation, AnimationCurve,
    Text, Icon, FilePicker, FilePickerResultEvent, FilePickerFileType
)


class FunctionCardView(Container):
    def __init__(self, page: Page, function):
        super().__init__()
        self.page = page
        self.function = function
        self.key = self.function.id
        
        self.ref_card_result = Ref[Column]()
        self.ref_show_button = Ref[IconButton]()
        self.ref_result_data = Ref[Markdown]()

        self.content = self._create_card_content()
        self.on_click = self.function._on_click
        
        self.border = border.all(color=colors.BLACK)
        self.bgcolor = colors.BLACK54
        self.border_radius = 10
        self.padding = 5

        self.save_result_data_dialog = self._create_save_result_data_dialog()

    
    def change_selection(self):
        '''Изменяет выделение карточки'''
        if self.function.selected:
            self.border = border.all(color=colors.BLUE)
            self.bgcolor = colors.BLACK26
        else:
            self.border = border.all(color=colors.BLACK)
            self.bgcolor = colors.BLACK54


    def _create_card_content(self):
        '''Coздает содержимое карточки функции'''
        card_content = Column(
            expand=True,
            controls=[
                self._create_card_title(),
                self._create_card_result_title(),
                self._create_card_result_data(),
            ]
        )
        return card_content
    

    def _create_card_title(self) -> Row:
        '''Создает заголовок карточки'''
        return Row( # TODO: переписать на Stack
            alignment = MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment = CrossAxisAlignment.START,
            controls = [
                Row(
                    expand = True,
                    wrap = True,
                    controls = [
                        Markdown(
                            extension_set = MarkdownExtensionSet.GITHUB_WEB,
                            value = self._cerate_title_value()
                        ),
                    ],
                ),
                IconButton(
                    icon=icons.DELETE,
                    data=self,
                    on_click=self.function.delete,
                )
            ],
        )
    

    def _cerate_title_value(self):
        '''Создает строку с названием функции на русском и ее пердставление в коде'''
        func_name = f'#### **{self.function.name}** (*id:*\u00A0***{self.function.id}***)\n'
        func_signature = self._get_title_function_signature()
        return func_name + func_signature


    def _get_title_function_signature(self):
        '''Создает строку с представление сигнатуры функции со значениями параметров'''
        formated_parameters = self.function.calculate.get_current_parameters_formatted()
        parameters = '\n\n'.join(
            f"&nbsp;&nbsp;&nbsp;&nbsp;**{name}**: {value}"
            for name, value in formated_parameters.items()
        )
        return f'**{self.function.calculate_function_name}** (\n\n{parameters}\n\n)'


    def _create_card_result_title(self) -> Row:
        '''Создает заголовок результата'''
        return Row(
            alignment=MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                Markdown("#### Результат:"),
                Row(
                    controls=[
                        IconButton(
                            icon=icons.SAVE,
                            on_click=self._open_dialog_save_to_file
                        ),
                        IconButton(
                            icon=icons.KEYBOARD_ARROW_DOWN,
                            ref=self.ref_show_button,
                            on_click=self._change_result_visible
                        ),
                    ]
                )
            ]
        )
    

    def _create_card_result_data(self) -> Container:
        return Container(
            animate_size=animation.Animation(200, AnimationCurve.FAST_OUT_SLOWIN),
            content=Column(
                ref=self.ref_card_result,
                visible=False,
                controls=[
                    Markdown(
                        ref=self.ref_result_data,
                        extension_set=MarkdownExtensionSet.GITHUB_WEB,
                        value=self._get_result_table()
                    ),
                    Row(
                        alignment=MainAxisAlignment.END,
                        controls=[
                            IconButton(
                                content=Row(
                                    controls=[
                                        Text(value="Скрыть результат"),
                                        Icon(name='KEYBOARD_ARROW_UP')
                                    ]
                                ),
                                on_click=self._change_result_visible
                            ),
                        ]
                    )
                ]
            )
        )


    def _get_result_table(self, max_rows=10) -> str:
        '''Создает таблицное представление результатов'''
        data = self.function.get_result_main_data()
        if data is None or data.empty:
            return '***Нет данных***'
        
        if len(data) <= max_rows:
            markdown_table = data.to_markdown()
        else:
            df_head = data.head(max_rows // 2)
            df_tail = data.tail(max_rows // 2)

            tail_rows = []
            for idx, row in df_tail.iterrows():
                row_text = f'| {idx} | ' + " | ".join(map(str, row)) + ' |'
                tail_rows.append(row_text)

            table_separator = '\n|' + '|'.join(['...'] * (data.shape[1] + 1)) + '|\n' if data.shape[0] > 10 else ""
            markdown_table = df_head.to_markdown() + table_separator + '\n'.join(tail_rows)
                
        return markdown_table
    

    def _change_result_visible(self, e):
        '''Изменяет видимость результата'''
        self.ref_card_result.current.visible = not self.ref_card_result.current.visible
        if self.ref_card_result.current.visible:
            self.ref_show_button.current.icon = icons.KEYBOARD_ARROW_UP
        else:
            self.ref_show_button.current.icon = icons.KEYBOARD_ARROW_DOWN
        self.update()
    

    def _create_save_result_data_dialog(self) -> FilePicker:
        '''Создает диалоговое окно для сохранения результата'''
        return FilePicker(
            on_result=self._save_result_data,
        )
    

    def _save_result_data(self, e: FilePickerResultEvent) -> None:
        '''Сохраняет результаты в файл'''
        path = e.path
        if not path:
            return
        file_format = os.path.splitext(path)[-1][1:].lower()

        if file_format not in ['csv', 'json']:
            path = f'{path}.csv'
            file_format = 'csv'

        try:
            with open(path, 'w') as file:
                data_to_save = self.function.get_result_main_data()
                match file_format:
                    case 'csv':
                        data_to_save.to_csv(file, index=False)
                    case 'json':
                        data_to_save.to_json(file, orient='records')
                    case _:
                        raise Exception(f'Неизвестный формат файла: {file_format}')
                        
        except Exception as ex:
            print(f'Ошибка при сохранении: {ex}')
    

    def _open_dialog_save_to_file(self, e) -> None:
        '''Открывает диалоговое окно cохранения результата'''
        self.page.overlay.append(self.save_result_data_dialog)
        self.page.update()

        parameters_text = "; ".join([
            f"{param}={value}".replace(': ', '-')
            for param, value in self.function.calculate.get_current_parameters_formatted().items()
            if 'show' not in param
        ])
        parameters_text = (parameters_text[:100] + '...') if len(parameters_text) > 100 else parameters_text

        self.save_result_data_dialog.save_file(
            dialog_title = f"Сохрание результата функции {self.function.formatted_name}",
            file_name = f"{self.function.name}({parameters_text}).csv",
            file_type = FilePickerFileType.CUSTOM,
            allowed_extensions = ['csv', 'json'],
        )
