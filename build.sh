#!/usr/bin/env bash

# exit if an exit code different than 0 is met
set -e

pushd src/
if [[ -f release_id.txt || ${TRAVIS_BRANCH} != "master" ]]; then
  python setup.py sdist
fi
popd
