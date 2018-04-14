# if there's no package available to be pushed
# then abort the build, which won't affect the build status anyway
pushd src
if [[ ! -f release_id.txt ]]; then
  exit 4
fi
popd
