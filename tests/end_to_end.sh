set -e

# Create temp repo
pushd $(mktemp -d)
temp_repo=$(pwd)
git init
echo "A" >  a.txt
git add *
git commit -am "First commit"
popd

# tests workspace
pushd $(mktemp -d)
gitorg init
gitorg add local:$temp_repo
gitorg add web:https://github.com/mariocj89/dothub.git
gitorg add github:dothub-sandbox
gitorg add github:mariocj89/github-*

popd
