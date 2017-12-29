#!/usr/bin/env bash

# exit if an exit code different than 0 is met
set -e

git clean -df

pushd src/

PACKAGE_TOREPLACE_NAME=$(python setup.py --name)
PACKAGE_TOREPLACE_VERSION=$(python setup.py --version)

PACKAGE_NAME="gopigo3"
PACKAGE_VERSION=$PACKAGE_TOREPLACE_VERSION

# append to package name the branch name
# and
# append the build number to version
if [[ $TRAVIS_PULL_REQUEST_BRANCH == "" ]]; then
  # if we push to a branch
  # do the appending if only the branch is not master
  if [[ ! $TRAVIS_BRANCH == "master" ]]; then
    PACKAGE_NAME="$PACKAGE_NAME-$(sed 's/\//-/g' <<< $TRAVIS_BRANCH)"
    PACKAGE_VERSION="$PACKAGE_VERSION.$TRAVIS_BUILD_NUMBER"
  fi
else
  # if we have create a PR
  PACKAGE_NAME="$PACKAGE_NAME-$(sed 's/\//-/g' <<< $TRAVIS_PULL_REQUEST_BRANCH)"
  PACKAGE_VERSION="$PACKAGE_VERSION.$TRAVIS_BUILD_NUMBER"
fi

echo "Releasing $PACKAGE_NAME=$PACKAGE_VERSION"

sed -i -e 's/'"$PACKAGE_TOREPLACE_NAME"'/'"$PACKAGE_NAME"'/g' setup.py
sed -i -e 's/'"$PACKAGE_TOREPLACE_VERSION"'/'"$PACKAGE_VERSION"'/g' setup.py

python setup.py sdist

popd
