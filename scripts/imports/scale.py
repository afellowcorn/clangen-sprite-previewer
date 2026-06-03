from math import floor
from typing import Tuple

def ui_scale_dimensions(dim: Tuple[int, int]):
    """
    Use to scale the dimensions of an item - WILL IGNORE NEGATIVE VALUES
    :param dim: The dimensions to scale
    :return: The scaled dimensions
    """
    return (
        (
            floor(dim[0] * 1)
            if dim[0] > 0
            else dim[0]
        ),
        (
            floor(dim[1] * 1)
            if dim[1] > 0
            else dim[1]
        ),
    )