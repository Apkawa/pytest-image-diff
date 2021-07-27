from io import BytesIO
from typing import cast

from PIL import Image
from diffimg import diff
from imgdiff import simple_highlight, tile_images

from pytest_image_diff._types import PathOrFileType, ImageSize, OrientationType


class ImgDiffOpts:
    border: int = 0
    spacing: int = 3
    bgcolor: str = "#FFF"
    sepcolor: str = "#CCC"
    opacity: int = 64
    orientation: OrientationType = "auto"
    timeout: int = 10


def make_highlights(
    ref_path: PathOrFileType, image_path: PathOrFileType, diff_path: PathOrFileType
) -> Image:
    ref_img = Image.open(ref_path).convert("RGB")
    img = Image.open(image_path).convert("RGB")
    opts = ImgDiffOpts()
    mask1, mask2 = simple_highlight(ref_img, img, opts)
    img = tile_images(ref_img, img, mask1, mask2, opts)
    img.save(diff_path)
    return img


def resize_canvas(im: Image, new_size: ImageSize) -> BytesIO:
    new_image = Image.new(im.mode, new_size, (255, 0, 255))
    new_image.paste(im, (0, 0, *im.size))
    fp = BytesIO()
    new_image.save(fp, im.format)
    fp.seek(0)
    return fp


def _diff(
    ref_path: PathOrFileType, image_path: PathOrFileType, diff_path: PathOrFileType
) -> float:
    ref_im = Image.open(ref_path)
    im = Image.open(image_path)

    if ref_im.size != im.size:
        new_w = ref_im.size[0] - im.size[0]
        new_h = ref_im.size[1] - im.size[1]
        ref_new_size = list(ref_im.size)
        im_new_size = list(im.size)
        if new_w < 0:
            ref_new_size[0] = im.size[0]
        elif new_w > 0:
            im_new_size[0] = ref_im.size[0]

        if new_h < 0:
            ref_new_size[1] = im.size[1]
        elif new_h > 0:
            im_new_size[1] = ref_im.size[1]

        _im_new_size: ImageSize = cast(ImageSize, tuple(im_new_size))
        _ref_new_size: ImageSize = cast(ImageSize, tuple(ref_new_size))

        if ref_im.size != ref_new_size:
            ref_path = resize_canvas(ref_im, _ref_new_size)
        if im.size != im_new_size:
            image_path = resize_canvas(im, _im_new_size)

    threshold: float = diff(
        ref_path, image_path, delete_diff_file=True, ignore_alpha=True
    )

    make_highlights(ref_path, image_path, diff_path)
    return threshold
