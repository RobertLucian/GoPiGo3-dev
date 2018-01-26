#!/usr/bin/env bash

# exit if an exit code different than 0 is met
set -e

pushd src/
python setup.py sdist
popd
