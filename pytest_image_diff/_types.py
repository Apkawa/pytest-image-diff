from typing import BinaryIO, Union, Tuple, Callable, Optional

from PIL.Image import Image
from typing_extensions import Literal


PathOrFileType = Union[str, bytes, BinaryIO]
ImageFileType = Union[Image, PathOrFileType]
ImageSize = Tuple[int, int]

ScreenshotRegressionCallableType = Callable[[float, Optional[str]], bool]
ImageRegressionCallableType = Callable[[ImageFileType, float, Optional[str]], bool]
ImageDiffCallableType = Callable[[ImageFileType, ImageFileType, float, Optional[str]], bool]

# ``opts.orientation`` can be 'lr' for left-and-right,
# 'tb' for top-and-bottom, or 'auto' for automatic.
OrientationType = Literal['auto', 'lr', 'tb']
