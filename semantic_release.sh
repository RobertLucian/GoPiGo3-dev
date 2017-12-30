#!/usr/bin/env bash

# exit if an exit code different than 0 is met
set -e

pushd src/

declare -a ACCEPTED_DEVBRANCHES=(
"feature"
"release"
"fix"
"hotfix"
)

# function for displaying the allowed patterns for branches
unknown_branch () {
  echo "Current branch detected: ${TRAVIS_BRANCH}"
  echo "The following patterns for branches are accepted:"
  for branch in "${ACCEPTED_DEVBRANCHES[@]}"
  do
     echo "branch allowed: ${branch}\/\*"
  done
  echo "branch allowed: develop"
  echo "branch allowed: master"
}

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
  if [[ $TRAVIS_BRANCH == "master" ]]; then
    PACKAGE_NAME="${PACKAGE_NAME}"
    # semantic release on master

  # check if we've got the develop branch
  elif [[ $TRAVIS_BRANCH == "develop" ]]; then
    PACKAGE_NAME="${PACKAGE_NAME}-develop"
    PACKAGE_VERSION="${TRAVIS_BUILD_NUMBER}.dev"

  # check if we have a branch with a slash in it
  elif [[ $TRAVIS_BRANCH == "*\/*" ]]; then

    # check if the branch follows the provided pattern
    TYPE_BRANCH=$(sed 's/\/.*//' <<< ${TRAVIS_BRANCH})
    $var=0
    for branch in "${ACCEPTED_DEVBRANCHES[@]}"
    do
       if [[ "TYPE_BRANCH" == "${branch}" ]]; then
         var=$((var + 1))
       fi
    done

    # if the branch doesn't fit our patterns
    # then let the build fail
    if [[ $var != 1 ]]; then
      unknown_branch
      exit 3
    # otherwise set the package name and version
    else
      PACKAGE_NAME="${PACKAGE_NAME}-$(sed 's/\//-/g' <<< ${TRAVIS_BRANCH})"
      PACKAGE_VERSION="${TRAVIS_BUILD_NUMBER}.dev"
    fi
  else
    unknown_branch
    exit 3
  fi
  echo "Releasing $PACKAGE_NAME=$PACKAGE_VERSION.dev"
else
  # if we have a PR build
  PACKAGE_NAME="${PACKAGE_NAME}-$(sed 's/\//-/g' <<< ${TRAVIS_PULL_REQUEST_BRANCH})"
  PACKAGE_VERSION="${TRAVIS_BUILD_NUMBER}"
fi

sed -i -e 's/'"${PACKAGE_TOREPLACE_NAME}"'/'"${PACKAGE_NAME}"'/g' setup.py
sed -i -e 's/'"${PACKAGE_TOREPLACE_VERSION}"'/'"${PACKAGE_VERSION}"'/g' setup.py
popd
