from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .workplace import Workplace

from flet import *


class ResultArea(Column):
    def __init__(self, page: Page, workplace: "Workplace"):
        super().__init__()

        self.page = page
        self.workplace = workplace
