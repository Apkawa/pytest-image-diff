from PIL import Image
from diffimg import diff
from imgdiff import simple_highlight, tile_images


class ImgdiffOpts:
    border = 0
    spacing = 3
    bgcolor = '#FFF'
    sepcolor = '#CCC'
    opacity = 64
    orientation = 'auto'
    timeout = 10


def make_highlights(ref_path, image_path, diff_path):
    ref_img = Image.open(ref_path).convert("RGB")
    img = Image.open(image_path).convert("RGB")
    mask1, mask2 = simple_highlight(ref_img, img, ImgdiffOpts)
    img = tile_images(ref_img, img, mask1, mask2, ImgdiffOpts)
    img.save(diff_path)
    return img


def _diff(ref_path: str, image_path: str, diff_path: str) -> float:

    threshold = diff(
        ref_path, image_path,
        delete_diff_file=True,
        ignore_alpha=True)
    make_highlights(ref_path, image_path, diff_path)
    return threshold
