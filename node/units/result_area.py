from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .workplace import Workplace

from flet import *


class ResultArea(Container):
    def __init__(self, page: Page, workplace: "Workplace"):
        super().__init__()

        self.page = page
        self.workplace = workplace
        
        self.expand = True
        self.alignment = alignment.top_center
        self.bgcolor = colors.PURPLE_900

        self.result_controls = [Text("Результаты")]
        self.content = self.create_controls()


    def create_controls(self):
        return Column(
            tight = True,
            expand = True,
            scroll = ScrollMode.AUTO,
            controls = [Container(
                padding = 10,
                content = Column(
                    spacing = 10,
                    controls = self.result_controls
                ) 
            )]
        )
    
    
    
    
