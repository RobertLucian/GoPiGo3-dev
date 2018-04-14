# if there's no package available to be pushed
# then abort the build, which won't affect the build status anyway
pushd src
if [[ ! -f release_id.txt ]]; then
  echo "No packages are being pushed to packagecloud.io"
  exit 4
else
  echo "Found packages to be pushed to packagecloud.io"
fi
popd
