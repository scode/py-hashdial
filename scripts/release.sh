#!/bin/bash

#pip3 install twine
#pip3 install wheel

python setup.py sdist
python setup.py bdist_wheel
twine upload --repository-url https://test.pypi.org/legacy/ dist/*

echo "If all looks good, finish with: twine upload dist/*"
