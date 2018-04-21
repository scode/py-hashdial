#!/bin/bash

set -ex

export PYTHONPATH=.

flake8
mypy $(find hashdial tests -name '*.py')
pytest
