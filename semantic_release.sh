#!/usr/bin/env bash

# exit if an exit code different than 0 is met
set -e

# this script is meant for labeling the python package accordingly
# and for creating a release on GitHub for master branch

pushd src/

declare -a ACCEPTED_DEVBRANCHES=(
"feature"
"release"
"fix"
"hotfix"
)

unknown_branch () {
  echo "Current branch detected: ${TRAVIS_BRANCH}"
  echo "The following patterns for branches are accepted:"
  for branch in "${ACCEPTED_DEVBRANCHES[@]}"
  do
     echo "branch allowed: ${branch}/*"
  done
  echo "branch allowed: develop"
  echo "branch allowed: master"
}

do_master_release () {
  last_tag=$(git describe --tags --abbrev=0)
  echo "Reading and parsing commit messages since tag $last_tag"

  git log $last_tag HEAD --pretty=format:"%s%n%b" > changelog.txt
  python process_changelog.py $last_tag changelog.txt release.json

  if [[ -f release.json ]]; then
    export PYTHONIOENCODING=utf8

    echo "Creating new release on GitHub on ${TRAVIS_REPO_SLUG}"
    ID=$(curl -X POST https://api.github.com/repos/$TRAVIS_REPO_SLUG/releases?access_token=$GH_TOKEN --header "Content-Type: application/json" -d @release.json | \
      python -c "import sys, json; response = json.load(sys.stdin); out = response['id'] if 'id' in response else -1; print(out);")
    if [[ ID == -1 ]]; then
      echo "Bad response on publishing release with GitHub API"
      exit 3
    else
      echo $ID > release_id.txt
    fi
  else
    echo "Version number not changed, so not creating a new release"
  fi
}

# function for displaying the allowed patterns for branches

PACKAGE_TOREPLACE_NAME=$(python setup.py --name)
PACKAGE_TOREPLACE_VERSION=$(python setup.py --version)

PACKAGE_NAME="gopigo3"
PACKAGE_VERSION=$PACKAGE_TOREPLACE_VERSION

DATE=`date +%Y.%m`

# append to package name the branch name
# and
# append the build number to version

if [[ $TRAVIS_PULL_REQUEST_BRANCH == "" ]]; then

  echo "Detected branch build on ${TRAVIS_BRANCH}"

  # use version numbers (major, minor, patch)
  # and create a release on github if branch is master
  if [[ $TRAVIS_BRANCH == "master" ]]; then
    echo "Creating release on ${TRAVIS_BRANCH}"
    PACKAGE_NAME="${PACKAGE_NAME}"
    do_master_release

  # if it's a develop branch then use the date and the build number
  # in the package's version
  elif [[ $TRAVIS_BRANCH == "develop" ]]; then
    echo "Creating label for package on ${TRAVIS_BRANCH} branch"
    PACKAGE_NAME="${PACKAGE_NAME}-${TRAVIS_BRANCH}"
    PACKAGE_VERSION="${DATE}.dev${TRAVIS_BUILD_NUMBER}"

  # check if we have a branch with a slash in it
  # like feature/awesome-ftr, fix/annoying-issue, etc
  # and then use the type of branch in the version of the package
  elif [[ $TRAVIS_BRANCH == *\/* ]]; then
    echo "Detected branch with slash in it: ${TRAVIS_BRANCH}"
    # check if the branch follows the provided pattern
    TYPE_BRANCH=$(sed 's/\/.*//' <<< ${TRAVIS_BRANCH})
    var=0
    for branch in "${ACCEPTED_DEVBRANCHES[@]}"
    do
       if [[ "${TYPE_BRANCH}" == "${branch}" ]]; then
         var=$((var + 1))
       fi
    done

    # if the branch doesn't fit our patterns
    # then let the build fail
    if [[ $var != 1 ]]; then
      unknown_branch
      exit 1
    # otherwise set the package name and version
    else
      echo "Creating label for package on ${TRAVIS_BRANCH} branch"
      PACKAGE_NAME="${PACKAGE_NAME}-$(sed 's/\//-/g' <<< ${TRAVIS_BRANCH})"
      PACKAGE_VERSION="${DATE}.dev${TRAVIS_BUILD_NUMBER}"
    fi
  else
    unknown_branch
    exit 2
  fi
  echo "Releasing $PACKAGE_NAME=$PACKAGE_VERSION.dev"
else
  # if we have a PR build
  echo "PR build detected on branch ${TRAVIS_PULL_REQUEST_BRANCH}"
  PACKAGE_NAME="${PACKAGE_NAME}-$(sed 's/\//-/g' <<< ${TRAVIS_PULL_REQUEST_BRANCH})"
  PACKAGE_VERSION="${DATE}.dev${TRAVIS_BUILD_NUMBER}"
fi

sed -i -e 's/'"${PACKAGE_TOREPLACE_NAME}"'/'"${PACKAGE_NAME}"'/g' setup.py
sed -i -e 's/'"${PACKAGE_TOREPLACE_VERSION}"'/'"${PACKAGE_VERSION}"'/g' setup.py

popd
