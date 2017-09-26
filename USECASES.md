# Overview

A place to document our use cases for Data Object Service (DOS).

## Presentation wtih an Overview

https://docs.google.com/presentation/d/18vB5wDvvvW4nlZDtbidcY5Sv5TbbegLRTT2Ar1a38-U/edit#slide=id.g1cffa4d16d_15_0

## Google Doc with Use Cases

https://docs.google.com/document/d/1KNKYhMLzzbbS4x79PZE_GgVPaPSa4zNpZiey4fF1-Vo/edit

## Another Google Doc from Jonathan with Use Cases

https://docs.google.com/document/d/1UyqzlFpV-jzkB16wWjbwL4OL9HiQZRaqdzHDha7XOmU/edit?ts=59168060#heading=h.a8u6rulb7fu

## Cromwell

The Cromwell group has 4 instances via 2 projects where DOS is being considered. These are all similar enough to effectively be a single use case. We need to model an institution's local storage as a private cloud exposing basic read/write/sizeof functionality akin to GCS or S3. For instance instead of `gs:this/is/my/bucket` it'd be `site1:this/is/my/bucket` or `site2:this/is/my/bucket`. While these use cases don't *need* human readability the stakeholders have expressed preferences towards this over UUID approaches. Similar stances have been taken regarding putting a redirection utility in front of these private clouds.

## Other Projects to Look At

### Datalad

From Angel:

In the interest of "what else is out there that fits into the use case of DOS" there is Datalad coming from the neuroimaging space:

http://datalad.org/

Datalad Objective

Building atop git-annex, DataLad aims to provide a single, uniform interface to access data from various data-sharing initiatives and data providers, and functionality to create, deliver, update, and share datasets for individuals and portal maintainers. As a command-line tool, it provides an abstraction layer for the underlying Git-based middleware implementing the actual data logistics, and serves as a foundation for other future user front-ends, such as a web-interface.

Datasets

DataLad can create DataLad datasets using any data files published on the web. But the one-time import of data isn't enough, which is why DataLad can be automated to monitor such data sources and incorporate any modifications made to them over time — thus enabling the easy publication and maintenance of entire distributions of datasets.

Using this automated process, the DataLad team maintains data trackers for a number of popular public data portals. These datasets, some automatically generated and others manually created and curated, are collated into a DataLad super-datasetthat is published publicly in its entirety at http://datasets.datalad.org. This super-dataset establishes the official DataLad data distribution that is available via the DataLad resource identifier ///. Some of these datasets (e.g. ///crcns) require authentication credentials, but — other than the supplying of those credentials — access to all resources is completely uniform regardless of the data's origin. DataLad also aggregates all relevant metadata for these datasets — so they can be discovered using DataLad's search.
