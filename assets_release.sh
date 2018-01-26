#!/usr/bin/env bash

# pushes the built package to GitHub for its specific release

pushd src

if [[ -f release_id.txt ]]; then
  ID=$(cat release_id.txt)
  PYTHON_PKG_NAME="PythonPackage"
  PYTHON_PKG_FILENAME=$(ls dist | head -n 1)

  echo "Publishing python wheel with GitHub API"
  curl "https://uploads.github.com/repos/$TRAVIS_REPO_SLUG/releases/$ID/assets?name=$PYTHON_PKG_NAME&label=python-targz&access_token=$GH_TOKEN" \
  --header "Content-Type: application/octet-stream" \
  --data-binary @"dist/$PYTHON_PKG_FILENAME"
fi

popd
