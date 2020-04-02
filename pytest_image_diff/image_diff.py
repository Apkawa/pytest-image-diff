from io import BytesIO

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


def resize_canvas(im, new_size) -> BytesIO:
    newImage = Image.new(im.mode, new_size, (255, 0, 255))
    newImage.paste(im, (0, 0, *im.size))
    fp = BytesIO()
    newImage.save(fp, im.format)
    fp.seek(0)
    return fp


def _diff(ref_path: str, image_path: str, diff_path: str) -> float:
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
        if ref_im.size != ref_new_size:
            ref_path = resize_canvas(ref_im, ref_new_size)
        if im.size != im_new_size:
            image_path = resize_canvas(im, im_new_size)

    threshold = diff(
        ref_path, image_path,
        delete_diff_file=True,
        ignore_alpha=True)
    make_highlights(ref_path, image_path, diff_path)
    return threshold
