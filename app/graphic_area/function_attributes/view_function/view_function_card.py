from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ...function import Function

from .result_attributes.dialog_color_picker import DialogColorPicker
from .result_attributes.dialog_save import DialogSaveResultData

import flet as ft
from flet import (
    Page, Container, border, colors, Ref, Column, IconButton,
    Row, MainAxisAlignment, CrossAxisAlignment, Markdown, Text,
    MarkdownExtensionSet, icons, animation, AnimationCurve, Icon,
    DragTarget, Draggable, DragTargetAcceptEvent, ControlEvent
)


class FunctionCardView(DragTarget):
    def __init__(self, page: Page, function: "Function"):
        super().__init__()
        self.page = page
        self.function = function
        self.key = function.id
        
        self.ref_card_conteiner = Ref[Container]()
        self.ref_card_result = Ref[Column]()
        self.ref_result_show_button = Ref[IconButton]()
        self.ref_result_data = Ref[Markdown]()
        self.ref_card_signature = Ref[Markdown]()
        self.ref_card_title_indicator = Ref[Container]()
        self.ref_draggable_title_indicator = Ref[Container]()

        self.dialog_color_picker = DialogColorPicker(function.color, function.update_color)
        self.page.overlay.append(self.dialog_color_picker)

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
        from_function = src.content.data
        to_function = self.function

        if from_function == to_function:
            self.change_selection()
            self.update()
            return
        
        self.function._graphic_area.change_card_positions(
            from_function, to_function
        )


    def will_drag_accept(self, e: ControlEvent):
        '''Срабатывает при наведении курсора с перетаскиваемой карточкой на эту карточку'''
        self.ref_card_conteiner.current.bgcolor = colors.GREEN_500
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
                border = border.all(color=colors.WHITE54),
                border_radius = 10,
                padding = 10,
                content = self._create_title_indicator(self.ref_draggable_title_indicator),
            ),
        )


    def _create_draggable_content(self) -> Container:
        '''Создает содержимое перетаскиваемого элемента'''
        return Container(
            ref = self.ref_card_conteiner,
            key = self.function.id,
            data = self.function,
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
        return Row(
            alignment = MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment = CrossAxisAlignment.START,
            width = 300,
            controls=[
                self._create_title_indicator(self.ref_card_title_indicator),
                IconButton(icons.DELETE, on_click=self.function.delete)
            ]
        )
    

    def _create_title_indicator(self, ref):
        '''Создает индикатор цвета карточки с номером'''
        return Row(
            vertical_alignment = CrossAxisAlignment.CENTER,
            controls=[
                Column(
                    spacing = 0,
                    horizontal_alignment = CrossAxisAlignment.CENTER,
                    controls=[
                        Container(
                            ref = ref,
                            height = 16,
                            width = 16,
                            border_radius = 30,
                            bgcolor = self.function.color,
                            on_click = self.dialog_color_picker.open_dialog,
                            on_hover = self._on_hover_color_indicator,
                        ),
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
        )
    

    def _on_hover_color_indicator(self, e: ControlEvent):
        '''Устанавливает тень вокруг индикатора'''
        if e.data == "true":
            e.control.shadow = ft.BoxShadow(
                spread_radius = 15,
                color = ft.colors.WHITE10,
                blur_style = ft.ShadowBlurStyle.NORMAL,
            )
        else: 
            e.control.shadow = None
        e.control.update()


    def _create_card_signature(self) -> Row:
        '''Создает строку с представление сигнатуры функции'''
        return Markdown(
            ref = self.ref_card_signature,
            width = 300,
            extension_set = MarkdownExtensionSet.GITHUB_WEB,
            value = self._create_function_signature()
        )


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


    def update_color(self):
        '''Обновляет цвет индикатора карточки'''
        title = self.ref_card_title_indicator.current
        title.bgcolor = self.function.color
        title.update()

        draggable = self.ref_draggable_title_indicator.current
        draggable.bgcolor = self.function.color
        draggable.update()
