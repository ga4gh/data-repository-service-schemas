# Overview 

A place to put a comparison of endpoints/features in DOS to GDC, ICGC, HCA, and potentially other systems.

## DOS vs. HCA, ICGC, and GDC

Brian W. took the first pass at a comparison between GDC and DOS.  See https://docs.google.com/presentation/d/1CCzsff4PZcNwysKPBzHSbTiP611HJO8jDVF1fjEY1nY/edit#slide=id.p

Feature/Endpoints  | DOS | HCA Data Store | ICGC Storage | GDC Signpost
------------------ | --- | -------------- | ------------ | ------------

TODO: fill this in based on the above from Brian W. 

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
