from flet import (
    Container,
    border,
    colors,
    Ref,
    Column,
    IconButton,
    Row,
    MainAxisAlignment,
    CrossAxisAlignment,
    Markdown,
    MarkdownExtensionSet,
    icons,
    animation,
    AnimationCurve,
    Text,
    Icon,
)


class FunctionCardView(Container):
    def __init__(self, function):
        super().__init__()
        self.function = function

        self.ref_card_result = Ref[Column]()
        self.ref_show_button = Ref[IconButton]()

        self.content = self._create_card_content()
        self.data = self
        self.on_click = self.on_change_selected
        
        self.border = border.all(color=colors.BLACK)
        self.bgcolor = colors.BLACK54
        self.border_radius = 10
        self.padding = 5


    def _create_card_content(self):
        '''
        Coздает содержимое карточки функции
        '''
        card_content = Column(
            expand=True,
            controls=[
                Text(self.function.formatted_name),
                # self._create_card_title(),
                # self._create_card_parameters(),
                # self._create_card_result_title(),
                # self._create_card_result_data(),
            ]
        )
        return card_content
    

    def _create_card_title(self) -> Row:
        '''Создает заголовок карточки'''
        return Row(
            alignment=MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=CrossAxisAlignment.START,
            controls=[
                Row(
                    expand=True,
                    wrap=True,
                    controls=[
                        Markdown(
                            extension_set=MarkdownExtensionSet.GITHUB_WEB,
                            value = f'#### **{self.function.print_name}** (*id:*\u00A0***{self.function_id}***)\n' \
                                + f'**{self.function.name}** (*{", ".join(self.function.parameters_names)}*)'
                        ),
                    ],
                ),
                IconButton(
                    icon=icons.DELETE,
                    data=self,
                    on_click=self.on_click_delete
                )
            ],
        )
    

    def _create_card_parameters(self) -> Markdown:
        '''Создает параметры карточки'''
        return Markdown(
            animate_size=200,
            ref=self.ref_card_parameters,
            extension_set=MarkdownExtensionSet.GITHUB_WEB,
            value=self._get_card_parameters_text()
        )
    

    def _create_card_result_title(self, ref_card_result, ref_show_button) -> Row:
        return Row(
            alignment=MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                Markdown(
                    value="#### Результат:"
                ),
                Row(
                    controls=[
                        IconButton(
                            icon=icons.SAVE,
                            on_click=self._open_dialog_save_file
                        ),
                        IconButton(
                            icon=icons.KEYBOARD_ARROW_DOWN,
                            ref=ref_show_button,
                            data={
                                'control': ref_card_result,
                                'button': ref_show_button,
                            },
                            on_click=self._change_function_result_visible
                        ),
                    ]
                )
            ]
        )
    

    def _create_card_result_data(self, ref_card_result, ref_show_button) -> Container:
        return Container(
            animate_size=animation.Animation(200, AnimationCurve.FAST_OUT_SLOWIN),
            content=Column(
                ref=ref_card_result,
                visible=False,
                controls=[
                    Markdown(
                        ref=self.ref_card_result_data,
                        extension_set=MarkdownExtensionSet.GITHUB_WEB,
                        value=self._get_card_parameters_result()
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
                                    'control': ref_card_result,
                                    'button': ref_show_button,
                                },
                                on_click=self._change_function_result_visible
                            ),
                        ]
                    )
                ]
            )
        )