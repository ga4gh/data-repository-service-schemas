# Overview

A place to document our use cases for Data Repository Service (DRS).

## Overview from Driver Projects

See [this spreadsheet](https://docs.google.com/spreadsheets/d/1BoigMy4I44Wbd0y-GRvLtUCkGmRk5RAlJYf6zJGlRWg/edit#gid=0) for an overview of what use cases our Driver Projects would like DRS to support.

## Older Information

The sections below are from efforts in 2018 and earlier when DRS was referred to as Data Object Service (DOS).

### Presentation with an Overview

https://docs.google.com/presentation/d/18vB5wDvvvW4nlZDtbidcY5Sv5TbbegLRTT2Ar1a38-U/edit#slide=id.g1cffa4d16d_15_0

### Google Doc with Use Cases

https://docs.google.com/document/d/1KNKYhMLzzbbS4x79PZE_GgVPaPSa4zNpZiey4fF1-Vo/edit

### Another Google Doc from Jonathan with Use Cases

https://docs.google.com/document/d/1UyqzlFpV-jzkB16wWjbwL4OL9HiQZRaqdzHDha7XOmU/edit?ts=59168060#heading=h.a8u6rulb7fu

### Cromwell

The Cromwell group has 4 instances via 2 projects where DOS is being considered. These are all similar enough to effectively be a single use case. We need to model an institution's local storage as a private cloud exposing basic read/write/sizeof functionality akin to GCS or S3. For instance instead of `gs:this/is/my/bucket` it'd be `site1:this/is/my/bucket` or `site2:this/is/my/bucket`. While these use cases don't *need* human readability the stakeholders have expressed preferences towards this over UUID approaches. Similar stances have been taken regarding putting a redirection utility in front of these private clouds.

## ELIXIR RDSDS <-- --> DRS Alignment Presentation

https://drive.google.com/open?id=12gK3X8B-wStbGezyh1nU9w-kZdIvK6UJ
