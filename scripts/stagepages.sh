#!/usr/bin/env bash

set -e
set -v

if [ "$TRAVIS_BRANCH" != "gh-pages" ]; then
  if [ "$TRAVIS_BRANCH" == "master" ]; then
    if [ "$TRAVIS_PULL_REQUEST" == "false" ]; then
      branchpath="."
    else
      branch=$(echo "$TRAVIS_PULL_REQUEST_BRANCH" | awk '{print tolower($0)}')
      branchpath="preview/$branch"
    fi
  else
    branch=$(echo "$TRAVIS_BRANCH" | awk '{print tolower($0)}')
    branchpath="preview/$branch"
  fi
  mkdir -p "$branchpath/docs"
  cp docs/html5/index.html "$branchpath/docs/"
  cp docs/pdf/index.pdf "$branchpath/docs/"
  cp docs/asciidoc/*.png "$branchpath/docs/"
  cp openapi/data_repository_service.swagger.yaml "$branchpath/swagger.yaml"
  cp -R web_deploy/* "$branchpath/"
fi

# do some cleanup, these cause the gh-pages deploy to break
rm -rf node_modules
