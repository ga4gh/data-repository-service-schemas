How to contribute to the DRS GA4GH Schema
======================================

Thank you for taking the time to contribute. We appreciate it!

The GA4GH DRS schema defines an API for sharing data.

There are two ways to contribute to the effort - via issues, which are
used for discussion, and pull requests, which are concrete proposals of
change.

Issues
======

The project's [Issues
Page](https://github.com/ga4gh/data-repository-service-schemas/issues) is a forum to
discuss both major and minor issues related to developing the standards,
formats, and APIs. It also serves as the means for collaborating with
the group and discussing contributions that will ultimately lead to
changes to the formats and APIs. See the [Issue](#issue_resolution)
section below for specifics on how issues are resolved by the community.
Examples of the type of issues that can be submitted are:

-   Identify use cases that will shape the standards and APIs
-   How to add or delete objects and/or object attributes
-   How a particular attribute should be defined
-   Report bugs you encounter when using the reference implementations

Pull Requests
=============

The way to contribute development effort and code to the project is via
GitHub pull requests. GitHub provides a nice [overview on how to create
a pull
request](https://help.github.com/articles/creating-a-pull-request).
Contributions typically require pull requests to each of the schemas,
server and compliance repositories, although pull requests to the server
may merely improve the code without affecting the API, and therefore
changing the schemas or compliance tests. A set of branches across the
repositories each with the same name is a branch set, e.g. the master
branch in each repository forms the master branch set.

Some general rules to follow:
-   Create an issue in Github to track your work and start a conversation. Make a note of the number, you'll
    need it when naming your feature branch below.
-   We follow [HubFlow](https://datasift.github.io/gitflow/) which means we use
    a feature branch strategy with pull requests always going to `develop`
    and releases happening from `master`. **Please read the HubFlow guide linked above, it's a quick read and will give you a really good idea of how our branches work. Do not make pull requests to `master`!**
-   If you are a core developer with write access to the repo, make a feature
    branch following HubFlow conventions in the repo (see next step).  Otherwise
    [fork](https://help.github.com/articles/fork-a-repo) the repo into your personal GitHub space to work on.
-   Create a "feature" branch for each update that you're working on (either in the main repo or your fork depending
    on the previous step). These branches should start with "feature/issue-[number]-[some-description]". For example
    "feature/issue-123-improving-the-docs".  Most devs will use the HubFlow command line tools to do this however, if you
    make a feature branch in GitHub's UI, then please make sure you follow this naming convention.
-   If you are creating a feature branch in the main repo and you follow this
    convention nice things will happen e.g. TravisCI will check your branch and the documentation and swagger will be built
    for you, see the [README.md](README.md) for how to construct a URL to view these for your feature branch.
-   When you're happy with your feature branch, make a [Pull Request](https://help.github.com/articles/about-pull-requests/)
    in GitHub from your feature branch (or fork with a feature branch) to develop.  Pick at least one other person to review
    and write up a good message that links back to the issue you started this whole process with.
-   If you have multiple related pull requests, coordinate pull requests across the branch set by making them as
    simultaneously as possible, and [cross referencing
    them](http://stackoverflow.com/questions/23019608/github-commit-syntax-to-link-a-pull-request-issue).
-   Keep your pull requests as small as possible. Large pull requests
    are hard to review. Try to break up your changes into self-contained
    and incremental pull requests.
-   The first line of commit messages should be a short (&lt;80
    character) summary, followed by an empty line and then any details
    that you want to share about the commit.
-   Please try to follow the [existing syntax style](#syntax_style)

When you submit or change your pull request, the Travis build system
will automatically run tests to ensure valid schema syntax. If your pull
request fails to pass tests, review the test log, make changes and then
push them to your feature branch to be tested again.

Builds with Travis-CI
=====================

We use Travis for CI testing.  If you create a fork and feature branch
this will not automatically be built from our Travis.  However, if you
are a developer and have created a feature branch following the naming
convention above, you should see automated builds.

Check https://app.travis-ci.com/github/ga4gh/data-repository-service-schemas to see the status of the builds.

Pull Request Voting Process
===========================

DRS is very much focused on meeting the needs of our Driver Projects
so this voting process is focused on their needs.

1) We always have an issue created before a PR, this is where a description and initial conversation takes place

2) Someone is assigned the ticket, they bring together one (or more) pull requests... they might do it themselves or ask for help.  Multiple pull requests could be used if there are different approaches that need to be explored

3) David, Brian, and Rishi review the PRs every week on the call (and also ping the mailing list), set a deadline by which drivers (and a few key non-drivers) need to respond with a +1, 0, or -1 by.  A non-vote means 0 so neutral. We try for no "-1"s. Strive to reach consensus with our drivers. We ask that a -1 give us details why.

4) David and Brian as Work Stream leads retain a veto if something goes off the rails

5) We merge or discard depending on the vote/veto by the date we set when the PR was shared with the group

Driver Projects who we will ask to vote on PRs:

Pressing Need:
- AGHA
- ELIXIR
- Genomics England
- HCA
- TOPMed

Fast Follow:
- CanDIG
- ClinGen
- ENA/EGA/EVA
- ICGC ARGO
- NCI DCF
- NIH All of Us

The named key voting implementors are:
- @ddietterich from Verily Data Repo
- @sarpera from Seven Bridges Genomics
- @delagoya from Illumina


Syntax Style and Conventions
============================

The current code conventions for the source files are as follows:

-   Follow the [protocol buffers style
    guide](https://developers.google.com/protocol-buffers/docs/style)
-   Use two-space indentation, and no tabs.
-   Hard-wrap code to 80 characters per line.
-   Comments may use
    [reStructuredText](http://docutils.sourceforge.net/rst.html)
    mark up.

Documentation
=============

The goal of GA4GH is to define an interoperable API specification. To
achieve this, the intent, rationale, and semantics of all Data Objects
and operations need to be clearly and precisely defined. Decisions that
are not captured in documentation are lost.

All schemas defined in GA4GH must include normative documentation. This
should consist of overview and design documentation as well as
documentation in the schemas. This documentation should explain the
goals, overall design, and rationale for decisions that were made. It
must be addressed to both client and server developer audiences. It may
cite published papers or stable web documentation.

Overview documentation should be in markdown format
in the docs/asciidoc/ directory. This format was chosen for
inclusion in documentation build system that is under
development. Graphics are encouraged and should have a source to
drawings in SVG format that will be converted to PNG by the
documentation build.

Our documentation build system is a work in progress and may change.  For
much more information on this see [DOCSBUILD.md](DOCSBUILD.md).

Releases
========

From time to time the group will make a release, this is done with the HubFlow
release process which generally involves creating a branch
"release-foo", where foo is the release name.  And following the HubFlow
tooling for pushing this to master/develop and taggging in GitHub.
Only bug fixes are allowed
to the release branch and the release branch is removed after a successful HubFlow release.
