# Contributing

## Setup

```bash
python3 -m venv ~/.virtualenv/pytest-image-diff/
source ~/.virtualenv/pytest-image-diff/bin/activate
pip install -r requirements-dev.txt
```

## Run tests

```bash
pytest
tox
```

## Build docs
```
python setup.py build_sphinx
```

## Bump version

```bash
python setup.py bumpversion
```

## Publish pypi

```bash
python setup.py publish
```

