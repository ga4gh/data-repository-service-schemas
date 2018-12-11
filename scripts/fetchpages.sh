#!/usr/bin/env bash

set -e
set -v

REPO_URL="https://github.com/$TRAVIS_REPO_SLUG"
rm -rf .ghpages-tmp
mkdir -p .ghpages-tmp
cd .ghpages-tmp
git clone --depth=1 --branch=gh-pages $REPO_URL .
if [ "$TRAVIS_BRANCH" == "master" ]; then
cp -Rn . ../
else
# in case it doesn't exist
mkdir -p preview
cp -Rn preview ../preview/
fi
cd ..
rm -rf .ghpages-tmp
