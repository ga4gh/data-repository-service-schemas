#!/usr/bin/env bash
set -ev

if [ "$TRAVIS_BRANCH" == "master" ]; then
    cp docs/html5/index.html docs/
    cp openapi/data_repository_service.swagger.yaml ./swagger.yaml
    mkdir -p swagger-ui/
    cp docs/_swagger-ui-template.html swagger-ui/index.html
elif [ "$TRAVIS_BRANCH" != "gh-pages" ]; then
    branch=$(echo "$TRAVIS_BRANCH" | awk '{print tolower($0)}')
    branchpath="preview/$branch"
    mkdir -p "$branchpath/docs"
    cp docs/html5/index.html "$branchpath/docs/"
    cp docs/pdf/index.pdf "$branchpath/docs/"
    cp openapi/data_repository_service.swagger.yaml "$branchpath/swagger.yaml"
    mkdir -p "$branchpath/swagger-ui/"
    cp docs/_swagger-ui-template.html "$branchpath/swagger-ui/index.html"
fi

# Vendor swagger-ui
npm install swagger-ui-dist@3.20.5
mv $(node -e "console.log(path.dirname(require.resolve('swagger-ui-dist')));") _swagger-ui/

# do some cleanup, these cause the gh-pages deploy to break
rm -rf node_modules
