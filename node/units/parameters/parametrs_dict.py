from .parametr_typing import *
from .parametr_out_value import *
from .parametr_single_value import *



type_to_param = {
    ParameterType.OUT: OutParam,
    ParameterType.SINGLE_VALUE: SingleValueParam
}