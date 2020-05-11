#!/usr/bin/env bash
set -ev

if [ "$TRAVIS_BRANCH" != "gh-pages" ]; then
  if [ "$TRAVIS_BRANCH" == "master" ]; then
    branchpath="."
  else
    branch=$(echo "$TRAVIS_BRANCH" | awk '{print tolower($0)}')
    branchpath="preview/$branch"
  fi
  echo $branchpath
  mkdir -p "$branchpath/docs"
  cp docs/html5/index.html "$branchpath/docs/"
  cp docs/html5/more_background_on_compact_identifiers.html "$branchpath/docs/"
  cp docs/pdf/index.pdf "$branchpath/docs/"
  cp docs/pdf/more_background_on_compact_identifiers.pdf "$branchpath/docs/"
  cp docs/asciidoc/*.png "$branchpath/docs/"
  cp openapi/data_repository_service.swagger.yaml "$branchpath/swagger.yaml"
  cp -R web_deploy/* "$branchpath/"
fi

# do some cleanup, these cause the gh-pages deploy to break
# rm -rf node_modules
# rm -rf web_deploy
# rm -rf spec
