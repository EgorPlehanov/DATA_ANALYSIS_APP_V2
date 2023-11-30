from dataclasses import dataclass
from typing import List, Optional
from pandas import DataFrame


@dataclass
class ResultData:
    main_data: Optional[DataFrame]              = None
    type: Optional[str]                         = None
    initial_data: Optional[List['ResultData']]  = None
    extra_data: Optional[List['ResultData']]    = None
    error_message: Optional[str]                = None
    view_chart: Optional[bool]                  = None
    view_histogram: Optional[bool]              = None
    view_table_horizontal: Optional[bool]       = None
    view_table_vertical: Optional[bool]         = None
    main_view: Optional[str]                    = None
