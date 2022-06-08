from pathlib import Path
from typing import BinaryIO, Union, Tuple, Optional, TYPE_CHECKING
from typing_extensions import Literal, Protocol

from PIL.Image import Image

if TYPE_CHECKING:
    from .plugin import DiffCompareResult

PathOrFileType = Union[str, bytes, Path, BinaryIO]
ImageFileType = Union[Image, PathOrFileType]
ImageSize = Tuple[int, int]


class ImageRegressionCallableType(Protocol):
    def __call__(
        self,
        image: ImageFileType,
        threshold: Optional[float] = None,
        suffix: Optional[str] = None,
        throw_exception: Optional[bool] = None,
    ) -> "DiffCompareResult":
        pass


class ImageDiffCallableType(Protocol):
    def __call__(
        self,
        image: ImageFileType,
        image_2: ImageFileType,
        threshold: Optional[float] = None,
        suffix: Optional[str] = None,
        throw_exception: Optional[bool] = None,
    ) -> "DiffCompareResult":
        pass


# ``opts.orientation`` can be 'lr' for left-and-right,
# 'tb' for top-and-bottom, or 'auto' for automatic.
OrientationType = Literal["auto", "lr", "tb"]
