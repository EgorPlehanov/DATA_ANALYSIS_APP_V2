from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ...function import Function

from .result_attributes.dialog_save import DialogSaveResultData
from flet import (
    Page, Container, border, colors, Ref, Column, IconButton,
    Row, MainAxisAlignment, CrossAxisAlignment, Markdown, Text,
    MarkdownExtensionSet, icons, animation, AnimationCurve, Icon,
    DragTarget, Draggable, DragTargetAcceptEvent, ControlEvent
)


# class FunctionCardView(Container):
#     def __init__(self, page: Page, function):
#         super().__init__()
#         self.page = page
#         self.function = function
#         self.key = self.function.id
        
#         self.ref_card_result = Ref[Column]()
#         self.ref_show_button = Ref[IconButton]()
#         self.ref_result_data = Ref[Markdown]()
#         self.ref_card_signature = Ref[Markdown]()

#         self.content = self._create_card_content()
#         self.on_click = self.function._on_click
#         # self.ink = True
        
#         self.border = border.all(color=colors.BLACK)
#         self.bgcolor = colors.BLACK54
#         self.border_radius = 10
#         self.padding = 10

#         self.save_result_data_dialog = self._create_save_result_data_dialog()


# def change_selection(self):
    #     '''Изменяет выделение карточки'''
    #     if self.function.selected:
    #         self.border = border.all(color=colors.BLUE)
    #         self.bgcolor = colors.BLACK26
    #     else:
    #         self.border = border.all(color=colors.BLACK)
    #         self.bgcolor = colors.BLACK54


    # def _create_card_content(self):
    #     '''Coздает содержимое карточки функции'''
    #     card_content = Column(
    #         controls=[
    #             self._create_card_title(),
    #             self._create_card_signature(),
    #             self._create_card_result_title(),
    #             self._create_card_result_data(),
    #         ]
    #     )
    #     return card_content
    

    # def change_selection(self):
    #     '''Изменяет выделение карточки'''
    #     if self.function.selected:
    #         self.border = border.all(color=colors.BLUE)
    #         self.bgcolor = colors.BLACK26
    #     else:
    #         self.border = border.all(color=colors.BLACK)
    #         self.bgcolor = colors.BLACK54


    # def _create_card_content(self):
    #     '''Coздает содержимое карточки функции'''
    #     card_content = Column(
    #         controls=[
    #             self._create_card_title(),
    #             self._create_card_signature(),
    #             self._create_card_result_title(),
    #             self._create_card_result_data(),
    #         ]
    #     )
    #     return card_content



