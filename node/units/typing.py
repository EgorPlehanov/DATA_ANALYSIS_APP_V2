from dataclasses import dataclass, field
from typing import List
from flet import icons




@dataclass
class Folder:
    key: str = "unknown"
    name: str = "Untitled"
    icon: str = icons.QUESTION_MARK
    obj_list: List = field(default_factory=list)