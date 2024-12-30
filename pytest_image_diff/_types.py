import pathlib
from typing import BinaryIO, Union, Tuple, Optional, TYPE_CHECKING, Literal
from typing_extensions import Protocol


from PIL.Image import Image as ImageType

if TYPE_CHECKING:
    from .plugin import DiffCompareResult

PathType = Union[str, pathlib.Path]
PathOrFileType = Union[PathType, bytes, BinaryIO]
ImageFileType = Union[ImageType, PathOrFileType]
ImageSize = Tuple[int, int]
ColorModeType = Literal["RGB", "RGBA"]
ImageDiffColorModeType = Union[ColorModeType, None]
ColorType = Tuple[int, int, int]


class ImageRegressionCallableType(Protocol):
    def __call__(
        self,
        image: ImageFileType,
        threshold: Optional[float] = None,
        suffix: Optional[str] = None,
        throw_exception: Optional[bool] = None,
        color_mode: Optional[ImageDiffColorModeType] = None,
        alpha_color: Optional[ColorType] = None,
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
        color_mode: Optional[ImageDiffColorModeType] = None,
        alpha_color: Optional[ColorType] = None,
    ) -> "DiffCompareResult":
        pass


# ``opts.orientation`` can be 'lr' for left-and-right,
# 'tb' for top-and-bottom, or 'auto' for automatic.
OrientationType = Literal["auto", "lr", "tb"]
