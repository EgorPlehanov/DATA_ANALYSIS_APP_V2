from typing import Any
from flet import (
    Row, colors, border, BorderSide, Container,animation, Markdown,
    AnimationCurve, Ref, IconButton, Icon, CrossAxisAlignment, icons
)


class ResultToggleContainer(Container):
    def __init__(self,
        control: Any = None,
        button_name: str = 'Показать',
        is_open: bool = True
    ):
        super().__init__()
        self.control = control
        self.button_name = button_name
        self.is_open = is_open

        self.ref_control = Ref[Container]()
        self.ref_button = Ref[IconButton]()

        self.content = self.create_content()

        self.animate_size = animation.Animation(200, AnimationCurve.FAST_OUT_SLOWIN)
        self.border_radius = 10
        self.border = border.only(left=BorderSide(1, colors.with_opacity(0.5, colors.ON_SURFACE)))


    def create_content(self) -> Row:
        '''Создает блок с кнопкой для скрытия/открытия переданного виджета'''
        return Row(
        controls = [
            self._create_button(),
            Container(
                ref = self.ref_control,
                expand = True,
                content = self.control,
                visible = self.is_open
            )
        ],
        vertical_alignment = CrossAxisAlignment.START,
        spacing = 0,
    )


    def _create_button(self) -> IconButton:
        '''Создает кнопку для скрытия/открытия переданного виджета'''
        button = IconButton(
            ref = self.ref_button,
            icon = icons.KEYBOARD_ARROW_UP,
            expand = not self.is_open,
            on_click = self._change_control_visible
        )
        if not self.is_open:
            button.icon = None
            button.content = Row(
                controls = [
                    Icon(name='KEYBOARD_ARROW_DOWN'),
                    Row(
                        expand = True,
                        wrap = True,
                        controls = [Markdown(self.button_name)]
                    )
                ]
            )
        return button
            

    def _change_control_visible(self, e) -> None:
        '''Изменяет видимость блока при нажатии на кнопку'''
        button: IconButton = e.control
        control = self.ref_control.current

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
                            Markdown(self.button_name),
                            # Text(value=button_name, max_lines=3),
                        ]
                    )
                ]
            )
        self.update()
