import os
import shutil
from typing import BinaryIO

from PIL.Image import Image
from _pytest import junitxml


def build_filename(name, suffix='', prefix='', max_length=128):
    return '-'.join(
        filter(None, [prefix, name[:max_length - len(suffix) - len(prefix) - 5], suffix]))


def get_test_info(request, suffix='', prefix=''):
    try:
        names = junitxml.mangle_testnames(request.node.nodeid.split("::"))
    except AttributeError:
        # pytest>=2.9.0
        names = junitxml.mangle_test_address(request.node.nodeid)

    classname = '.'.join(names[:-1])
    test_name = names[-1]
    return {
        'test_name': test_name,
        'classname': classname,
    }


def image_save(image: Image or bytes or str or BinaryIO, path: str):
    if isinstance(image, Image):
        image.save(path)
    elif isinstance(image, str):
        if not os.path.exists(image):
            raise ValueError("Image maybe path. Path not exists!")
        shutil.copyfile(image, path)
    elif hasattr(image, 'read'):
        with open(path, 'wb') as f:
            shutil.copyfileobj(image, f)
    else:
        raise NotImplementedError()

def ensure_dirs(filepath):
    if not os.path.exists(filepath):
        file_dir = os.path.dirname(filepath)
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
