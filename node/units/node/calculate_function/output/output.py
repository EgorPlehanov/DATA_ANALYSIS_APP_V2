from flet import *
from typing import Any
from datetime import datetime



def display_result(result: Any, label: str):
    """
    Функция вывода значения
    """
    # return {"result": result}
    cur_time = datetime.now().strftime("%H:%M:%S")
    return {"result": Container(
            border_radius = 10,
            bgcolor = colors.BLACK26,
            padding = padding.only(left=10, top=10, right=10, bottom=10),
            content = Column([
                Container(
                    content = Row(
                        alignment = MainAxisAlignment.CENTER,
                        controls = [Text(
                            value = f"{cur_time}: {label}",
                            weight = FontWeight.BOLD,
                            size = 20,
                            text_align = TextAlign.CENTER
                        )]
                    ),
                ),
                Column([
                    Text(result)
                ]),
            ])
        )
    }
            