Schemas for the Data Object Service (DOS) API
=============================================

The `Global Alliance for Genomics and
Health <http://genomicsandhealth.org/>`_ is an international coalition
formed to enable the sharing of genomic and clinical data. This
collaborative consortium takes place primarily via GitHub and public
meetings.

Cloud Workstream
----------------

The `Data Working Group <http://ga4gh.org/#/>`_ concentrates on data
representation, storage, and analysis, including working with platform
development partners and industry leaders to develop standards that will
facilitate interoperability. The Cloud Workstream is an informal,
multi-vendor working group focused on standards for exchanging
Docker-based tools and CWL/WDL workflows, execution of Docker-based
tools and workflows on clouds, and abstract access to cloud object
stores.

What is DOS?
------------

This proposal for a DOS release is based on the schema work of Brian W.
and others from OHSU along with work by UCSC. It also is informed by
existing object storage systems such as:

-  `GNOS`_ (as used by `PCAWG`_)
-  ICGC Storage (`as used to store data on S3`_, see `overture-stack/score`_)
-  `Human Cell Atlas Storage`_ (see `HumanCellAtlas/data-store`_)
-  `NCI GDC Storage`_
-  `Keep by Curoverse`_ (see `curoverse/arvados`_)

The goal of DOS is to create a generic API on top of these and other
projects, so workflow systems can access data in the same way regardless
of project.

.. _GNOS: http://annaisystems.com/
.. _PCAWG: https://dcc.icgc.org/pcawg
.. _as used to store data on S3: https://dcc.icgc.org/icgc-in-the-cloud/aws
.. _overture-stack/score: https://github.com/overture-stack/score
.. _Human Cell Atlas Storage: https://dss.staging.data.humancellatlas.org/
.. _HumanCellAtlas/data-store: https://github.com/HumanCellAtlas/data-store
.. _NCI GDC Storage: https://gdc.cancer.gov
.. _Keep by Curoverse: https://arvados.org/
.. _curoverse/arvados: https://github.com/curoverse/arvados

Key features
------------

Data object management
^^^^^^^^^^^^^^^^^^^^^^

This section of the API focuses on how to read and write data objects to
cloud environments and how to join them together as data bundles. Data
bundles are simply a flat collection of one or more files. This section
of the API enables:

-  create/update/delete a file
-  create/update/delete a data bundle
-  register UUIDs with these entities (an optionally track versions of
   each)
-  generate signed URLs and/or cloud specific object storage paths and
   temporary credentials

Data object queries
^^^^^^^^^^^^^^^^^^^

A key feature of this API beyond creating/modifying/deletion files is
the ability to find data objects across cloud environments and
implementations of DOS. This section of the API allows users to query by
data bundle or file UUIDs which returns information about where these
data objects are available. This response will typically be used to find
the same file or data bundle located across multiple cloud environments.

Implementations
---------------

There are currently a few experimental implementations that use some
version of these schemas.

-  `DOS Connect <https://github.com/ohsu-comp-bio/dos_connect>`_
   observes cloud and local storage systems and broadcasts their changes
   to a service that presents DOS endpoints.
-  `DOS Downloader <https://github.com/david4096/dos-downloader>`_ is a
   mechanism for downloading Data Objects from DOS URLs.
-  `dos-gdc-lambda <https://github.com/david4096/dos-gdc-lambda>`_
   presents data from the GDC public REST API using the Data Object
   Service.
-  `dos-signpost-lambda <https://github.com/david4096/dos-signpost-lambda>`_
   presents data from a signpost instance using the Data Object Service.

More information
----------------

-  `Global Alliance for Genomics and
   Health <http://genomicsandhealth.org>`__
-  `GA4GH Cloud Workstream <http://ga4gh.cloud>`__