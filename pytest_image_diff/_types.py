from typing import BinaryIO, Union, Tuple, Optional

from PIL.Image import Image
from typing_extensions import Literal, Protocol

PathOrFileType = Union[str, bytes, BinaryIO]
ImageFileType = Union[Image, PathOrFileType]
ImageSize = Tuple[int, int]


class ImageRegressionCallableType(Protocol):
    def __call__(
        self,
        image: ImageFileType,
        threshold: Optional[float] = None,
        suffix: Optional[str] = None,
    ) -> bool:
        pass


class ImageDiffCallableType(Protocol):
    def __call__(
        self,
        image: ImageFileType,
        image_2: ImageFileType,
        threshold: Optional[float] = None,
        suffix: Optional[str] = None,
    ) -> bool:
        pass


# ``opts.orientation`` can be 'lr' for left-and-right,
# 'tb' for top-and-bottom, or 'auto' for automatic.
OrientationType = Literal["auto", "lr", "tb"]
