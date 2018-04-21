#!/bin/bash

set -e

cd docs

PYTHONPATH=.. make html
