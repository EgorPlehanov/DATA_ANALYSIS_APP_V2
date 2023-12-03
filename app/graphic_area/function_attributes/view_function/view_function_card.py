from flet import (
    Container, border, colors, Ref, Column, IconButton,
    Row, MainAxisAlignment, CrossAxisAlignment, Markdown,
    MarkdownExtensionSet, icons, animation, AnimationCurve,
    Text, Icon,
)


class FunctionCardView(Container):
    def __init__(self, function):
        super().__init__()
        self.function = function
        
        self.ref_card_result = Ref[Column]()
        self.ref_show_button = Ref[IconButton]()
        self.ref_result_data = Ref[Markdown]()

        self.content = self._create_card_content()
        # self.on_click = self._change_selected
        
        self.border = border.all(color=colors.BLACK)
        self.bgcolor = colors.BLACK54
        self.border_radius = 10
        self.padding = 5


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
        return Row(
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
                    # on_click=self.on_click_delete
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
                            # on_click=self._open_dialog_save_file
                        ),
                        IconButton(
                            icon=icons.KEYBOARD_ARROW_DOWN,
                            ref=self.ref_show_button,
                            data={
                                'control': self.ref_card_result,
                                'button': self.ref_show_button,
                            },
                            # on_click=self._change_function_result_visible
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
                        # value=self._get_card_parameters_result()
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
                                data={
                                    'control': self.ref_card_result,
                                    'button': self.ref_show_button,
                                },
                                # on_click=self._change_function_result_visible
                            ),
                        ]
                    )
                ]
            )
        )