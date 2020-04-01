import os
from tempfile import NamedTemporaryFile

import pytest
from diffimg import diff

from .helpers import get_test_info, build_filename, image_save, ensure_dirs
from .image_diff import _diff


@pytest.fixture(scope='session')
def image_diff_root(request):
    return request.config.rootdir


@pytest.fixture(scope='session')  # pragma: no cover
def image_diff_dir(image_diff_root):
    """Browser screenshot directory."""
    return os.path.join(image_diff_root, '.tests/image_diff/')


@pytest.fixture(scope='session')
def image_diff_reference_dir(image_diff_root):
    return os.path.join(image_diff_root, 'image_diff_reference')


@pytest.fixture(scope="function")
def image_diff_info(request, image_diff_reference_dir, image_diff_dir):
    def _factory(image, suffix):
        test_info = get_test_info(request)
        reference_dir = os.path.join(image_diff_reference_dir, test_info['classname'])
        screenshot_dir = os.path.join(image_diff_dir, test_info['classname'])
        reference_name = os.path.join(reference_dir,
                                      build_filename(test_info['test_name'],
                                                     suffix=suffix + '-reference.png'))
        image_name = os.path.join(screenshot_dir,
                                  build_filename(test_info['test_name'],
                                                 suffix=suffix + '-screenshot.png'))
        diff_name = os.path.join(screenshot_dir, build_filename(test_info['test_name'],
                                                                suffix=suffix + '-diff.png'))
        return dict(
            diff_name=diff_name,
            image_name=image_name,
            reference_name=reference_name,
        )

    yield _factory


@pytest.fixture(scope="function")
def image_regression(image_diff_info):
    def _factory(image, suffix='', threshold=0.00):
        diff_info = image_diff_info(image, suffix)
        reference_name = diff_info['reference_name']
        diff_name = diff_info['diff_name']
        image_name = diff_info['image_name']
        if not os.path.exists(reference_name):
            ensure_dirs(reference_name)
            image_save(image, reference_name)
            return

        ensure_dirs(image_name)
        image_save(image, image_name)
        diff_ratio = _diff(reference_name, image_name, diff_name)
        assert diff_ratio <= threshold, "Image not equals!"

        # Todo clean empty dirs
        for f in [image_name, diff_name]:
            if os.path.exists(f):
                os.unlink(f)
        return diff_info

    yield _factory


@pytest.fixture(scope="function")
def image_diff(image_diff_info):
    def _factory(image, image_2, diff_path=None, suffix='', threshold=0.00):
        image_temp_file = NamedTemporaryFile(suffix='.jpg')
        image_2_temp_file = NamedTemporaryFile(suffix='.jpg')
        if not diff_path:
            _info = image_diff_info(image, suffix)
            diff_path = _info['diff_name']

        image_save(image, path=image_temp_file.name)
        image_save(image_2, path=image_2_temp_file.name)
        diff_ratio = _diff(image_temp_file.name, image_2_temp_file.name, diff_path)
        assert diff_ratio <= threshold, "Image not equals! See %s" % diff_path
        # Todo clean empty dirs
        for f in [diff_path]:
            if os.path.exists(f):
                os.unlink(f)
        return diff_path

    yield _factory
