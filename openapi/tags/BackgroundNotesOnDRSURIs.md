## Design Motivation

DRS URIs are aligned with the [FAIR data principles](https://www.nature.com/articles/sdata201618) and the [Joint Declaration of Data Citation Principles](https://www.nature.com/articles/sdata20182) — both hostname-based and compact identifier-based URIs provide globally unique, machine-resolvable, persistent identifiers for data.

* We require all URIs to begin with `drs://` as a signal to humans and systems consuming these URIs that the response they will ultimately receive, after transforming the URI to a fetchable URL, will be a DRS JSON packet. This signal differentiates DRS URIs from the wide variety of other entities (HTML documents, PDFs, ontology notes, etc.) that can be represented by compact identifiers.
* We support hostname-based URIs because of their simplicity and efficiency for server and client implementers.
* We support compact identifier-based URIs, and the meta-resolver services of identifiers.org and n2t.net (Name-to-Thing), because of the wide adoption of compact identifiers in the research community. as detailed by [Wimalaratne et al (2018)](https://www.nature.com/articles/sdata201829) in "Uniform resolution of compact identifiers for biomedical data."
