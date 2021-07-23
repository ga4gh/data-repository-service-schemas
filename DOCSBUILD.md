# Documentation Build Process

This doc outlines the build process for OpenAPI and HTML docs (in Travis CI) and subsequent deployment to GitHub Pages.

These instructions are based on best practices for using `gh-openapi-docs`, which includes:

+ **When code is merged into the `master` branch of this repository**, artifacts are created and hosted at the following paths:
  + ga4gh.github.io/[repo]/docs/ — reference docs for the API
  + ga4gh.github.io/[repo]/openapi.json — API spec in JSON format
  + ga4gh.github.io/[repo]/openapi.yaml — API spec in YAML format

+ **For non-`master` branches**, reviewers can preview documentation and other pages under "ga4gh.github.io/[repo]/preview/[branch-name]/"
  + docs/ — docs preview for current version of [branch-name]
  + openapi.json — spec (JSON) preview for current version of [branch-name]
  + openapi.yaml — spec (YAML) preview for current version of [branch-name]

+ When changes are pushed to branches on a fork of the main repo (and the user has set up Travis for their forked repo), the same path apply but should be relative to "[user-or-org].github.io/[repo]/".

---

## Reference docs with `gh-openapi-docs`

This repo uses the `gh-openapi-docs` ([Github](https://github.com/ga4gh/gh-openapi-docs), [npm](https://www.npmjs.com/package/@ga4gh/gh-openapi-docs)) command to automatically generate human-readable HTML pages from the OpenAPI specification.

You'll need `nodejs`, `npm`, `openapi-cli`, `redoc-cli`, and `gh-openapi-docs` installed on your machine to build documentation locally. See the [README](https://github.com/ga4gh/gh-openapi-docs) for instructions on installing the `gh-openapi-docs` tool in general, and [.travis.yml](./.travis.yml) for how the tool has been specifically installed for DRS.