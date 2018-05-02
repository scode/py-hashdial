#!/bin/bash

set -e

venv_dir=$(mktemp -d)

virtualenv -p python3.6 "${venv_dir}"
pip3 install -r requirements.txt

echo "Done. To activate: source ${venv_dir}/bin/activate"


