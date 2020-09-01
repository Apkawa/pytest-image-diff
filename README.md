[![PyPi](https://img.shields.io/pypi/v/pytest-image-diff.svg)](https://pypi.python.org/pypi/pytest-image-diff)
[![Build Status](https://travis-ci.org/Apkawa/pytest-image-diff.svg?branch=master)](https://travis-ci.org/Apkawa/pytest-image-diff)
[![Documentation Status](https://readthedocs.org/projects/pytest-image-diff/badge/?version=latest)](https://pytest-ngrok.readthedocs.io/en/latest/?badge=latest)
[![Codecov](https://codecov.io/gh/Apkawa/pytest-image-diff/branch/master/graph/badge.svg)](https://codecov.io/gh/Apkawa/pytest-image-diff)
[![Requirements Status](https://requires.io/github/Apkawa/pytest-image-diff/requirements.svg?branch=master)](https://requires.io/github/Apkawa/pytest-image-diff/requirements/?branch=master)
[![PyUP](https://pyup.io/repos/github/Apkawa/pytest-image-diff/shield.svg)](https://pyup.io/repos/github/Apkawa/pytest-image-diff)
[![PyPi Python versions](https://img.shields.io/pypi/pyversions/pytest-image-diff.svg)](https://pypi.python.org/pypi/pytest-image-diff)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

# pytest-image-diff

# Installation

```bash
pip install pytest-image-diff
```

or from git

```bash
pip install -e git+https://githib.com/Apkawa/pytest-image-diff.git@master#egg=pytest-image-diff
```

Python>=3.5


# Usage

```python
from PIL import Image


def test_compare(image_diff):
    image: Image or str or bytes = Image.new()
    image2: Image or str or bytes = '/path/to/image.jpeg'
    image_diff(image, image2)

def test_regression(image_regression):
    image: Image or str or bytes = Image.new()
    image_regression(image)
```







