#!/usr/bin/env bash

set -e

git clean -df

pushd src/
python setup.py bdist_wheel --universal
python setup.py bdist_egg
python setup.py sdist --format=bztar, zip, gztar, tar
popd