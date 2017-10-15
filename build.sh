#!/usr/bin/env bash

set -e

git clean -df

pushd src/
python setup.py bdist_wheel
popd