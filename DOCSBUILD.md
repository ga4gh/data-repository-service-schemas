# Documentation Build Process

This doc (from James Eddy) describes the build process for Swagger UI and static docs (in Travis CI) and subsequent deployment to GitHub Pages (cc @briandoconnor, @denis-yuen, @david4096, @natanlao).

These instructions are based on the current configuration for the [**Workflow Execution Service (WES) API schema repo**](https://github.com/ga4gh/workflow-execution-service-schemas), which includes:

+ **When code is merged into the `master` branch of this repository**, artifacts are created and hosted at the following paths:
  + ga4gh.github.io/[repo]/swagger-ui/ — Swagger UI for the API spec
  + ga4gh.github.io/[repo]/docs/ — reference docs for the API
  + ga4gh.github.io/[repo]/swagger.json — API spec in JSON format
  + ga4gh.github.io/[repo]/swagger.yaml — API spec in YAML format

+ **For non-`master` branches**, reviewers can preview documentation and other pages under "ga4gh.github.io/[repo]/preview/[branch-name]/"
  + swagger-ui/ — Swagger UI preview for current version of [branch-name]
  + docs/ — docs preview for current version of [branch-name]
  + swagger.json — spec (JSON) preview for current version of [branch-name]
  + swagger.yaml — spec (YAML) preview for current version of [branch-name]

+ When changes are pushed to branches on a fork of the main repo (and the user has set up Travis for their forked repo), the same path apply but should be relative to "[user-or-org].github.io/[repo]/".

+ `README.md` and `CONTRIBUTING.md` updated with all of the above links

+ `README.md` badges indicating Travis CI build status and Swagger/OpenAPI validation status


---

## Reference docs with `asciidoctor` and `swagger2markup`

Uses the swagger2markup gradle plugin and asciidoctor to (1) automatically generate human-readable asciidoc files from the contract-first OpenAPI (swagger) yaml spec; and (2) incorporate
manual content to build an overall document in HTML and PDF formats.

You'll need gradle installed to test locally.

<details>

<summary>Steps</summary>

### Set up directory

I started with the setup used in [**this template**](https://github.com/Swagger2Markup/swagger2markup-gradle-project-template) and copied over files for the Swagger2Markup [**gradle plugin**](http://swagger2markup.github.io/swagger2markup/1.3.1/#_gradle_plugin).

**Note:** the choice of directory structure used here was my own, and is somewhat arbitrary. You can reorganize however you like, but you'll need to keep track of paths across various scripts and config files.

```terminal
. # top level repo directory, e.g., 'workflow-execution-service-schemas/'
├── build.gradle
├── gradle
│   └── wrapper
│       ├── gradle-wrapper.jar
│       └── gradle-wrapper.properties
└── gradlew
```

### Update `gradle.settings`

Change root project name (to the name of your repo's project):
```groovy
rootProject.name = 'workflow-execution-service-schemas'
```

### Update `build.gradle`

Add `asciiDocDir` to `ext`:
```groovy
ext {
    asciiDocDir = file("docs/asciidoc")
    asciiDocOutputDir = file("docs/asciidoc/swagger2markup")
}
```

Update paths in `convertSwagger2markup`:
```groovy
convertSwagger2markup {
    swaggerInput file("openapi/workflow_execution_service.swagger.yaml").getAbsolutePath()
    outputDir asciiDocOutputDir
    config = ['swagger2markup.markupLanguage' : 'ASCIIDOC',
              'swagger2markup.extensions.dynamicDefinitions.contentPath' : file('docs/asciidoc/swagger2markup/definitions').absolutePath,
              'swagger2markup.extensions.dynamicOverview.contentPath' : file('docs/asciidoc/swagger2markup/overview').absolutePath,
              'swagger2markup.extensions.dynamicPaths.contentPath' : file('docs/asciidoc/swagger2markup/paths').absolutePath,
              'swagger2markup.extensions.dynamicSecurity.contentPath' : file('docs/asciidoc/swagger2markup/security').absolutePath]
}
```

Add `sourceDir` and `outputDir` to `asciidoctor`:
```groovy
asciidoctor {
    dependsOn convertSwagger2markup
    sourceDir asciiDocDir
    outputDir file("docs")
    sources {
        include 'index.adoc'
    }
    backends = ['html5', 'pdf']
    attributes = [
            doctype: 'book',
            toc: 'left',
            toclevels: '3',
            numbered: '',
            sectlinks: '',
            sectanchors: '',
            hardbreaks: '',
            generated: asciiDocOutputDir
    ]
}
```

Update paths in `watch`:
```groovy
watch {
    asciidoc {
        files fileTree('docs/asciidoc')
        tasks 'asciidoctor'
    }
}
```

### Generate AsciiDoc docs

Run `./gradlew convertSwagger2markup` to convert swagger YAML to AsciiDoc files and initialize the `docs` folder:
```terminal
.
└── docs
    └── asciidoc
        └── swagger2markup
            ├── definitions.adoc
            ├── overview.adoc
            ├── paths.adoc
            └── security.adoc
```

### Add `index.adoc` and `front_matter.adoc`

The [index file](https://github.com/ga4gh/workflow-execution-service-schemas/blob/master/docs/asciidoc/index.adoc) allows you to control the order in which pages are built for HTML and PDF docs; it looks like this:
```adoc
include::{generated}/overview.adoc[]
include::front_matter.adoc[]
include::{generated}/paths.adoc[]
include::{generated}/definitions.adoc[]
```

The ["front matter" file](https://github.com/ga4gh/workflow-execution-service-schemas/blob/master/docs/asciidoc/front_matter.adoc) is where you can add any manual content that you want to integrate with the
generated docs. This content needs to be composed using AsciiDoc (`.adoc`) format:

```adoc
== Section header

Some summary text.

Features:

* feature 1
* feature 2

== Another section header

More text...
```

### Build reference docs

Run `./gradlew asciidoctor` to test. Check `docs/asciidoc/html5/index.html` to see the generated HTML report or `docs/asciidoc/pdf/index.pdf` to see the generated PDF report.

```terminal
.
└── docs
    ├── README.md
    ├── asciidoc
    │   ├── front_matter.adoc
    │   ├── index.adoc
    │   └── swagger2markup
    │       ├── definitions.adoc
    │       ├── overview.adoc
    │       ├── paths.adoc
    │       └── security.adoc
    ├── html5
    │   └── index.html
    └── pdf
        └── index.pdf
```

You can also add a `README.md` to the `docs` folder with a link to where generated docs will be hosted:
```md
View the full [Reference Documentation](https://ga4gh.github.io/workflow-execution-service-schemas/docs/) for the Workflow Execution Service API.
```

</details>

## Swagger UI

I initially used the node package [**generator-openapi-repo**](https://github.com/Rebilly/generator-openapi-repo) to set up Swagger UI stuff for the repo. However, I found that the generator code did way more than I needed, and some other stuff that I couldn't control. I cut out some of the excess pieces and rewrote the associated scripts to minimize the need for random JS code.

Also, with help from @coverbeck, I updated the gradle plugin to install and provide an interface to the Swagger UI node components (eliminating the need for `gulpfile.js`).

<details>

<summary>Steps</summary>

### Set up directory

```terminal
.
├── gulpfile.js  # deprecated; need to remove
├── package.json
└── scripts
    ├── buildui.js  # deprecated; need to remove
    ├── fetchpages.sh
    └── stagepages.sh
```

### Add/edit `package.json`

You should be able to copy the contents of [`package.json`](https://github.com/ga4gh/workflow-execution-service-schemas/blob/master/package.json) from the WES repo to get started. Update `name` and `version` to match the information for your repo.

### Edit `stagepages.sh`

This script builds Swagger UI and sets up various elements in their target locations for deployment to GitHub pages. The path to the swagger YAML is hardcoded in a couple lines, so you'll need to change that.

```shell
#!/usr/bin/env bash

set -e
set -v

if [ "$TRAVIS_BRANCH" == "master" ]; then
    cp docs/html5/index.html docs/
    cp openapi/workflow_execution_service.swagger.yaml ./swagger.yaml
    cp -R web_deploy/* .
elif [ "$TRAVIS_BRANCH" != "gh-pages" ]; then
  branch=$(echo "$TRAVIS_BRANCH" | awk '{print tolower($0)}')
  branchpath="preview/$branch"
  mkdir -p "$branchpath/docs"
  cp docs/html5/index.html "$branchpath/docs/"
  cp openapi/workflow_execution_service.swagger.yaml "$branchpath/swagger.yaml"
  cp -R web_deploy/* "$branchpath/"
fi
```

</details>

### Tweak .gitignore

You need to remove the following line from .gitignore otherwise
the javascript libraries from swagger won't be copied during
gh-pages deploy:

  lib/


## Configure Travis CI for repo

This last step should be pretty straightforward — even though it was the hardest and most time consuming to troubleshoot. :) Here, you'll extend the `.travis.yml` config to run additional steps (after your API spec code has been built and tested) to build, set up, and deploy docs and Swagger elements.

<details>

<summary>Steps</summary>

### Create/add GitHub token

Follow [instructions](https://docs.travis-ci.com/user/deployment/pages/#setting-the-github-token) from Travis CI docs.

### Update `travis.yml`

If you already have a build/test/deply job configured in Travis, you can separate this as a separate stage in `jobs/include` — it's OK for different stages to use different environments. I believe you could also use `matrix` here, but this seems to work.

```yaml
jobs:
  include:
    - stage: test
      language: python
      python:
      - '2.7'
      before_install:
      - sudo apt-get update -qq
      - pip install . --process-dependency-links
      - pip install -r python/dev-requirements.txt
      script:
      - nosetests python/
      - flake8 python
      - ga4gh_wes_client
      deploy:
      ...

    - stage: build_pages
      ...
```

Add docs/swagger build commands for Java-based stage:

**Note:** the `fetchpages.sh` step here effectively acts to retrieve the current state of the `gh-pages` branch and store it to be re-pushed along with the newly generated pages — rather than overwritten.

```yaml
jobs:
  include:
    - stage: test
      ...

    - stage: build_pages
      language: java
      jdk: oraclejdk8
      before_install:
      - chmod +x gradlew
      - chmod +x scripts/fetchpages.sh
      - chmod +x scripts/stagepages.sh
      script:
      - "./scripts/fetchpages.sh"
      - "./gradlew installSwagger buildSwagger asciidoctor"
      - "./scripts/stagepages.sh"
```

Add deploy instructions for GitHub pages:

**Note:** It is important that all of your build/deploy steps for docs and Swagger elements use the same language for the build environment (and preferably part of the same job/stage). Travis *does not* cache information between jobs of different languages, and so pushing to `gh-pages` without missing or overwriting something from a previous job gets really complicated.

```yaml
jobs:
  include:
    - stage: test
      ...

    - stage: build_pages
      language: java
      jdk: oraclejdk8
      before_install:
      - chmod +x gradlew
      - chmod +x scripts/fetchpages.sh
      - chmod +x scripts/stagepages.sh
      script:
      - "./scripts/fetchpages.sh"
      - "./gradlew installSwagger buildSwagger asciidoctor"
      - "./scripts/stagepages.sh"
      deploy:
        provider: pages
        skip-cleanup: true
        github-token: $GITHUB_TOKEN
        on:
          all_branches: true
```

Push to your repo and cross your fingers...

</details>

## Update README links/badges

For ideas on how to set up references to docs and Swagger elements in your main `README.md`, refer to the [**README**](https://github.com/ga4gh/workflow-execution-service-schemas/blob/master/README.md) for the WES API repo.