class FunctionCardView(DragTarget):
    def __init__(self, page: Page, function: "Function"):
        super().__init__()
        self.page = page
        self.function = function
        
        self.ref_card_conteiner = Ref[Container]()
        self.ref_card_result = Ref[Column]()
        self.ref_result_show_button = Ref[IconButton]()
        self.ref_result_data = Ref[Markdown]()
        self.ref_card_signature = Ref[Markdown]()

        self.dialog_save_result_data = DialogSaveResultData(function)
        self.page.overlay.append(self.dialog_save_result_data)
        self.page.update()

        self.group = "card"
        self.content = self._create_content()

        self.on_will_accept = self.will_drag_accept
        self.on_accept = self.drag_accept
        self.on_leave = self.drag_leave


    def change_selection(self):
        '''Изменяет выделение карточки'''
        control = self.ref_card_conteiner.current
        if self.function.selected:
            control.border = border.all(color=colors.BLUE)
            control.bgcolor = colors.BLACK26
        else:
            control.border = border.all(color=colors.BLACK)
            control.bgcolor = colors.BLACK54


    def drag_accept(self, e: DragTargetAcceptEvent):
        '''Перемещает карточку (срабатывает при подтверждении перетаскивания)'''
        src: Container = self.page.get_control(e.src_id)
        from_function = src.content.data['function']
        to_function = self.function
        if from_function == to_function:
            return
        
        self.function._graphic_area.change_card_positions(
            from_function, to_function
        )
        function_card: FunctionCardView = src.content.data['card']
        function_card.change_selection()


    def will_drag_accept(self, e: ControlEvent):
        '''Срабатывает при наведении курсора с перетаскиваемой карточкой на эту карточку'''
        self.ref_card_conteiner.current.bgcolor = colors.GREEN
        self.update()


    def drag_leave(self, e: ControlEvent):
        '''Срабатывает при отмене перетаскивания карточки'''
        self.change_selection()
        self.update()


    def _create_content(self) -> Draggable:
        '''Coздает содержимое карточки функции'''
        return Draggable(
            group = self.group,
            content = self._create_draggable_content(),
            content_feedback = Container(
                bgcolor = colors.BLACK87,
                width = 300,
                border = border.all(color=colors.WHITE),
                border_radius = 10,
                padding = 10,
                content = Text(self.function.formatted_name, size=20, color=colors.WHITE),
            ),
        )


    def _create_draggable_content(self) -> Container:
        '''Создает содержимое перетаскиваемого элемента'''
        return Container(
            ref = self.ref_card_conteiner,
            key = self.function.id,
            data = {
                "card": self,
                "function": self.function
            },
            border = border.all(color=colors.BLACK),
            bgcolor = colors.BLACK54,
            border_radius = 10,
            padding = 10,
            on_click = self.function._on_click,
            content = Column(
                controls = [
                    self._create_card_title(),
                    self._create_card_signature(),
                    self._create_card_result_title(),
                    self._create_card_result_data(),
                ]
            )
        )
        
        
    def _create_card_title(self) -> Row:
        '''Создает заголовок карточки'''
        return Row([Row(
            alignment = MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment = CrossAxisAlignment.START,
            expand = True,
            controls=[
                Row(
                    vertical_alignment = CrossAxisAlignment.CENTER,
                    controls=[
                        Column(
                            spacing = 0,
                            horizontal_alignment = CrossAxisAlignment.CENTER,
                            controls=[
                                Icon(icons.CIRCLE, color=self.function.color, size=16),
                                Markdown(
                                    extension_set = MarkdownExtensionSet.GITHUB_WEB,
                                    value = f"*id:*\u00A0***{self.function.id}***"
                                ),
                            ]
                        ),
                        Row(
                            width = 230,
                            wrap = True,
                            controls=[Markdown(
                                extension_set = MarkdownExtensionSet.GITHUB_WEB,
                                value = f"#### **{self.function.name}**"
                            )]
                        )
                    ]
                ),
                IconButton(icons.DELETE, on_click=self.function.delete)
            ]
        )])
    


    def _create_card_signature(self) -> Row:
        '''Создает строку с представление сигнатуры функции'''
        return Row([Row(
            expand=True,
            wrap=True,
            controls=[Markdown(
                    ref = self.ref_card_signature,
                    extension_set = MarkdownExtensionSet.GITHUB_WEB,
                    value = self._create_function_signature()
            )]
        )])


    def _create_function_signature(self):
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
                Row([
                    IconButton(
                        icon=icons.SAVE,
                        on_click=self.dialog_save_result_data.open_dialog
                    ),
                    IconButton(
                        icon=icons.KEYBOARD_ARROW_DOWN,
                        ref=self.ref_result_show_button,
                        on_click=self._change_result_visible
                    ),
                ])
            ]
        )
    

    def _create_card_result_data(self) -> Container:
        '''Создает содержимое результата карточки'''
        return Container(
            animate_size = animation.Animation(200, AnimationCurve.FAST_OUT_SLOWIN),
            content = Column(
                ref = self.ref_card_result,
                visible = False,
                controls = [
                    Markdown(
                        ref = self.ref_result_data,
                        extension_set = MarkdownExtensionSet.GITHUB_WEB,
                        value = self._get_result_table()
                    ),
                    Row(
                        alignment = MainAxisAlignment.END,
                        controls = [
                            IconButton(
                                content = Row(
                                    controls = [
                                        Text("Скрыть результат"),
                                        Icon('KEYBOARD_ARROW_UP')
                                    ]
                                ),
                                on_click = self._change_result_visible
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
    

    def _change_result_visible(self, e: ControlEvent) -> None:
        '''Изменяет видимость результата'''
        self.ref_card_result.current.visible = not self.ref_card_result.current.visible
        if self.ref_card_result.current.visible:
            self.ref_result_show_button.current.icon = icons.KEYBOARD_ARROW_UP
        else:
            self.ref_result_show_button.current.icon = icons.KEYBOARD_ARROW_DOWN
        self.update()


    def update_values(self) -> None:
        '''Обновляет значения текстовых полей сигнатуры со значениями параметров и результатов'''
        self.ref_card_signature.current.value = self._create_function_signature()
        self.ref_result_data.current.value = self._get_result_table()
        self.update()
    